from ._files import FilesystemTools
from .__files_advanced import ClaudeTools
from .__web import WebSearchTool
import asyncio

_fs_tools = FilesystemTools()
_claude_tools = ClaudeTools()
_web_tools = WebSearchTool()

basic_filsystem_tools = [
    _fs_tools.read_file,
    _fs_tools.write_file,
    _fs_tools.list_directory,
    _fs_tools.create_directory,
    _fs_tools.copy_file,
    _fs_tools.move_file,
    _fs_tools.search_files,
    _fs_tools.get_file_info,
    _fs_tools.list_allowed_directories,
    _fs_tools.read_multiple_files,
    _fs_tools.tree,
    _fs_tools.delete_file,
    _fs_tools.modify_file,
    _fs_tools.search_within_files,
    _fs_tools.handle_read_resource
]

# Direct access to ClaudeTools methods
claude_tools = _claude_tools

# Tools dictionary for easy access
tools_dict = {
    'read_file': _claude_tools.read.read_file,
    'write_file': _claude_tools.write.write_file,
    'edit_file': _claude_tools.edit.edit_file,
    'apply_edit': _claude_tools.edit.apply_pending_edit,
    'discard_edit': _claude_tools.edit.discard_pending_edit,
    'multi_edit_file': _claude_tools.multiedit.multi_edit_file,
    'bash_execute': _claude_tools.bash.execute,
    'glob_find_files': _claude_tools.glob.find_files,
    'grep_search': _claude_tools.grep.search,
    'list_directory': _claude_tools.ls.list_directory,
    # 'read_notebook': _claude_tools.notebook_read.read_notebook,
    # 'edit_notebook_cell': _claude_tools.notebook_edit.edit_cell,
    'fetch_url': _claude_tools.web_fetch.fetch_url,
    'web_search': _web_tools.web_search,
    'todo_read': _claude_tools.todo_read.todo_read,
    'todo_write': _claude_tools.todo_write.todo_write,
    # 'task_execute': _claude_tools.task.task_execute
}

# Tool schemas for LLM integration (OpenAI-compatible)
try:
    from .tool_schemas import get_tool_schemas
    tools = get_tool_schemas()
except ImportError as e:
    print(f"Warning: Could not import tool schemas: {e}")
    # Fallback to empty list
    tools = []