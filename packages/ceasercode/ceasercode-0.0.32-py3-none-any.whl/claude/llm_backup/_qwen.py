from typing import Optional, List, Dict, Any, Union, Callable, Generator
from qwen_agent.llm import get_chat_model
from pydantic import BaseModel
from .__util import convert_function_to_tool
import json


class Qwen:
    def __init__(self, model="Qwen/Qwen3-8B", host="http://localhost", port=8000, api_key="EMPTY"):
        self.llm = get_chat_model({
            "model": model,
            "model_server": f"{host}:{port}/v1",
            "api_key": api_key,
            "generate_cfg": {
                "extra_body": {
                    "chat_template_kwargs": {"enable_thinking": True}
                }
            }
        })

    def __call__(
        self,
        prompt: str = "",
        system_prompt: Optional[str] = None,
        schema: Optional[Union[Dict[str, Any], BaseModel]] = None,
        messages: Optional[list] = None,
        tools: Optional[List[Callable]] = None,
        model: str = None,
        temperature: float = 0.7,
        top_p: float = 0.8,
        max_tokens: int = 512,
        enable_thinking: bool = True,
        repetition_penalty: float = 1.05,
        seed: Optional[int] = None,
        **kwargs
    ) -> Generator[Dict[str, Any], None, None]:
        """
        LLM function using Qwen-Agent with streaming support
        
        Args:
            prompt (str): The user prompt
            system_prompt (str, optional): System prompt to guide the model
            schema (Union[Dict, BaseModel], optional): Pydantic model or dict schema for structured output
            messages (list, optional): messages list
            tools (List[Callable], optional): List of Python functions to use as tools
            model (str): Qwen model name (ignored, uses init model)
            temperature (float): Temperature for response generation (default: 0.7)
            top_p (float): Top-p sampling parameter (default: 0.8)
            max_tokens (int): Maximum tokens to generate (default: 512)
            enable_thinking (bool): Enable thinking mode for reasoning models (default: True)
            repetition_penalty (float): Repetition penalty (default: 1.05)
            seed (int, optional): Random seed for reproducible outputs
            **kwargs: Additional options
        
        Yields:
            Dict[str, Any]: Streaming response chunks with content and tool calls
        """
        # Build messages
        if not messages:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

        # Convert tools to functions format for Qwen-Agent
        functions = None
        if tools:
            functions = []
            for tool in tools:
                converted_tool = convert_function_to_tool(tool)
                functions.append(converted_tool["function"])

        try:
            # Use Qwen-Agent's streaming chat
            for responses in self.llm.chat(
                messages=messages,
                functions=functions,
                stream=True
            ):
                # Process each response message
                for response in responses:
                    response_chunk = {
                        "model": model or "qwen",
                        "created_at": None,
                        "done": False
                    }
                    
                    # Handle regular content
                    if response.get("content"):
                        response_chunk["message"] = {
                            "role": "assistant",
                            "content": response["content"]
                        }
                    
                    # Handle function calls
                    if response.get("function_call"):
                        fn_call = response["function_call"]
                        response_chunk["message"] = {
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [{
                                "function": {
                                    "name": fn_call["name"],
                                    "arguments": fn_call["arguments"]
                                }
                            }]
                        }
                    
                    # Handle reasoning content (thinking mode)
                    if response.get("reasoning_content"):
                        response_chunk["message"] = {
                            "role": "assistant",
                            "content": response["reasoning_content"],
                            "reasoning": True
                        }
                    
                    yield response_chunk
                    
            # Final done message
            yield {
                "model": model or "qwen",
                "created_at": None,
                "done": True
            }
                    
        except Exception as e:
            yield {
                "model": model or "qwen",
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
        temperature: float = 0.7,
        top_p: float = 0.8,
        max_tokens: int = 512,
        enable_thinking: bool = True,
        repetition_penalty: float = 1.05,
        seed: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        LLM function using Qwen-Agent (non-streaming)
        
        Args:
            prompt (str): The user prompt
            system_prompt (str, optional): System prompt to guide the model
            schema (Union[Dict, BaseModel], optional): Pydantic model or dict schema for structured output
            messages (list, optional): messages list
            tools (List[Callable], optional): List of Python functions to use as tools
            model (str): Qwen model name (ignored, uses init model)
            temperature (float): Temperature for response generation (default: 0.7)
            top_p (float): Top-p sampling parameter (default: 0.8)
            max_tokens (int): Maximum tokens to generate (default: 512)
            enable_thinking (bool): Enable thinking mode for reasoning models (default: True)
            repetition_penalty (float): Repetition penalty (default: 1.05)
            seed (int, optional): Random seed for reproducible outputs
            **kwargs: Additional options
        
        Returns:
            Dict[str, Any]: Response with content and tool calls
        """
        # Build messages
        if not messages:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

        # Convert tools to functions format for Qwen-Agent
        functions = None
        if tools:
            functions = []
            for tool in tools:
                converted_tool = convert_function_to_tool(tool)
                functions.append(converted_tool["function"])

        try:
            # Use Qwen-Agent's non-streaming chat
            for responses in self.llm.chat(
                messages=messages,
                functions=functions
            ):
                # Process responses and build result
                result = {
                    "model": model or "qwen",
                    "created_at": None,
                    "done": True
                }
                
                # Collect all responses
                all_content = []
                tool_calls = []
                reasoning_content = []
                
                for response in responses:
                    if response.get("content"):
                        all_content.append(response["content"])
                    
                    if response.get("function_call"):
                        fn_call = response["function_call"]
                        tool_calls.append({
                            "function": {
                                "name": fn_call["name"],
                                "arguments": fn_call["arguments"]
                            }
                        })
                    
                    if response.get("reasoning_content"):
                        reasoning_content.append(response["reasoning_content"])
                
                # Build message
                message = {
                    "role": "assistant",
                    "content": "\n".join(all_content) if all_content else ""
                }
                
                if tool_calls:
                    message["tool_calls"] = tool_calls
                
                if reasoning_content:
                    message["reasoning_content"] = "\n".join(reasoning_content)
                
                result["message"] = message
                return result
                
        except Exception as e:
            return {
                "model": model or "qwen",
                "created_at": None,
                "done": True,
                "error": str(e)
            }