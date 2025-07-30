from typing import Optional, List, Dict, Any, Union, Callable, Generator
from openai import OpenAI
from pydantic import BaseModel
try:
    from .__util import convert_function_to_tool
except ImportError:
    # Fallback for direct import
    from __util import convert_function_to_tool


class FunctionWrapper:
    """Wrapper for tool call function data"""
    def __init__(self, function_dict: dict):
        self._data = function_dict
    
    @property
    def name(self):
        return self._data.get('name', '')
    
    @property
    def arguments(self):
        args_str = self._data.get('arguments', '{}')
        try:
            import json
            return json.loads(args_str) if isinstance(args_str, str) else args_str
        except:
            return {}


class ToolCallWrapper:
    """Wrapper for tool call data"""
    def __init__(self, tool_call_dict: dict):
        self._data = tool_call_dict
        if 'function' in tool_call_dict:
            self.function = FunctionWrapper(tool_call_dict['function'])
        else:
            self.function = FunctionWrapper({})
    
    @property
    def id(self):
        return self._data.get('id', '')
    
    @property
    def type(self):
        return self._data.get('type', 'function')


class MessageWrapper:
    """Wrapper to make dict responses compatible with attribute access"""
    def __init__(self, message_dict: dict):
        self._data = message_dict
    
    @property
    def content(self):
        return self._data.get('content', '')
    
    @property
    def role(self):
        return self._data.get('role', 'assistant')
    
    @property
    def tool_calls(self):
        tool_calls_data = self._data.get('tool_calls', None)
        if tool_calls_data and isinstance(tool_calls_data, list):
            return [ToolCallWrapper(tc) for tc in tool_calls_data]
        return tool_calls_data


class ResponseWrapper:
    """Wrapper to make dict responses compatible with Ollama-style attribute access"""
    def __init__(self, response_dict: dict):
        self._data = response_dict
        if 'message' in response_dict:
            self.message = MessageWrapper(response_dict['message'])
        else:
            # Create empty message for compatibility
            self.message = MessageWrapper({'content': '', 'role': 'assistant'})
    
    @property
    def model(self):
        return self._data.get('model', '')
    
    @property
    def created_at(self):
        return self._data.get('created_at', None)
    
    @property
    def done(self):
        return self._data.get('done', True)


class OAI:
    def __init__(self, base_url: str = "https://api.openai.com/v1", api_key: str = None, **kwargs):
        """
        Initialize OpenAI-compatible client (works with OpenAI, OpenRouter, etc.)
        
        Args:
            base_url (str): API base URL (default: OpenAI API)
            api_key (str): API key for authentication
            **kwargs: Additional client parameters
        """
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            **kwargs
        )

    def __call__(
        self,
        prompt: str = "",
        system_prompt: Optional[str] = None,
        schema: Optional[Union[Dict[str, Any], BaseModel]] = None,
        messages: Optional[list] = None,
        tools: Optional[List[Callable]] = None,
        model: str = None,
        temperature: float = None,
        num_ctx: int = None,
        seed: Optional[int] = None,
        stream: bool = True,
        **kwargs
    ) -> Generator[Dict[str, Any], None, None]:
        """
        LLM function using OpenAI-compatible API with streaming support
        
        Args:
            prompt (str): The user prompt
            system_prompt (str, optional): System prompt to guide the model
            schema (Union[Dict, BaseModel], optional): Pydantic model or dict schema for structured output
            messages (list, optional): messages list
            tools (List[Callable], optional): List of Python functions to use as tools
            model (str): Model name
            temperature (float): Temperature for response generation
            num_ctx (int): Context window size (max_tokens)
            seed (int, optional): Random seed for reproducible outputs
            stream (bool): Whether to stream responses (default: True)
            **kwargs: Additional options to pass to the API
        
        Yields:
            Dict[str, Any]: Streaming response chunks with content and tool calls
        """
        # Build messages
        if not messages:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            if prompt:
                messages.append({"role": "user", "content": prompt})
        
        # Prepare chat parameters
        chat_params = {
            "model": model,
            "messages": messages,
            "stream": stream,
        }
        
        # Add optional parameters
        if temperature is not None:
            chat_params["temperature"] = temperature
        if num_ctx is not None:
            chat_params["max_tokens"] = num_ctx
        if seed is not None:
            chat_params["seed"] = seed
        
        # Add tools if provided
        if tools:
            converted_tools = [convert_function_to_tool(tool) for tool in tools]
            chat_params["tools"] = converted_tools
            chat_params["tool_choice"] = "auto"
        
        # Handle structured output via response_format (for compatible models)
        if schema:
            if isinstance(schema, type) and issubclass(schema, BaseModel):
                # For models that support structured output
                chat_params["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "response",
                        "schema": schema.model_json_schema()
                    }
                }
            else:
                # Fallback: add schema instruction to system prompt
                schema_instruction = f"\\n\\nPlease respond with valid JSON matching this schema: {schema}"
                if messages and messages[0]["role"] == "system":
                    messages[0]["content"] += schema_instruction
                else:
                    messages.insert(0, {"role": "system", "content": f"You are a helpful assistant.{schema_instruction}"})
        
        # Add any additional API-specific options from kwargs
        chat_params.update(kwargs)
        
        # Stream the response
        try:
            if stream:
                stream_response = self.client.chat.completions.create(**chat_params)
                
                for chunk in stream_response:
                    # Convert OpenAI format to Ollama-like format for compatibility
                    if chunk.choices and len(chunk.choices) > 0:
                        choice = chunk.choices[0]
                        
                        # Build response chunk in Ollama format
                        response_chunk = {
                            "model": model,
                            "created_at": getattr(chunk, 'created', None),
                            "done": False
                        }
                        
                        # Handle content
                        if choice.delta.content:
                            response_chunk["message"] = {
                                "role": "assistant",
                                "content": choice.delta.content
                            }
                        
                        # Handle tool calls - note: streaming tool calls can be fragmented
                        if choice.delta.tool_calls:
                            tool_calls = []
                            for tool_call in choice.delta.tool_calls:
                                if tool_call.function and tool_call.function.name:
                                    tool_calls.append({
                                        "function": {
                                            "name": tool_call.function.name,
                                            "arguments": tool_call.function.arguments or ""
                                        }
                                    })
                            
                            if tool_calls:
                                if "message" not in response_chunk:
                                    response_chunk["message"] = {"role": "assistant"}
                                response_chunk["message"]["tool_calls"] = tool_calls
                        
                        # Check if done
                        if choice.finish_reason:
                            response_chunk["done"] = True
                            response_chunk["done_reason"] = choice.finish_reason
                        
                        yield response_chunk
            else:
                # Non-streaming response
                response = self.client.chat.completions.create(**chat_params)
                choice = response.choices[0]
                
                response_chunk = {
                    "model": model,
                    "created_at": getattr(response, 'created', None),
                    "done": True,
                    "message": {
                        "role": "assistant",
                        "content": choice.message.content or ""
                    }
                }
                
                # Handle tool calls in non-streaming mode
                if choice.message.tool_calls:
                    tool_calls = []
                    for tool_call in choice.message.tool_calls:
                        tool_calls.append({
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        })
                    response_chunk["message"]["tool_calls"] = tool_calls
                
                if choice.finish_reason:
                    response_chunk["done_reason"] = choice.finish_reason
                
                yield response_chunk
                
        except Exception as e:
            # Return error in Ollama format
            yield {
                "model": model,
                "created_at": None,
                "done": True,
                "error": str(e)
            }

    def chat(
        self,
        prompt: str = "",
        system_prompt: Optional[str] = None,
        schema: Optional[Union[Dict[str, Any], BaseModel]] = None,
        messages: Optional[list] = None,
        tools: Optional[List[Callable]] = None,
        model: str = None,
        temperature: float = None,
        num_ctx: int = None,
        seed: Optional[int] = None,
        **kwargs
    ) -> ResponseWrapper:
        """
        Non-streaming chat completion
        
        Returns:
            ResponseWrapper: Complete response with attribute access compatibility
        """
        # Use __call__ with stream=False and get the single response
        for response in self.__call__(
            prompt=prompt,
            system_prompt=system_prompt,
            schema=schema,
            messages=messages,
            tools=tools,
            model=model,
            temperature=temperature,
            num_ctx=num_ctx,
            seed=seed,
            stream=False,
            **kwargs
        ):
            return ResponseWrapper(response)