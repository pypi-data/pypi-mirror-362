import inspect
import re
from collections import defaultdict
from typing import Union, Callable, Any, Dict


def _parse_docstring(doc_string: Union[str, None]) -> dict[str, str]:
    """Parse docstring to extract function description and parameter descriptions."""
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
            parts = re.split(r'(?:\(([^)]*)\)|:)\s*', line, maxsplit=1)
            arg_name = parts[0].strip()
            last_key = arg_name
            arg_description = parts[-1].strip()
            if len(parts) > 2 and parts[1]:
                arg_description = parts[-1].split(':', 1)[-1].strip()
            parsed_docstring[last_key] = arg_description
        elif last_key and line:
            parsed_docstring[last_key] += ' ' + line

    return parsed_docstring


def convert_function_to_tool(func: Callable) -> Dict[str, Any]:
    """Convert a Python function to OpenAI tool format for vLLM."""
    doc_string_hash = str(hash(inspect.getdoc(func)))
    parsed_docstring = _parse_docstring(inspect.getdoc(func))

    # Get function signature
    sig = inspect.signature(func)

    # Build JSON schema for parameters
    properties = {}
    required = []

    for param_name, param in sig.parameters.items():
        param_type = "string"  # default type

        # Try to infer type from annotation
        if param.annotation != inspect._empty:
            if param.annotation == int:
                param_type = "integer"
            elif param.annotation == float:
                param_type = "number"
            elif param.annotation == bool:
                param_type = "boolean"
            elif param.annotation == list:
                param_type = "array"
            elif param.annotation == dict:
                param_type = "object"

        properties[param_name] = {
            "type": param_type,
            "description": parsed_docstring.get(param_name, "")
        }

        # If parameter has no default, it's required
        if param.default == inspect._empty:
            required.append(param_name)

    tool = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": parsed_docstring.get(doc_string_hash, "").strip(),
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }

    return tool

