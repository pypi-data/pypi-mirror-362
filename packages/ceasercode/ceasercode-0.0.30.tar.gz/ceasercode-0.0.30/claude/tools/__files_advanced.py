#!/usr/bin/env python3
"""
Claude Code Python Tools Implementation

This module implements the core tools for file operations, command execution,
and other utilities similar to those found in Claude Desktop/MCP servers.

Based on the TypeScript implementation found in claude-code, this provides:
- Task: Launch agents for complex operations  
- Bash: Execute shell commands safely
- Glob: Fast file pattern matching
- Grep: Content search with regex
- LS: List directory contents
- Read: Read file contents with various formats
- Edit: Make string replacements in files
- MultiEdit: Multiple edits in one operation
- Write: Create/overwrite files
- NotebookRead/Edit: Jupyter notebook support
- WebFetch: Fetch web content
- TodoRead/Write: Task management
"""

import asyncio
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
import fnmatch
import glob as python_glob
import tempfile
import urllib.request
import urllib.parse
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable, AsyncIterator, Iterator
from urllib.parse import urlencode, parse_qs

import aiohttp
import aiofiles


# ============================================================================
# CORE TYPES AND EXCEPTIONS
# ============================================================================

class ToolError(Exception):
    """Base exception for tool operations"""
    def __init__(self, message: str, category: str = "general", resolution: str = None):
        super().__init__(message)
        self.category = category
        self.resolution = resolution


class ValidationError(ToolError):
    """Validation error for tool inputs"""
    def __init__(self, message: str, resolution: str = None):
        super().__init__(message, "validation", resolution)


class FileSystemError(ToolError):
    """File system operation error"""
    def __init__(self, message: str, resolution: str = None):
        super().__init__(message, "filesystem", resolution)


class ExecutionError(ToolError):
    """Command execution error"""
    def __init__(self, message: str, resolution: str = None):
        super().__init__(message, "execution", resolution)


@dataclass
class FileInfo:
    """Information about a file or directory"""
    path: str
    name: str
    size: int
    is_file: bool
    is_directory: bool
    modified_time: float
    permissions: str


@dataclass
class ExecutionResult:
    """Result of command execution"""
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration: float
    success: bool


@dataclass
class SearchResult:
    """Result of content search"""
    file_path: str
    line_number: int
    line_content: str
    match_start: int
    match_end: int


@dataclass
class TodoItem:
    """Todo list item"""
    id: str
    content: str
    status: str = 'pending'  # 'pending', 'in_progress', 'completed'
    priority: str = 'medium'  # 'low', 'medium', 'high'
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


# ============================================================================
# LOGGING SETUP
# ============================================================================

class ToolLogger:
    """Simple logger for tool operations"""
    
    def __init__(self, level: str = "INFO"):
        self.level = getattr(logging, level.upper(), logging.INFO)
        logging.basicConfig(
            level=self.level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('claude-tools')
    
    def debug(self, message: str, **kwargs):
        if kwargs:
            message += f" {kwargs}"
        # self.logger.debug(message)
    
    def info(self, message: str, **kwargs):
        if kwargs:
            message += f" {kwargs}"
        # self.logger.info(message)
    
    def warn(self, message: str, **kwargs):
        if kwargs:
            message += f" {kwargs}"
        self.logger.warning(message)
    
    def error(self, message: str, **kwargs):
        if kwargs:
            message += f" {kwargs}"
        self.logger.error(message)


logger = ToolLogger()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_path(path: str) -> str:
    """Validate and normalize a file path"""
    if not path:
        raise ValidationError("Path cannot be empty")
    
    # Resolve path and check for directory traversal
    try:
        normalized = os.path.normpath(path)
        if ".." in normalized.split(os.sep):
            raise ValidationError("Path contains directory traversal")
        return normalized
    except Exception as e:
        raise ValidationError(f"Invalid path: {path}") from e


def is_safe_command(command: str) -> bool:
    """Check if a command is safe to execute"""
    dangerous_patterns = [
        r'rm\s+-rf?\s+/',  # rm -rf /
        r'dd\s+.*of=/dev/',  # dd to device
        r'mkfs',  # format filesystem
        r':\(\)\{.*\}',  # fork bomb
        r'sudo.*rm',  # sudo rm
        r'>\s*/dev/',  # redirect to device
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return False
    return True


def get_file_type(file_path: str) -> str:
    """Get file type based on extension"""
    ext = Path(file_path).suffix.lower()
    type_map = {
        '.py': 'python',
        '.js': 'javascript', 
        '.ts': 'typescript',
        '.json': 'json',
        '.md': 'markdown',
        '.txt': 'text',
        '.csv': 'csv',
        '.html': 'html',
        '.css': 'css',
        '.ipynb': 'notebook'
    }
    return type_map.get(ext, 'unknown')


# ============================================================================
# TASK AGENT
# ============================================================================

class TaskAgent:
    """
    Agent for launching complex searches and file operations.
    This provides a high-level interface for coordinating multiple tools.
    """
    
    def __init__(self):
        self.tools = {
            'bash': BashTool(),
            'glob': GlobTool(), 
            'grep': GrepTool(),
            'ls': LSTool(),
            'read': ReadTool(),
            'edit': EditTool(),
            'multiedit': MultiEditTool(),
            'write': WriteTool()
        }
    
    async def task_execute(self, description: str, instructions: str) -> Dict[str, Any]:
        """Execute a complex task with multiple steps"""
        logger.info(f"Executing task: {description}")
        
        results = {
            'task_description': description,
            'instructions': instructions,
            'steps': [],
            'final_result': None,
            'success': False
        }
        
        try:
            # Parse instructions and execute steps
            # This is a simplified implementation - in practice, you'd have
            # more sophisticated task parsing and execution
            
            steps = self._parse_instructions(instructions)
            
            for i, step in enumerate(steps):
                logger.info(f"Executing step {i+1}: {step['action']}")
                
                step_result = await self._execute_step(step)
                results['steps'].append({
                    'step_number': i + 1,
                    'action': step['action'],
                    'result': step_result
                })
                
                if not step_result.get('success', False):
                    results['error'] = f"Step {i+1} failed: {step_result.get('error', 'Unknown error')}"
                    return results
            
            results['success'] = True
            results['final_result'] = "Task completed successfully"
            
        except Exception as e:
            results['error'] = str(e)
            logger.error(f"Task execution failed: {e}")
        
        return results
    
    def _parse_instructions(self, instructions: str) -> List[Dict[str, Any]]:
        """Parse task instructions into executable steps"""
        # Simplified parsing - look for common patterns
        steps = []
        
        if "search for" in instructions.lower():
            # Extract search terms
            match = re.search(r"search for ['\"]([^'\"]+)['\"]", instructions, re.IGNORECASE)
            if match:
                term = match.group(1)
                steps.append({
                    'action': 'search',
                    'tool': 'grep',
                    'params': {'pattern': term, 'path': '.'}
                })
        
        if "find files" in instructions.lower():
            # Extract file patterns
            match = re.search(r"find files.*['\"]([^'\"]+)['\"]", instructions, re.IGNORECASE)
            if match:
                pattern = match.group(1)
                steps.append({
                    'action': 'find_files',
                    'tool': 'glob',
                    'params': {'pattern': pattern}
                })
        
        if "read file" in instructions.lower():
            # Extract file path
            match = re.search(r"read file ['\"]([^'\"]+)['\"]", instructions, re.IGNORECASE)
            if match:
                file_path = match.group(1)
                steps.append({
                    'action': 'read_file',
                    'tool': 'read',
                    'params': {'file_path': file_path}
                })
        
        return steps
    
    async def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step in the task"""
        tool_name = step['tool']
        action = step['action']
        params = step['params']
        
        if tool_name not in self.tools:
            return {'success': False, 'error': f"Unknown tool: {tool_name}"}
        
        tool = self.tools[tool_name]
        
        try:
            if action == 'search':
                result = await tool.search(**params)
            elif action == 'find_files':
                result = await tool.find_files(**params)
            elif action == 'read_file':
                result = await tool.read_file(**params)
            else:
                return {'success': False, 'error': f"Unknown action: {action}"}
            
            return {'success': True, 'result': result}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}


# ============================================================================
# BASH TOOL
# ============================================================================

class BashTool:
    """Execute shell commands with security measures"""
    
    def __init__(self, timeout: float = 30.0, max_output_size: int = 1024 * 1024):
        self.timeout = timeout
        self.max_output_size = max_output_size
    
    async def execute(self, command: str, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None) -> ExecutionResult:
        """Execute a shell command safely"""
        logger.info(f"Executing command: {command}")
        
        # Validate command safety
        if not is_safe_command(command):
            raise ExecutionError(
                f"Dangerous command blocked: {command}",
                "This command is blocked for safety reasons"
            )
        
        start_time = time.time()
        
        try:
            # Prepare environment
            exec_env = os.environ.copy()
            if env:
                exec_env.update(env)
            
            # Execute command
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                env=exec_env
            )
            
            # Wait for completion with timeout
            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=self.timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                raise ExecutionError(
                    f"Command timed out after {self.timeout} seconds",
                    "Try reducing the scope or increasing timeout"
                )
            
            # Decode output
            stdout = stdout_bytes.decode('utf-8', errors='replace')
            stderr = stderr_bytes.decode('utf-8', errors='replace')
            
            # Check output size
            if len(stdout) + len(stderr) > self.max_output_size:
                stdout = stdout[:self.max_output_size // 2] + "\n... (output truncated)"
                stderr = stderr[:self.max_output_size // 2] + "\n... (output truncated)"
            
            duration = time.time() - start_time
            
            result = ExecutionResult(
                command=command,
                exit_code=process.returncode,
                stdout=stdout,
                stderr=stderr,
                duration=duration,
                success=process.returncode == 0
            )
            
            logger.info(f"Command completed with exit code {process.returncode}")
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Command execution failed: {e}")
            
            return ExecutionResult(
                command=command,
                exit_code=-1,
                stdout="",
                stderr=str(e),
                duration=duration,
                success=False
            )


# ============================================================================
# GLOB TOOL
# ============================================================================

class GlobTool:
    """Fast file pattern matching"""
    
    def __init__(self):
        pass
    
    async def find_files(self, pattern: str, path: str = ".", recursive: bool = True) -> List[str]:
        """Find files matching a glob pattern"""
        logger.info(f"Finding files with pattern: {pattern} in {path}")
        
        try:
            validated_path = validate_path(path)
            
            if recursive:
                # Use ** for recursive search
                if not pattern.startswith('**/'):
                    pattern = f"**/{pattern}"
                
                search_pattern = os.path.join(validated_path, pattern)
                matches = python_glob.glob(search_pattern, recursive=True)
            else:
                search_pattern = os.path.join(validated_path, pattern)
                matches = python_glob.glob(search_pattern)
            
            # Filter to only files (not directories)
            files = [m for m in matches if os.path.isfile(m)]
            
            # Sort by modification time (newest first)
            files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            
            logger.info(f"Found {len(files)} files matching pattern")
            return files
            
        except Exception as e:
            logger.error(f"Glob search failed: {e}")
            raise FileSystemError(f"Failed to search for files: {e}")
    
    async def find_patterns(self, patterns: List[str], path: str = ".") -> Dict[str, List[str]]:
        """Find files matching multiple patterns"""
        results = {}
        
        for pattern in patterns:
            try:
                files = await self.find_files(pattern, path)
                results[pattern] = files
            except Exception as e:
                results[pattern] = []
                logger.error(f"Pattern {pattern} failed: {e}")
        
        return results


# ============================================================================
# GREP TOOL 
# ============================================================================

class GrepTool:
    """Fast content search using regex patterns"""
    
    def __init__(self, max_file_size: int = 10 * 1024 * 1024):  # 10MB
        self.max_file_size = max_file_size
    
    async def search(
        self, 
        pattern: str, 
        path: str = ".", 
        file_pattern: str = "*",
        case_sensitive: bool = False,
        max_results: int = 1000
    ) -> List[SearchResult]:
        """Search for pattern in files"""
        logger.info(f"Searching for pattern: {pattern} in {path}")
        
        try:
            # Compile regex pattern
            flags = 0 if case_sensitive else re.IGNORECASE
            regex = re.compile(pattern, flags)
            
            # Find files to search
            glob_tool = GlobTool()
            files = await glob_tool.find_files(file_pattern, path)
            
            results = []
            
            for file_path in files:
                if len(results) >= max_results:
                    break
                
                try:
                    # Check file size
                    if os.path.getsize(file_path) > self.max_file_size:
                        logger.warn(f"Skipping large file: {file_path}")
                        continue
                    
                    # Search in file
                    file_results = await self._search_file(file_path, regex)
                    results.extend(file_results)
                    
                except Exception as e:
                    logger.error(f"Error searching file {file_path}: {e}")
                    continue
            
            logger.info(f"Found {len(results)} matches")
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise ToolError(f"Search failed: {e}")
    
    async def _search_file(self, file_path: str, regex: re.Pattern) -> List[SearchResult]:
        """Search for pattern in a single file"""
        results = []
        
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                line_number = 0
                async for line in f:
                    line_number += 1
                    
                    for match in regex.finditer(line):
                        results.append(SearchResult(
                            file_path=file_path,
                            line_number=line_number,
                            line_content=line.rstrip('\n\r'),
                            match_start=match.start(),
                            match_end=match.end()
                        ))
        
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
        
        return results


# ============================================================================
# LS TOOL
# ============================================================================

class LSTool:
    """List files and directories"""
    
    def __init__(self):
        pass
    
    async def list_directory(
        self, 
        path: str = ".", 
        show_hidden: bool = False,
        recursive: bool = False,
        ignore_patterns: Optional[List[str]] = None
    ) -> List[FileInfo]:
        """List directory contents"""
        logger.info(f"Listing directory: {path}")
        
        try:
            validated_path = validate_path(path)
            
            if not os.path.exists(validated_path):
                raise FileSystemError(f"Path does not exist: {path}")
            
            if not os.path.isdir(validated_path):
                raise FileSystemError(f"Path is not a directory: {path}")
            
            ignore_patterns = ignore_patterns or ['.git', '__pycache__', '*.pyc', '.DS_Store']
            
            files = []
            
            if recursive:
                for root, dirs, filenames in os.walk(validated_path):
                    # Filter directories
                    dirs[:] = [d for d in dirs if not self._should_ignore(d, ignore_patterns)]
                    
                    for name in filenames:
                        if not show_hidden and name.startswith('.'):
                            continue
                        
                        if self._should_ignore(name, ignore_patterns):
                            continue
                        
                        full_path = os.path.join(root, name)
                        file_info = await self._get_file_info(full_path)
                        if file_info:
                            files.append(file_info)
            else:
                for item in os.listdir(validated_path):
                    if not show_hidden and item.startswith('.'):
                        continue
                    
                    if self._should_ignore(item, ignore_patterns):
                        continue
                    
                    full_path = os.path.join(validated_path, item)
                    file_info = await self._get_file_info(full_path)
                    if file_info:
                        files.append(file_info)
            
            # Sort by name
            files.sort(key=lambda x: x.name.lower())
            
            # logger.info(f"Listed {len(files)} items")
            return files
            
        except Exception as e:
            logger.error(f"Directory listing failed: {e}")
            raise FileSystemError(f"Failed to list directory: {e}")
    
    def _should_ignore(self, name: str, patterns: List[str]) -> bool:
        """Check if file should be ignored based on patterns"""
        for pattern in patterns:
            if fnmatch.fnmatch(name, pattern):
                return True
        return False
    
    async def _get_file_info(self, file_path: str) -> Optional[FileInfo]:
        """Get information about a file"""
        try:
            stat = os.stat(file_path)
            
            return FileInfo(
                path=file_path,
                name=os.path.basename(file_path),
                size=stat.st_size,
                is_file=os.path.isfile(file_path),
                is_directory=os.path.isdir(file_path),
                modified_time=stat.st_mtime,
                permissions=oct(stat.st_mode)[-3:]
            )
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {e}")
            return None


# ============================================================================
# READ TOOL
# ============================================================================

class ReadTool:
    """Read file contents with various format support"""
    
    def __init__(self, max_file_size: int = 50 * 1024 * 1024):  # 50MB
        self.max_file_size = max_file_size
    
    async def read_file(
        self, 
        file_path: str, 
        encoding: str = 'utf-8',
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Read file contents"""
        logger.info(f"Reading file: {file_path}")
        
        try:
            validated_path = validate_path(file_path)
            
            if not os.path.exists(validated_path):
                raise FileSystemError(f"File does not exist: {file_path}")
            
            if not os.path.isfile(validated_path):
                raise FileSystemError(f"Path is not a file: {file_path}")
            
            # Check file size
            file_size = os.path.getsize(validated_path)
            if file_size > self.max_file_size:
                raise FileSystemError(
                    f"File too large: {file_size} bytes", 
                    "Try reading a smaller file or use offset/limit parameters"
                )
            
            file_type = get_file_type(validated_path)
            
            # Handle different file types
            if file_type == 'notebook':
                return await self._read_notebook(validated_path)
            elif file_type == 'json':
                return await self._read_json(validated_path)
            else:
                return await self._read_text_file(validated_path, encoding, offset, limit)
                
        except Exception as e:
            logger.error(f"File reading failed: {e}")
            raise FileSystemError(f"Failed to read file: {e}")
    
    async def _read_text_file(self, file_path: str, encoding: str, offset: int, limit: int) -> Dict[str, Any]:
        """Read text file with optional offset and limit"""
        try:
            async with aiofiles.open(file_path, 'r', encoding=encoding, errors='replace') as f:
                content = await f.read()
            
            lines = content.split('\n')
            
            # Apply offset and limit
            if offset is not None or limit is not None:
                start = offset or 0
                end = (start + limit) if limit else len(lines)
                lines = lines[start:end]
                content = '\n'.join(lines)
            
            return {
                'type': 'text',
                'content': content,
                'lines': len(lines),
                'size': len(content),
                'encoding': encoding
            }
            
        except UnicodeDecodeError as e:
            # Try binary read for non-text files
            logger.warn(f"Unicode decode error, trying binary read: {e}")
            return await self._read_binary_file(file_path)
    
    async def _read_binary_file(self, file_path: str) -> Dict[str, Any]:
        """Read binary file and return hex representation"""
        async with aiofiles.open(file_path, 'rb') as f:
            data = await f.read()
        
        # Limit binary display
        if len(data) > 1024:
            data = data[:1024]
            truncated = True
        else:
            truncated = False
        
        hex_content = data.hex()
        
        return {
            'type': 'binary',
            'content': hex_content,
            'size': len(data),
            'truncated': truncated
        }
    
    async def _read_json(self, file_path: str) -> Dict[str, Any]:
        """Read and parse JSON file"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        try:
            parsed = json.loads(content)
            return {
                'type': 'json',
                'content': content,
                'parsed': parsed,
                'size': len(content)
            }
        except json.JSONDecodeError as e:
            return {
                'type': 'json',
                'content': content,
                'parse_error': str(e),
                'size': len(content)
            }
    
    async def _read_notebook(self, file_path: str) -> Dict[str, Any]:
        """Read Jupyter notebook file"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        try:
            notebook = json.loads(content)
            
            # Extract cell information
            cells = []
            for i, cell in enumerate(notebook.get('cells', [])):
                cells.append({
                    'index': i,
                    'cell_type': cell.get('cell_type', 'unknown'),
                    'source': ''.join(cell.get('source', [])),
                    'outputs': cell.get('outputs', [])
                })
            
            return {
                'type': 'notebook',
                'content': content,
                'cells': cells,
                'cell_count': len(cells),
                'size': len(content)
            }
            
        except json.JSONDecodeError as e:
            return {
                'type': 'notebook',
                'content': content,
                'parse_error': str(e),
                'size': len(content)
            }


# ============================================================================
# EDIT TOOL
# ============================================================================

class EditTool:
    """Make exact string replacements in files"""
    
    def __init__(self):
        self._pending_edit = None
    
    async def edit_file(
        self, 
        file_path: str, 
        old_string: str, 
        new_string: str,
        replace_all: bool = False
    ) -> Dict[str, Any]:
        """Edit file by replacing strings"""
        logger.info(f"Editing file: {file_path}")
        
        try:
            validated_path = validate_path(file_path)
            
            if not os.path.exists(validated_path):
                raise FileSystemError(f"File does not exist: {file_path}")
            
            # Read current content
            async with aiofiles.open(validated_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            original_content = content
            
            # Perform replacement
            if replace_all:
                new_content = content.replace(old_string, new_string)
                replacements = content.count(old_string)
            else:
                # Replace only first occurrence
                if old_string not in content:
                    raise ValidationError(f"String not found in file: {old_string}")
                
                # Check for multiple occurrences
                if content.count(old_string) > 1:
                    raise ValidationError(
                        f"Multiple occurrences of string found. Use replace_all=True or provide more context",
                        "Make the old_string more specific or use replace_all option"
                    )
                
                new_content = content.replace(old_string, new_string, 1)
                replacements = 1
            
            if replacements == 0:
                raise ValidationError(f"String not found in file: {old_string}")
            
            # Generate diff (but don't write file yet)
            diff = self._generate_diff(original_content, new_content, file_path)
            
            # Store the new content for later application
            self._pending_edit = {
                'file_path': validated_path,
                'new_content': new_content,
                'applied': False
            }
            
            logger.info(f"File edit prepared, {replacements} replacements ready")
            
            return {
                'success': True,
                'file_path': file_path,
                'replacements': replacements,
                'old_string': old_string,
                'new_string': new_string,
                'original_size': len(original_content),
                'new_size': len(new_content),
                'diff': diff,
                'pending_application': True
            }
            
        except Exception as e:
            logger.error(f"File editing failed: {e}")
            raise FileSystemError(f"Failed to edit file: {e}")
    
    def _generate_diff(self, original_content: str, new_content: str, file_path: str) -> str:
        """Generate unified diff between original and new content"""
        import difflib
        
        original_lines = original_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        diff_lines = list(difflib.unified_diff(
            original_lines,
            new_lines,
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
            lineterm=""
        ))
        
        return ''.join(diff_lines)
    
    async def preview_edit(
        self, 
        file_path: str, 
        old_string: str, 
        new_string: str,
        replace_all: bool = False
    ) -> Dict[str, Any]:
        """Preview what an edit would do without actually making changes"""
        logger.info(f"Previewing edit for file: {file_path}")
        
        try:
            validated_path = validate_path(file_path)
            
            if not os.path.exists(validated_path):
                raise FileSystemError(f"File does not exist: {file_path}")
            
            # Read current content
            async with aiofiles.open(validated_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            original_content = content
            
            # Perform replacement (in memory only)
            if replace_all:
                new_content = content.replace(old_string, new_string)
                replacements = content.count(old_string)
            else:
                # Replace only first occurrence
                if old_string not in content:
                    raise ValidationError(f"String not found in file: {old_string}")
                
                # Check for multiple occurrences
                if content.count(old_string) > 1:
                    raise ValidationError(
                        f"Multiple occurrences of string found. Use replace_all=True or provide more context",
                        "Make the old_string more specific or use replace_all option"
                    )
                
                new_content = content.replace(old_string, new_string, 1)
                replacements = 1
            
            if replacements == 0:
                raise ValidationError(f"String not found in file: {old_string}")
            
            # Generate diff (without writing)
            diff = self._generate_diff(original_content, new_content, file_path)
            
            return {
                'success': True,
                'file_path': file_path,
                'replacements': replacements,
                'old_string': old_string,
                'new_string': new_string,
                'original_size': len(original_content),
                'new_size': len(new_content),
                'diff': diff,
                'preview_only': True
            }
            
        except Exception as e:
            logger.error(f"Edit preview failed: {e}")
            raise FileSystemError(f"Failed to preview edit: {e}")
    
    async def apply_pending_edit(self) -> Dict[str, Any]:
        """Apply the pending edit to the file"""
        if not self._pending_edit or self._pending_edit.get('applied', False):
            raise ValidationError("No pending edit to apply")
        
        try:
            # Write the new content to file
            async with aiofiles.open(self._pending_edit['file_path'], 'w', encoding='utf-8') as f:
                await f.write(self._pending_edit['new_content'])
            
            self._pending_edit['applied'] = True
            logger.info(f"Pending edit applied to {self._pending_edit['file_path']}")
            
            return {
                'success': True,
                'file_path': self._pending_edit['file_path'],
                'applied': True
            }
            
        except Exception as e:
            logger.error(f"Failed to apply pending edit: {e}")
            raise FileSystemError(f"Failed to apply edit: {e}")
    
    async def discard_pending_edit(self) -> Dict[str, Any]:
        """Discard the pending edit without applying it"""
        if not self._pending_edit:
            raise ValidationError("No pending edit to discard")
        
        file_path = self._pending_edit['file_path']
        self._pending_edit = None
        logger.info(f"Pending edit discarded for {file_path}")
        
        return {
            'success': True,
            'file_path': file_path,
            'discarded': True
        }


# ============================================================================
# MULTI-EDIT TOOL
# ============================================================================

class MultiEditTool:
    """Make multiple edits to a single file in one operation"""
    
    def __init__(self):
        self.edit_tool = EditTool()
    
    async def multi_edit_file(
        self, 
        file_path: str, 
        edits: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Apply multiple edits to a file atomically"""
        logger.info(f"Multi-editing file: {file_path} with {len(edits)} edits")
        
        try:
            validated_path = validate_path(file_path)
            
            if not os.path.exists(validated_path):
                raise FileSystemError(f"File does not exist: {file_path}")
            
            # Read original content
            async with aiofiles.open(validated_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            original_content = content
            current_content = content
            edit_results = []
            
            # Apply edits sequentially
            for i, edit in enumerate(edits):
                old_string = edit.get('old_string')
                new_string = edit.get('new_string')
                replace_all = edit.get('replace_all', False)
                
                if not old_string or new_string is None:
                    raise ValidationError(f"Edit {i+1}: old_string and new_string are required")
                
                if old_string == new_string:
                    raise ValidationError(f"Edit {i+1}: old_string and new_string cannot be the same")
                
                # Check if old_string exists in current content
                if old_string not in current_content:
                    raise ValidationError(f"Edit {i+1}: String not found: {old_string}")
                
                # Apply replacement
                if replace_all:
                    new_content = current_content.replace(old_string, new_string)
                    replacements = current_content.count(old_string)
                else:
                    # Check for multiple occurrences unless replace_all is True
                    if current_content.count(old_string) > 1:
                        raise ValidationError(
                            f"Edit {i+1}: Multiple occurrences found. Use replace_all=True or provide more context"
                        )
                    
                    new_content = current_content.replace(old_string, new_string, 1)
                    replacements = 1
                
                current_content = new_content
                
                edit_results.append({
                    'edit_number': i + 1,
                    'old_string': old_string,
                    'new_string': new_string,
                    'replacements': replacements,
                    'success': True
                })
            
            # Write the final content
            async with aiofiles.open(validated_path, 'w', encoding='utf-8') as f:
                await f.write(current_content)
            
            logger.info(f"Multi-edit completed successfully, {len(edits)} edits applied")
            
            return {
                'success': True,
                'file_path': file_path,
                'total_edits': len(edits),
                'edit_results': edit_results,
                'original_size': len(original_content),
                'new_size': len(current_content)
            }
            
        except Exception as e:
            logger.error(f"Multi-edit failed: {e}")
            raise FileSystemError(f"Failed to multi-edit file: {e}")


# ============================================================================
# WRITE TOOL
# ============================================================================

class WriteTool:
    """Write new files or overwrite existing ones"""
    
    def __init__(self):
        pass
    
    async def write_file(
        self, 
        file_path: str, 
        content: str,
        encoding: str = 'utf-8',
        create_directories: bool = True,
        overwrite: bool = True
    ) -> Dict[str, Any]:
        """Write content to a file"""
        logger.info(f"Writing file: {file_path}")
        
        try:
            validated_path = validate_path(file_path)
            
            # Check if file exists and overwrite is False
            if os.path.exists(validated_path) and not overwrite:
                raise FileSystemError(
                    f"File already exists: {file_path}",
                    "Use overwrite=True to replace existing file"
                )
            
            # Create directories if needed
            if create_directories:
                dir_path = os.path.dirname(validated_path)
                if dir_path and not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                    logger.info(f"Created directory: {dir_path}")
            
            # Write file
            async with aiofiles.open(validated_path, 'w', encoding=encoding) as f:
                await f.write(content)
            
            # Get file info
            file_size = len(content.encode(encoding))
            line_count = content.count('\n') + 1 if content else 0
            
            logger.info(f"File written successfully: {file_size} bytes, {line_count} lines")
            
            return {
                'success': True,
                'file_path': file_path,
                'size': file_size,
                'lines': line_count,
                'encoding': encoding,
                'created_new': not os.path.exists(validated_path)
            }
            
        except Exception as e:
            logger.error(f"File writing failed: {e}")
            raise FileSystemError(f"Failed to write file: {e}")


# ============================================================================
# NOTEBOOK TOOLS
# ============================================================================

class NotebookReadTool:
    """Read Jupyter notebook files"""
    
    def __init__(self):
        self.read_tool = ReadTool()
    
    async def read_notebook(self, notebook_path: str) -> Dict[str, Any]:
        """Read Jupyter notebook and return structured data"""
        logger.info(f"Reading notebook: {notebook_path}")
        
        result = await self.read_tool.read_file(notebook_path)
        
        if result['type'] != 'notebook':
            raise ValidationError("File is not a Jupyter notebook")
        
        return result


class NotebookEditTool:
    """Edit Jupyter notebook cells"""
    
    def __init__(self):
        pass
    
    async def edit_cell(
        self,
        notebook_path: str,
        cell_number: int,
        new_source: str,
        cell_type: str = 'code',
        edit_mode: str = 'replace'
    ) -> Dict[str, Any]:
        """Edit a specific cell in a Jupyter notebook"""
        logger.info(f"Editing notebook cell: {notebook_path} cell {cell_number}")
        
        try:
            validated_path = validate_path(notebook_path)
            
            # Read notebook
            async with aiofiles.open(validated_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            notebook = json.loads(content)
            cells = notebook.get('cells', [])
            
            if edit_mode == 'insert':
                # Insert new cell
                new_cell = {
                    'cell_type': cell_type,
                    'source': new_source.split('\n'),
                    'metadata': {}
                }
                
                if cell_type == 'code':
                    new_cell['outputs'] = []
                    new_cell['execution_count'] = None
                
                cells.insert(cell_number, new_cell)
                
            elif edit_mode == 'delete':
                # Delete cell
                if 0 <= cell_number < len(cells):
                    cells.pop(cell_number)
                else:
                    raise ValidationError(f"Cell index {cell_number} out of range")
                
            else:  # replace
                # Replace cell content
                if 0 <= cell_number < len(cells):
                    cells[cell_number]['source'] = new_source.split('\n')
                    if cell_type:
                        cells[cell_number]['cell_type'] = cell_type
                else:
                    raise ValidationError(f"Cell index {cell_number} out of range")
            
            # Update notebook
            notebook['cells'] = cells
            
            # Write back to file
            async with aiofiles.open(validated_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(notebook, indent=2))
            
            logger.info(f"Notebook cell edited successfully")
            
            return {
                'success': True,
                'notebook_path': notebook_path,
                'cell_number': cell_number,
                'edit_mode': edit_mode,
                'total_cells': len(cells)
            }
            
        except Exception as e:
            logger.error(f"Notebook editing failed: {e}")
            raise FileSystemError(f"Failed to edit notebook: {e}")


# ============================================================================
# WEB TOOLS
# ============================================================================

class WebFetchTool:
    """Fetch and analyze web content"""
    
    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
    
    async def fetch_url(self, url: str, prompt: Optional[str] = None) -> Dict[str, Any]:
        """Fetch content from URL and optionally process with prompt"""
        logger.info(f"Fetching URL: {url}")
        
        try:
            # Validate URL format
            if not url.startswith(('http://', 'https://')):
                error_msg = f"Invalid URL format: {url}. URLs must start with 'http://' or 'https://'"
                return {
                    'url': url,
                    'error': error_msg,
                    'user_message': error_msg,
                    'success': False,
                    'status': 0
                }
            
            timeout = aiohttp.ClientTimeout(total=self.timeout, connect=10.0)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, allow_redirects=True) as response:
                    content_type = response.headers.get('content-type', '').lower()
                    
                    # Handle different status codes
                    if response.status >= 400:
                        error_content = await response.text()
                        
                        # Create user-friendly error messages
                        if response.status == 401:
                            user_message = f"Authorization failed for {url}. The URL requires authentication or valid credentials."
                        elif response.status == 403:
                            user_message = f"Access forbidden to {url}. You don't have permission to access this resource."
                        elif response.status == 404:
                            user_message = f"Page not found at {url}. The URL may be incorrect or the resource has been moved."
                        elif response.status == 429:
                            user_message = f"Rate limit exceeded for {url}. Too many requests - try again later."
                        elif response.status >= 500:
                            user_message = f"Server error at {url} (HTTP {response.status}). The website is experiencing technical difficulties."
                        else:
                            user_message = f"HTTP {response.status} error accessing {url}: {response.reason}"
                        
                        return {
                            'url': url,
                            'status': response.status,
                            'error': f"HTTP {response.status}: {response.reason}",
                            'user_message': user_message,
                            'content_type': content_type,
                            'content': error_content[:500] if error_content else "",
                            'size': len(error_content) if error_content else 0,
                            'success': False
                        }
                    
                    # Process successful response
                    if 'text/html' in content_type:
                        content = await response.text()
                        # Convert HTML to markdown (simplified)
                        processed_content = self._html_to_markdown(content)
                    elif 'application/json' in content_type:
                        content = await response.text()
                        processed_content = content  # Keep JSON as-is
                    else:
                        content = await response.text()
                        processed_content = content
                    
                    result = {
                        'url': url,
                        'status': response.status,
                        'content_type': content_type,
                        'content': processed_content,
                        'size': len(content),
                        'success': True,
                        'user_message': f"Successfully fetched {len(content)} characters from {url}"
                    }
                    
                    if prompt:
                        # Process with prompt (placeholder - would use AI in real implementation)
                        result['analysis'] = f"Analysis of {url} with prompt: {prompt}"
                    
                    return result
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching URL: {url}")
            user_message = f"Request to {url} timed out after {self.timeout} seconds. The server may be slow or unresponsive."
            return {
                'url': url,
                'error': f"Request timed out after {self.timeout} seconds",
                'user_message': user_message,
                'success': False,
                'status': 0
            }
        except aiohttp.ClientError as e:
            logger.error(f"Client error fetching URL: {url} - {e}")
            # Create more specific error messages based on error type
            if "Name or service not known" in str(e) or "nodename nor servname provided" in str(e):
                user_message = f"Could not resolve hostname for {url}. Please check the URL is correct."
            elif "Connection refused" in str(e):
                user_message = f"Connection refused to {url}. The server may be down or the port may be blocked."
            elif "SSL" in str(e) or "certificate" in str(e).lower():
                user_message = f"SSL/TLS error accessing {url}. The website may have certificate issues."
            else:
                user_message = f"Network error accessing {url}: {str(e)}"
            
            return {
                'url': url,
                'error': f"Connection error: {str(e)}",
                'user_message': user_message,
                'success': False,
                'status': 0
            }
        except Exception as e:
            logger.error(f"Web fetch failed: {e}")
            user_message = f"Unexpected error fetching {url}: {str(e)}"
            return {
                'url': url,
                'error': f"Unexpected error: {str(e)}",
                'user_message': user_message,
                'success': False,
                'status': 0
            }
    
    def _html_to_markdown(self, html: str) -> str:
        """Convert HTML to markdown (simplified)"""
        # This is a very basic implementation
        # In practice, you'd use a library like html2text
        
        # Remove scripts and styles
        html = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Convert basic tags
        html = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n', html, flags=re.IGNORECASE)
        html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n', html, flags=re.IGNORECASE)
        html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n', html, flags=re.IGNORECASE)
        html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html, flags=re.IGNORECASE)
        html = re.sub(r'<br[^>]*>', '\n', html, flags=re.IGNORECASE)
        
        # Remove remaining HTML tags
        html = re.sub(r'<[^>]+>', '', html)
        
        # Clean up whitespace
        html = re.sub(r'\n\s*\n', '\n\n', html)
        html = html.strip()
        
        return html


# ============================================================================
# TODO TOOLS
# ============================================================================

class TodoStorage:
    """Session-based storage for todos, similar to TypeScript implementation"""
    
    # Class-level storage to persist todos during the session by sessionId
    _session_todos: Dict[str, List[TodoItem]] = {}
    
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
    
    async def load_todos(self) -> List[TodoItem]:
        """Load todos for current session"""
        try:
            # Return todos for this session, or empty list if none exist
            return self._session_todos.get(self.session_id, []).copy()
            
        except Exception as e:
            logger.error(f"Failed to load todos: {e}")
            return []
    
    async def save_todos(self, todos: List[TodoItem]) -> None:
        """Save todos for current session"""
        try:
            # Save to session storage for this session
            self._session_todos[self.session_id] = todos.copy()
                
        except Exception as e:
            logger.error(f"Failed to save todos: {e}")
            raise ToolError(f"Failed to save todos: {e}")
    


class TodoReadTool:
    """Read current todo list"""
    
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
    
    async def todo_read(self, session_id: str = None) -> List[Dict[str, Any]]:
        """Read the current todo list for a session"""
        logger.info("Reading todo list")
        
        # Use provided session_id or default
        sid = session_id or self.session_id
        storage = TodoStorage(sid)
        todos = await storage.load_todos()
        
        return [asdict(todo) for todo in todos]


class TodoWriteTool:
    """Create and manage structured task lists"""
    
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
    
    async def todo_write(self, todos: List[Dict[str, Any]], session_id: str = None) -> Dict[str, Any]:
        """Write/update the todo list by merging with existing todos"""
        logger.info(f"Writing {len(todos)} todos")
        
        try:
            # Use provided session_id or default
            sid = session_id or self.session_id
            storage = TodoStorage(sid)
            
            # Load existing todos
            existing_todos = await storage.load_todos()
            existing_todos_dict = {todo.id: todo for todo in existing_todos}
            
            # Convert new todos to TodoItem objects and merge with existing
            updated_todos = []
            new_todos_dict = {}
            
            for todo_data in todos:
                # Handle both dict and string formats for backward compatibility
                if isinstance(todo_data, str):
                    # Generate ID for new string-based todo
                    todo_id = str(int(time.time() * 1000000) + len(updated_todos))
                    new_todo = TodoItem(
                        id=todo_id,
                        content=todo_data,
                        status='pending',
                        priority='medium'
                    )
                    updated_todos.append(new_todo)
                    new_todos_dict[todo_id] = new_todo
                else:
                    # Ensure required fields with defaults
                    todo_data.setdefault('status', 'pending')
                    todo_data.setdefault('priority', 'medium')
                    todo_data.setdefault('created_at', time.time())
                    todo_data['updated_at'] = time.time()
                    
                    todo_id = todo_data.get('id')
                    if todo_id and todo_id in existing_todos_dict:
                        # Update existing todo
                        existing_todo = existing_todos_dict[todo_id]
                        existing_todo.content = todo_data.get('content', existing_todo.content)
                        existing_todo.status = todo_data.get('status', existing_todo.status)
                        existing_todo.priority = todo_data.get('priority', existing_todo.priority)
                        existing_todo.updated_at = time.time()
                        updated_todos.append(existing_todo)
                        new_todos_dict[todo_id] = existing_todo
                    else:
                        # Create new todo
                        if not todo_id:
                            todo_data['id'] = str(int(time.time() * 1000000) + len(updated_todos))
                        new_todo = TodoItem(**todo_data)
                        updated_todos.append(new_todo)
                        new_todos_dict[new_todo.id] = new_todo
            
            # Add any existing todos that weren't in the new list (preserve them)
            for existing_id, existing_todo in existing_todos_dict.items():
                if existing_id not in new_todos_dict:
                    updated_todos.append(existing_todo)
            
            await storage.save_todos(updated_todos)
            
            return {
                'success': True,
                'total_todos': len(updated_todos),
                'updated_at': time.time(),
                'todos': [asdict(todo) for todo in updated_todos]
            }
            
        except Exception as e:
            logger.error(f"Failed to write todos: {e}")
            raise ToolError(f"Failed to write todos: {e}")
    
    async def add_todo(
        self, 
        content: str, 
        priority: str = 'medium', 
        status: str = 'pending',
        session_id: str = None
    ) -> Dict[str, Any]:
        """Add a single todo item"""
        sid = session_id or self.session_id
        storage = TodoStorage(sid)
        todos = await storage.load_todos()
        
        new_todo = TodoItem(
            id=str(int(time.time() * 1000)),  # Simple ID generation
            content=content,
            status=status,
            priority=priority
        )
        
        todos.append(new_todo)
        await storage.save_todos(todos)
        
        return {
            'success': True,
            'todo': asdict(new_todo)
        }
    
    async def update_todo(self, todo_id: str, session_id: str = None, **updates) -> Dict[str, Any]:
        """Update a specific todo item"""
        sid = session_id or self.session_id
        storage = TodoStorage(sid)
        todos = await storage.load_todos()
        
        for todo in todos:
            if todo.id == todo_id:
                for key, value in updates.items():
                    if hasattr(todo, key):
                        setattr(todo, key, value)
                todo.updated_at = time.time()
                break
        else:
            raise ValidationError(f"Todo not found: {todo_id}")
        
        await storage.save_todos(todos)
        
        return {
            'success': True,
            'todo_id': todo_id,
            'updates': updates
        }
    


# ============================================================================
# MAIN TOOLS INTERFACE
# ============================================================================

class ClaudeTools:
    """Main interface for all Claude Code tools"""
    
    def __init__(self):
        # Initialize all tools
        self.task = TaskAgent()
        self.bash = BashTool()
        self.glob = GlobTool()
        self.grep = GrepTool()
        self.ls = LSTool()
        self.read = ReadTool()
        self.edit = EditTool()
        self.multiedit = MultiEditTool()
        self.write = WriteTool()
        self.notebook_read = NotebookReadTool()
        self.notebook_edit = NotebookEditTool()
        self.web_fetch = WebFetchTool()
        self.todo_read = TodoReadTool()
        self.todo_write = TodoWriteTool()
    
    def list_tools(self) -> List[str]:
        """Get list of available tools"""
        return [
            'task', 'bash', 'glob', 'grep', 'ls', 'read', 'edit', 'multiedit',
            'write', 'notebook_read', 'notebook_edit', 'web_fetch',
            'todo_read', 'todo_write'
        ]
    
    async def execute_tool(self, tool_name: str, method: str, **kwargs) -> Any:
        """Execute a tool method with given parameters"""
        if not hasattr(self, tool_name):
            raise ValidationError(f"Unknown tool: {tool_name}")
        
        tool = getattr(self, tool_name)
        
        if not hasattr(tool, method):
            raise ValidationError(f"Tool {tool_name} has no method {method}")
        
        method_func = getattr(tool, method)
        
        try:
            return await method_func(**kwargs)
        except Exception as e:
            logger.error(f"Tool execution failed: {tool_name}.{method} - {e}")
            raise


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

async def main():
    """Main CLI interface for testing tools"""
    tools = ClaudeTools()
    
    if len(sys.argv) < 3:
        print("Usage: python tools.py <tool> <method> [args...]")
        print("Available tools:", tools.list_tools())
        return
    
    tool_name = sys.argv[1]
    method = sys.argv[2]
    
    # Parse additional arguments as JSON if provided
    kwargs = {}
    if len(sys.argv) > 3:
        try:
            kwargs = json.loads(sys.argv[3])
        except json.JSONDecodeError:
            # Treat as simple string arguments
            if len(sys.argv) == 4:
                kwargs = {'path': sys.argv[3]}
            elif len(sys.argv) == 5:
                kwargs = {'pattern': sys.argv[3], 'path': sys.argv[4]}
    
    try:
        result = await tools.execute_tool(tool_name, method, **kwargs)
        print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
