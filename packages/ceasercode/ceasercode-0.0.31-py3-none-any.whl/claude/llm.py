"""
Unified LLM client using OpenAI-compatible interface for all providers.
Supports OpenAI, Ollama, Google GenAI, OpenRouter, and vLLM.
"""

import json
import base64
from typing import Dict, List, Optional, Union, Any, Iterator, Callable
from openai import OpenAI
import requests


class OAI:
    """
    Unified OpenAI-compatible LLM client supporting multiple providers.
    """
    
    PROVIDERS = {
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "api_key": None,  # Must be provided
            "default_model": "gpt-4"
        },
        "ollama": {
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",  # Required but unused
            "default_model": "llama3.2"
        },
        "google": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "api_key": None,  # Must be provided
            "default_model": "gemini-2.0-flash-exp"
        },
        "openrouter": {
            "base_url": "https://openrouter.ai/api/v1",
            "api_key": None,  # Must be provided
            "default_model": "google/gemini-2.0-flash-exp:free"
        },
        "vllm": {
            "base_url": "http://localhost:8000/v1",
            "api_key": "vllm",  # Required but unused
            "default_model": None  # Will be detected from server
        }
    }
    
    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the unified LLM client.
        
        Args:
            provider: Provider name (openai, ollama, google, openrouter, vllm)
            api_key: API key for the provider
            base_url: Custom base URL for the provider
            model: Model name to use
            **kwargs: Additional configuration options
        """
        if provider not in self.PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}. Available: {list(self.PROVIDERS.keys())}")
        
        self.provider = provider
        provider_config = self.PROVIDERS[provider].copy()
        
        # Override with custom values
        if api_key:
            provider_config["api_key"] = api_key
        if base_url:
            provider_config["base_url"] = base_url
        if model:
            provider_config["default_model"] = model
        
        # Validate required API key
        if provider in ["openai", "google", "openrouter"] and not provider_config["api_key"]:
            raise ValueError(f"API key is required for provider: {provider}")
        
        self.config = provider_config
        self.model = provider_config["default_model"]
        self.kwargs = kwargs
        
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=provider_config["api_key"],
            base_url=provider_config["base_url"]
        )
        
        # Auto-detect model for vLLM if not specified
        if provider == "vllm" and not self.model:
            self._detect_vllm_model()
    
    def _detect_vllm_model(self):
        """Auto-detect available model from vLLM server."""
        try:
            models = self.client.models.list()
            if models.data:
                self.model = models.data[0].id
        except Exception:
            self.model = "default"  # Fallback
    
    def _encode_media_from_url(self, url: str) -> str:
        """Encode media content from URL to base64."""
        response = requests.get(url)
        response.raise_for_status()
        return base64.b64encode(response.content).decode('utf-8')
    
    def _prepare_messages(self, messages: List[Dict]) -> List[Dict]:
        """Prepare messages for the API call, handling multimodal content."""
        prepared = []
        for msg in messages:
            if isinstance(msg.get("content"), list):
                # Handle multimodal content
                content_parts = []
                for part in msg["content"]:
                    if part.get("type") == "image_url":
                        # Handle image content
                        image_url = part["image_url"]["url"]
                        if image_url.startswith("http"):
                            # Convert URL to base64
                            encoded = self._encode_media_from_url(image_url)
                            part["image_url"]["url"] = f"data:image/jpeg;base64,{encoded}"
                        content_parts.append(part)
                    elif part.get("type") in ["video_url", "audio_url"]:
                        # Handle video/audio content
                        media_url = part[part["type"]]["url"]
                        if media_url.startswith("http"):
                            encoded = self._encode_media_from_url(media_url)
                            media_type = "video/mp4" if part["type"] == "video_url" else "audio/wav"
                            part[part["type"]]["url"] = f"data:{media_type};base64,{encoded}"
                        content_parts.append(part)
                    else:
                        content_parts.append(part)
                
                prepared.append({**msg, "content": content_parts})
            else:
                prepared.append(msg)
        
        return prepared
    
    def run(
        self,
        messages: List[Dict],
        model: Optional[str] = None,
        stream: bool = False,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Union[str, Dict]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict] = None,
        extra_body: Optional[Dict] = None,
        **kwargs
    ) -> Union[Any, Iterator[Any]]:
        """
        Universal run method supporting all features.
        
        Args:
            messages: Chat messages
            model: Model to use (defaults to configured model)
            stream: Whether to stream the response
            tools: Function tools for tool calling
            tool_choice: Tool choice strategy
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            response_format: Response format specification
            extra_body: Additional parameters for structured outputs
            **kwargs: Additional API parameters
        
        Returns:
            Response object or stream iterator
        """
        # Prepare parameters
        params = {
            "model": model or self.model,
            "messages": self._prepare_messages(messages),
            "stream": stream,
            **kwargs
        }
        
        # Add optional parameters
        if tools:
            params["tools"] = tools
        if tool_choice:
            params["tool_choice"] = tool_choice
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens:
            params["max_tokens"] = max_tokens
        if response_format:
            params["response_format"] = response_format
        if extra_body:
            params["extra_body"] = extra_body
        
        # Make the API call
        return self.client.chat.completions.create(**params)
    
    def chat(
        self,
        messages: List[Dict],
        **kwargs
    ) -> Any:
        """Simple chat completion (non-streaming)."""
        return self.run(messages, stream=False, **kwargs)
    
    def stream_chat(
        self,
        messages: List[Dict],
        **kwargs
    ) -> Iterator[Any]:
        """Streaming chat completion."""
        return self.run(messages, stream=True, **kwargs)
    
    def tool_call(
        self,
        messages: List[Dict],
        tools: List[Dict],
        tool_choice: Optional[Union[str, Dict]] = "auto",
        **kwargs
    ) -> Any:
        """Chat completion with tool calling."""
        return self.run(
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            **kwargs
        )
    
    def structured_output(
        self,
        messages: List[Dict],
        schema: Optional[Dict] = None,
        choice: Optional[List[str]] = None,
        regex: Optional[str] = None,
        grammar: Optional[str] = None,
        **kwargs
    ) -> Any:
        """Generate structured output using various constraints."""
        extra_body = {}
        
        if schema:
            extra_body["guided_json"] = schema
        elif choice:
            extra_body["guided_choice"] = choice
        elif regex:
            extra_body["guided_regex"] = regex
        elif grammar:
            extra_body["guided_grammar"] = grammar
        
        return self.run(
            messages=messages,
            extra_body=extra_body if extra_body else None,
            **kwargs
        )
    
    def multimodal_chat(
        self,
        text: str,
        images: Optional[List[str]] = None,
        videos: Optional[List[str]] = None,
        audio: Optional[List[str]] = None,
        **kwargs
    ) -> Any:
        """
        Multimodal chat with images, videos, and audio.
        
        Args:
            text: Text prompt
            images: List of image URLs or base64 strings
            videos: List of video URLs or base64 strings  
            audio: List of audio URLs or base64 strings
        """
        content = [{"type": "text", "text": text}]
        
        # Add images
        if images:
            for img_url in images:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": img_url}
                })
        
        # Add videos
        if videos:
            for vid_url in videos:
                content.append({
                    "type": "video_url", 
                    "video_url": {"url": vid_url}
                })
        
        # Add audio
        if audio:
            for aud_url in audio:
                content.append({
                    "type": "audio_url",
                    "audio_url": {"url": aud_url}
                })
        
        messages = [{"role": "user", "content": content}]
        return self.run(messages, **kwargs)
    
    def execute_tool_calls(
        self,
        tool_calls: List[Any],
        available_tools: Dict[str, Callable],
        messages: List[Dict]
    ) -> List[Dict]:
        """
        Execute tool calls and return updated messages.
        
        Args:
            tool_calls: Tool calls from the model response
            available_tools: Dictionary mapping tool names to functions
            messages: Current conversation messages
            
        Returns:
            Updated messages with tool results
        """
        # Add assistant message with tool calls
        messages.append({
            "role": "assistant",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function", 
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in tool_calls
            ]
        })
        
        # Execute each tool call
        for call in tool_calls:
            tool_name = call.function.name
            if tool_name in available_tools:
                try:
                    args = json.loads(call.function.arguments)
                    result = available_tools[tool_name](**args)
                    
                    messages.append({
                        "role": "tool",
                        "content": str(result),
                        "tool_call_id": call.id,
                        "name": tool_name
                    })
                except Exception as e:
                    messages.append({
                        "role": "tool", 
                        "content": f"Error: {str(e)}",
                        "tool_call_id": call.id,
                        "name": tool_name
                    })
        
        return messages
    
    def get_models(self) -> List[str]:
        """Get available models from the provider."""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception:
            return [self.model] if self.model else []
    
    def __repr__(self) -> str:
        return f"OAI(provider='{self.provider}', model='{self.model}')"


# Convenience functions for different providers
def create_openai_client(api_key: str, model: str = "gpt-4", **kwargs) -> OAI:
    """Create OpenAI client."""
    return OAI(provider="openai", api_key=api_key, model=model, **kwargs)

def create_ollama_client(base_url: str = "http://localhost:11434/v1", model: str = "llama3.2", **kwargs) -> OAI:
    """Create Ollama client."""
    return OAI(provider="ollama", base_url=base_url, model=model, **kwargs)

def create_google_client(api_key: str, model: str = "gemini-2.0-flash-exp", **kwargs) -> OAI:
    """Create Google GenAI client."""
    return OAI(provider="google", api_key=api_key, model=model, **kwargs)

def create_openrouter_client(api_key: str, model: str = "google/gemini-2.0-flash-exp:free", **kwargs) -> OAI:
    """Create OpenRouter client."""
    return OAI(provider="openrouter", api_key=api_key, model=model, **kwargs)

def create_vllm_client(base_url: str = "http://localhost:8000/v1", model: Optional[str] = None, **kwargs) -> OAI:
    """Create vLLM client."""
    return OAI(provider="vllm", base_url=base_url, model=model, **kwargs)