#!/usr/bin/env python3
"""
Tool schema generation for OpenAI-compatible function calling
"""

from __future__ import annotations

import inspect
import re
from collections import defaultdict
from typing import Callable, Union, Dict, Any, List

def _parse_docstring(doc_string: Union[str, None]) -> dict[str, str]:
    """Parse function docstring to extract parameter descriptions"""
    parsed_docstring = defaultdict(str)
    if not doc_string:
        return parsed_docstring

    key = str(hash(doc_string))
    for line in doc_string.splitlines():
        lowered_line = line.lower().strip()
        if lowered_line.startswith('args:'):
            key = 'args'
        elif lowered_line.startswith(('returns:', 'yields:', 'raises:')):
            key = '_'
        else:
            parsed_docstring[key] += f'{line.strip()}\n'

    last_key = None
    for line in parsed_docstring['args'].splitlines():
        line = line.strip()
        if ':' in line:
            # Split the line on either:
            # 1. A parenthetical expression like (integer) - captured in group 1
            # 2. A colon :
            # Followed by optional whitespace. Only split on first occurrence.
            parts = re.split(r'(?:\(([^)]*)\)|:)\s*', line, maxsplit=1)

            arg_name = parts[0].strip()
            last_key = arg_name

            # Get the description - will be in parts[1] if parenthetical or parts[-1] if after colon
            arg_description = parts[-1].strip()
            if len(parts) > 2 and parts[1]:  # Has parenthetical content
                arg_description = parts[-1].split(':', 1)[-1].strip()

            parsed_docstring[last_key] = arg_description

        elif last_key and line:
            parsed_docstring[last_key] += ' ' + line

    return parsed_docstring

def convert_function_to_tool_schema(func: Callable) -> Dict[str, Any]:
    """Convert a Python function to OpenAI-compatible tool schema"""
    doc_string_hash = str(hash(inspect.getdoc(func)))
    parsed_docstring = _parse_docstring(inspect.getdoc(func))
    
    # Get function signature
    sig = inspect.signature(func)
    
    # Build properties from function parameters
    properties = {}
    required = []
    
    for param_name, param in sig.parameters.items():
        if param_name == 'self':  # Skip self parameter
            continue
            
        # Determine parameter type
        param_type = "string"  # Default
        param_schema = {
            "type": param_type,
            "description": parsed_docstring.get(param_name, f"Parameter {param_name}")
        }
        
        if param.annotation != inspect.Parameter.empty:
            if param.annotation in (int, float):
                param_schema["type"] = "number"
            elif param.annotation == bool:
                param_schema["type"] = "boolean"
            elif hasattr(param.annotation, '__origin__'):
                # Handle List, Dict, etc.
                if param.annotation.__origin__ == list:
                    param_schema["type"] = "array"
                    # Add items field for Google compatibility
                    param_schema["items"] = {"type": "string"}  # Default to string items
                    # Try to get the item type from type annotations
                    if hasattr(param.annotation, '__args__') and param.annotation.__args__:
                        item_type = param.annotation.__args__[0]
                        if item_type == int:
                            param_schema["items"]["type"] = "number"
                        elif item_type == bool:
                            param_schema["items"]["type"] = "boolean"
                elif param.annotation.__origin__ == dict:
                    param_schema["type"] = "object"
        
        properties[param_name] = param_schema
        
        # Add to required if no default value
        if param.default == inspect.Parameter.empty:
            required.append(param_name)
    
    # Build tool schema
    tool_schema = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": parsed_docstring.get(doc_string_hash, f"Execute {func.__name__}").strip(),
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }
    
    return tool_schema

def generate_tool_schemas_from_tools_dict(tools_dict: Dict[str, Callable]) -> List[Dict[str, Any]]:
    """Generate OpenAI-compatible tool schemas from tools dictionary"""
    schemas = []
    
    for tool_name, tool_func in tools_dict.items():
        try:
            schema = convert_function_to_tool_schema(tool_func)
            schemas.append(schema)
        except Exception as e:
            print(f"Error generating schema for {tool_name}: {e}")
            # Create a basic schema as fallback
            schemas.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": f"Execute {tool_name}",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            })
    
    return schemas

# Predefined schemas for common tools
PREDEFINED_TOOL_SCHEMAS = {
    "read_file": {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    "write_file": {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    }
                },
                "required": ["file_path", "content"]
            }
        }
    },
    "edit_file": {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Edit a file by replacing text",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to edit"
                    },
                    "old_string": {
                        "type": "string",
                        "description": "Text to replace"
                    },
                    "new_string": {
                        "type": "string",
                        "description": "New text to replace with"
                    }
                },
                "required": ["file_path", "old_string", "new_string"]
            }
        }
    },
    "bash_execute": {
        "type": "function",
        "function": {
            "name": "bash_execute",
            "description": "Execute a bash command",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Bash command to execute"
                    }
                },
                "required": ["command"]
            }
        }
    },
    "list_directory": {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List contents of a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the directory to list"
                    }
                },
                "required": ["path"]
            }
        }
    },
    "glob_find_files": {
        "type": "function",
        "function": {
            "name": "glob_find_files",
            "description": "Find files matching a pattern",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Glob pattern to match files"
                    },
                    "path": {
                        "type": "string",
                        "description": "Directory to search in"
                    }
                },
                "required": ["pattern"]
            }
        }
    },
    "grep_search": {
        "type": "function",
        "function": {
            "name": "grep_search",
            "description": "Search for text patterns in files",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Regular expression pattern to search for"
                    },
                    "path": {
                        "type": "string",
                        "description": "Directory to search in"
                    }
                },
                "required": ["pattern"]
            }
        }
    },
    "fetch_url": {
        "type": "function",
        "function": {
            "name": "fetch_url",
            "description": "Fetch content from a URL and optionally process it with a prompt",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to fetch content from"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Optional prompt to process the fetched content"
                    }
                },
                "required": ["url"]
            }
        }
    },
    "todo_read": {
        "type": "function",
        "function": {
            "name": "todo_read",
            "description": "Read the current todo list",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    "todo_write": {
        "type": "function",
        "function": {
            "name": "todo_write",
            "description": "Create and manage structured task lists with priorities and status tracking",
            "parameters": {
                "type": "object",
                "properties": {
                    "todos": {
                        "type": "array",
                        "description": "Array of todo items with content, status, priority, and id",
                        "items": {
                            "type": "object",
                            "properties": {
                                "content": {
                                    "type": "string",
                                    "description": "Todo item description"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status of the todo item",
                                    "enum": ["pending", "in_progress", "completed"]
                                },
                                "priority": {
                                    "type": "string",
                                    "description": "Priority level of the todo item",
                                    "enum": ["low", "medium", "high"]
                                },
                                "id": {
                                    "type": "string",
                                    "description": "Unique identifier for the todo item"
                                }
                            },
                            "required": ["content", "status", "priority", "id"]
                        }
                    }
                },
                "required": ["todos"]
            }
        }
    }
}

def get_tool_schemas() -> List[Dict[str, Any]]:
    """Get list of tool schemas for LLM"""
    try:
        from claude.tools import tools_dict
        
        # Use predefined schemas for known tools, auto-generate for others
        schemas = []
        for tool_name, tool_func in tools_dict.items():
            if tool_name in PREDEFINED_TOOL_SCHEMAS:
                schemas.append(PREDEFINED_TOOL_SCHEMAS[tool_name])
            else:
                try:
                    schema = convert_function_to_tool_schema(tool_func)
                    schemas.append(schema)
                except Exception as e:
                    print(f"Warning: Could not generate schema for {tool_name}: {e}")
        
        return schemas
    except ImportError:
        print("Warning: Could not import tools_dict, using predefined schemas only")
        return list(PREDEFINED_TOOL_SCHEMAS.values())