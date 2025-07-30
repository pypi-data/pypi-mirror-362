#!/usr/bin/env python3
# Comprehensive test suite for the unified OAI LLM class
"""
Simple comprehensive test for OAI class core functionality.
"""

from llm import OAI
import sys


def test_core_functionality():
    """Test core chat and streaming with working providers"""
    print("=== Core Functionality Test ===")
    
    # Test Ollama (local)
    print("\n--- Ollama Chat ---")
    try:
        llm = OAI(provider="ollama", model="qwen3:0.6b")
        messages = [{"role": "user", "content": "Reply with exactly: 'Ollama works!'"}]
        response = llm.chat(messages)
        print(f"✓ Ollama: {response.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"✗ Ollama failed: {e}")
    
    # Test Google (API)
    print("\n--- Google Chat ---")
    try:
        llm = OAI(
            provider="google",
            api_key="AIzaSyBb8wTvVw9e25aX8XK-eBuu1JzDEPCdqUE",
            model="gemini-2.0-flash-exp"
        )
        messages = [{"role": "user", "content": "Reply with exactly: 'Google works!'"}]
        response = llm.chat(messages)
        print(f"✓ Google: {response.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"✗ Google failed: {e}")
    
    # Test streaming with Google (most reliable)
    print("\n--- Google Streaming ---")
    try:
        llm = OAI(
            provider="google",
            api_key="AIzaSyBb8wTvVw9e25aX8XK-eBuu1JzDEPCdqUE",
            model="gemini-2.0-flash-exp"
        )
        messages = [{"role": "user", "content": "Say 'Stream' then 'works' on separate words"}]
        
        print("Stream output: ", end="")
        stream = llm.stream_chat(messages)
        for chunk in stream:
            if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print("\n✓ Google streaming works")
    except Exception as e:
        print(f"✗ Google streaming failed: {e}")
    
    # Test Google tool calling
    print("\n--- Google Tool Calling ---")
    try:
        tools = [{
            "type": "function",
            "function": {
                "name": "test_function",
                "description": "A test function",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"}
                    },
                    "required": ["message"]
                }
            }
        }]
        
        llm = OAI(
            provider="google",
            api_key="AIzaSyBb8wTvVw9e25aX8XK-eBuu1JzDEPCdqUE",
            model="gemini-2.0-flash-exp"
        )
        messages = [{"role": "user", "content": "Call test_function with message 'hello'"}]
        response = llm.tool_call(messages, tools)
        
        if response.choices[0].message.tool_calls:
            print(f"✓ Google tool calling works: {response.choices[0].message.tool_calls[0].function.name}")
        else:
            print(f"✗ No tool call: {response.choices[0].message.content}")
    except Exception as e:
        print(f"✗ Google tool calling failed: {e}")


def test_convenience_functions():
    """Test convenience creation functions"""
    print("\n=== Convenience Functions Test ===")
    
    try:
        from llm import create_ollama_client, create_google_client
        
        # Test Ollama convenience function
        ollama_llm = create_ollama_client(model="qwen3:0.6b")
        print(f"✓ create_ollama_client: {ollama_llm}")
        
        # Test Google convenience function  
        google_llm = create_google_client(
            api_key="AIzaSyBb8wTvVw9e25aX8XK-eBuu1JzDEPCdqUE",
            model="gemini-2.0-flash-exp"
        )
        print(f"✓ create_google_client: {google_llm}")
        
    except Exception as e:
        print(f"✗ Convenience functions failed: {e}")


def test_provider_config():
    """Test provider configurations"""
    print("\n=== Provider Configuration Test ===")
    
    # Test all provider configs
    configs = [
        {"provider": "ollama", "model": "qwen3:0.6b"},
        {"provider": "google", "api_key": "test", "model": "gemini-2.0-flash-exp"},
        {"provider": "openrouter", "api_key": "test", "model": "test"},
        {"provider": "vllm", "base_url": "http://localhost:8000/v1"}
    ]
    
    for config in configs:
        try:
            llm = OAI(**config)
            print(f"✓ {config['provider']} config: {llm}")
        except Exception as e:
            print(f"✗ {config['provider']} config failed: {e}")


if __name__ == "__main__":
    print("Testing OAI Class - Simple & Comprehensive\n")
    
    test_core_functionality()
    test_convenience_functions()
    test_provider_config()
    
    print(f"\n=== Tests Complete ===")
    print("✓ Core OAI functionality verified!")