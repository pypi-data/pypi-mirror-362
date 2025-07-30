from typing import Optional, List, Dict, Any, Union, Callable, Generator
from ollama import Client
from .__util import convert_function_to_tool
from pydantic import BaseModel


class Ollama:
    def __init__(self, **kwargs):
        self.client = Client(**kwargs)

    def __call__(
        self,
        prompt: str="",
        system_prompt: Optional[str] = None,
        schema: Optional[Union[Dict[str, Any], BaseModel]] = None,
        messages: Optional[list] = None,
        tools: Optional[List[Callable]] = None,
        model: str = None,
        temperature: float = None,
        num_ctx: int = None,
        seed: Optional[int] = None,
        **kwargs
    ) -> Generator[Dict[str, Any], None, None]:
        """
        LLM function using Ollama with streaming support

        Args:
            prompt (str): The user prompt
            system_prompt (str, optional): System prompt to guide the model
            schema (Union[Dict, BaseModel], optional): Pydantic model or dict schema for structured output
            tools (List[Callable], optional): List of Python functions to use as tools
            messages:Optional[list]: messages list
            model (str): Ollama model name
            temperature (float): Temperature for response generation (default: 0)
            num_ctx (int): Context window size (default: 20000)
            seed (int, optional): Random seed for reproducible outputs
            **kwargs: Additional options to pass to Ollama (e.g., top_p, top_k, repeat_penalty, etc.)

        Yields:
            Dict[str, Any]: Streaming response chunks with content and tool calls
        """
        # Build messages
        if not messages:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

        # Prepare chat parameters
        options = {
            "temperature": temperature,
            "num_ctx": num_ctx
        }
        if seed is not None:
            options["seed"] = seed

        # Add any additional options from kwargs
        options.update(kwargs)

        chat_params = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": options,
        }

        # Add tools if provided
        if tools:
            converted_tools = [convert_function_to_tool(tool) for tool in tools]
            chat_params["tools"] = converted_tools

        # Add format/schema if provided
        if schema:
            if isinstance(schema, type) and issubclass(schema, BaseModel):
                chat_params["format"] = schema.model_json_schema()
            else:
                chat_params["format"] = schema

        for chunk in self.client.chat(**chat_params):
            yield chunk

    def chat(
        self,
        prompt: str="",
        system_prompt: Optional[str] = None,
        schema: Optional[Union[Dict[str, Any], BaseModel]] = None,
        messages: Optional[list] = None,
        tools: Optional[List[Callable]] = None,
        model: str = None,
        temperature: float = None,
        num_ctx: int = None,
        seed: Optional[int] = None,
        **kwargs
    ) -> Generator[Dict[str, Any], None, None]:
        """
        LLM function using Ollama with streaming support

        Args:
            prompt (str): The user prompt
            system_prompt (str, optional): System prompt to guide the model
            schema (Union[Dict, BaseModel], optional): Pydantic model or dict schema for structured output
            tools (List[Callable], optional): List of Python functions to use as tools
            messages:Optional[list]: messages list
            model (str): Ollama model name
            temperature (float): Temperature for response generation (default: 0)
            num_ctx (int): Context window size (default: 20000)
            seed (int, optional): Random seed for reproducible outputs
            **kwargs: Additional options to pass to Ollama (e.g., top_p, top_k, repeat_penalty, etc.)

        Yields:
            Dict[str, Any]: Streaming response chunks with content and tool calls
        """
        # Build messages
        if not messages:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

        # Prepare chat parameters
        options = {
            "temperature": temperature,
            "num_ctx": num_ctx
        }
        if seed is not None:
            options["seed"] = seed

        # Add any additional options from kwargs
        options.update(kwargs)

        chat_params = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": options,
        }

        # Add tools if provided
        if tools:
            converted_tools = [convert_function_to_tool(tool) for tool in tools]
            chat_params["tools"] = converted_tools

        # Add format/schema if provided
        if schema:
            if isinstance(schema, type) and issubclass(schema, BaseModel):
                chat_params["format"] = schema.model_json_schema()
            else:
                chat_params["format"] = schema

        return self.client.chat(**chat_params)
