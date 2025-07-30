from typing import Optional, List, Dict, Any, Union, Callable, Generator
from openai import OpenAI
from pydantic import BaseModel
from .__util import convert_function_to_tool

# vLLM client using OpenAI-compatible API
class VLLM:
    def __init__(self,host="http://0.0.0.0",port=8000):
        self.client = OpenAI(
            base_url=f"{host}:{port}/v1",  # vLLM OpenAI-compatible endpoint
            api_key="sk-dummy"     # vLLM doesn't require real API key for local inference
        )

def __call__(
    self,
    prompt: str,
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
    LLM function using vLLM with OpenAI-compatible API and streaming support
    
    Args:
        prompt (str): The user prompt
        system_prompt (str, optional): System prompt to guide the model
        schema (Union[Dict, BaseModel], optional): Pydantic model or dict schema for structured output
        messages (list, optional): messages list
        tools (List[Callable], optional): List of Python functions to use as tools
        model (str): vLLM model name
        temperature (float): Temperature for response generation (default: 0)
        num_ctx (int): Context window size (default: 20000)
        seed (int, optional): Random seed for reproducible outputs
        **kwargs: Additional options to pass to vLLM
    
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
    chat_params = {
        "model": model,
        "messages": messages,
        "stream": True,
        "temperature": temperature,
        "max_tokens": num_ctx,
    }
    
    # Add seed if provided
    if seed is not None:
        chat_params["seed"] = seed
    
    # Add tools if provided
    if tools:
        converted_tools = [convert_function_to_tool(tool) for tool in tools]
        chat_params["tools"] = converted_tools
    
    # Handle structured output via schema
    extra_body = {}
    if schema:
        if isinstance(schema, type) and issubclass(schema, BaseModel):
            # Pydantic model - get JSON schema for guided generation
            json_schema = schema.model_json_schema()
            extra_body["guided_json"] = json_schema
        else:
            # Assume it's already a dict schema
            extra_body["guided_json"] = schema
    
    # Add any additional vLLM-specific options from kwargs
    extra_body.update(kwargs)
    
    if extra_body:
        chat_params["extra_body"] = extra_body
    
    # Stream the response
    try:
        stream = self.client.chat.completions.create(**chat_params)
        
        for chunk in stream:
            # Convert OpenAI format to Ollama-like format for compatibility
            if chunk.choices and len(chunk.choices) > 0:
                choice = chunk.choices[0]
                
                # Build response chunk in Ollama format
                response_chunk = {
                    "model": model,
                    "created_at": chunk.created,
                    "done": False
                }
                
                # Handle content
                if choice.delta.content:
                    response_chunk["message"] = {
                        "role": "assistant",
                        "content": choice.delta.content
                    }
                
                # Handle tool calls
                if choice.delta.tool_calls:
                    tool_calls = []
                    for tool_call in choice.delta.tool_calls:
                        if tool_call.function:
                            tool_calls.append({
                                "function": {
                                    "name": tool_call.function.name,
                                    "arguments": tool_call.function.arguments
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
                
    except Exception as e:
        # Return error in Ollama format
        yield {
            "model": model,
            "created_at": None,
            "done": True,
            "error": str(e)
        }
