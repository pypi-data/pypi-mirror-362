"""
Example usage of Qwen class with tool calling
"""

from _qwen import Qwen
import json

# Define your tool functions
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract second number from first number"""
    return a - b

def get_weather(location: str) -> str:
    """Get current weather for a location"""
    # Mock weather data
    return f"The weather in {location} is sunny, 25°C"

# Helper function to get function by name
def get_function_by_name(name: str):
    """Get function by name for tool execution"""
    functions = {
        "add": add,
        "subtract": subtract,
        "get_weather": get_weather
    }
    return functions.get(name)

def main():
    # Initialize Qwen client
    qwen = Qwen(
        model="Qwen/Qwen3-8B",
        host="http://localhost", 
        port=8000,
        api_key="EMPTY"
    )
    
    # Define tools to use
    tools = [add, subtract, get_weather]
    
    # Initial user message
    messages = [
        {"role": "user", "content": "What is 15 + 27? Also, what's the weather like in Paris?"}
    ]
    
    print("🤖 Starting conversation with Qwen...")
    print(f"User: {messages[0]['content']}")
    print()
    
    # First call - model will generate tool calls
    print("🔄 Making initial request...")
    response = qwen.chat(
        messages=messages,
        tools=tools,
        enable_thinking=True
    )
    
    messages.append(response["message"])
    print(f"Assistant response: {response}")
    print()
    
    # Check if model wants to call functions
    if "tool_calls" in response["message"]:
        print("🔧 Model wants to call functions:")
        
        # Execute each function call
        for tool_call in response["message"]["tool_calls"]:
            function = tool_call["function"]
            fn_name = function["name"]
            fn_args = json.loads(function["arguments"])
            
            print(f"  - Calling {fn_name} with args: {fn_args}")
            
            # Execute the function
            try:
                result = get_function_by_name(fn_name)(**fn_args)
                print(f"  - Result: {result}")
                
                # Add function result to messages
                messages.append({
                    "role": "function",
                    "name": fn_name,
                    "content": json.dumps(result)
                })
                
            except Exception as e:
                print(f"  - Error: {e}")
                messages.append({
                    "role": "function", 
                    "name": fn_name,
                    "content": f"Error: {str(e)}"
                })
        
        print()
        print("🔄 Getting final response with tool results...")
        
        # Second call - model will use the tool results to generate final response
        final_response = qwen.chat(
            messages=messages,
            tools=tools,
            enable_thinking=True
        )
        
        print(f"Final Assistant Response: {final_response['message']['content']}")
        
    else:
        print("No tool calls needed")
        print(f"Assistant: {response['message']['content']}")

def streaming_example():
    """Example of streaming usage"""
    print("\n" + "="*50)
    print("🌊 STREAMING EXAMPLE")
    print("="*50)
    
    qwen = Qwen(
        model="Qwen/Qwen3-8B",
        host="http://localhost",
        port=8000,
        api_key="EMPTY"
    )
    
    tools = [add, subtract, get_weather]
    
    messages = [
        {"role": "user", "content": "Calculate 100 - 25 and tell me about the weather in Tokyo"}
    ]
    
    print(f"User: {messages[0]['content']}")
    print("\nAssistant (streaming):")
    
    # Collect responses for tool execution
    collected_responses = []
    
    for chunk in qwen(
        messages=messages,
        tools=tools,
        enable_thinking=True
    ):
        if chunk.get("error"):
            print(f"Error: {chunk['error']}")
            break
            
        if chunk.get("message"):
            message = chunk["message"]
            collected_responses.append(message)
            
            # Print content as it streams
            if message.get("content"):
                print(message["content"], end="", flush=True)
            
            # Handle tool calls
            if message.get("tool_calls"):
                print("\n🔧 Tool calls detected:")
                for tool_call in message["tool_calls"]:
                    function = tool_call["function"]
                    fn_name = function["name"]
                    fn_args = json.loads(function["arguments"])
                    
                    print(f"  - {fn_name}({fn_args})")
                    
                    # Execute function
                    try:
                        result = get_function_by_name(fn_name)(**fn_args)
                        print(f"  - Result: {result}")
                        
                        # Add to messages for next iteration
                        messages.append({
                            "role": "function",
                            "name": fn_name,
                            "content": json.dumps(result)
                        })
                    except Exception as e:
                        print(f"  - Error: {e}")
        
        if chunk.get("done"):
            print("\n✅ Done")
            break
    
    # If there were tool calls, make another request with results
    if any(msg.get("role") == "function" for msg in messages[1:]):
        print("\n🔄 Getting final response with tool results...")
        
        for chunk in qwen(
            messages=messages,
            tools=tools,
            enable_thinking=True
        ):
            if chunk.get("message", {}).get("content"):
                print(chunk["message"]["content"], end="", flush=True)
            
            if chunk.get("done"):
                print("\n✅ Final response complete")
                break

if __name__ == "__main__":
    main()
    streaming_example()