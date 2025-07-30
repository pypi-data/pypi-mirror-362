import os
import shutil
import re
import json
import fnmatch
import mimetypes
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime


class FilesystemTools:
    def __init__(self, allowed_dirs: List[str] = None):
        self.allowed_dirs = allowed_dirs or []
    
    def _is_path_allowed(self, path: str) -> bool:
        """Check if the given path is within allowed directories."""
        if not self.allowed_dirs:
            return True
        
        abs_path = os.path.abspath(path)
        for allowed_dir in self.allowed_dirs:
            abs_allowed = os.path.abspath(allowed_dir)
            if abs_path.startswith(abs_allowed):
                return True
        return False
    
    def _check_path_access(self, path: str) -> None:
        """Raise exception if path is not allowed."""
        if not self._is_path_allowed(path):
            raise PermissionError(f"Access to path '{path}' is not allowed")
    
    def read_file(self, path: str) -> str:
        """Read the complete contents of a file from the file system."""
        self._check_path_access(path)
        
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {path}")
        except PermissionError:
            raise PermissionError(f"Permission denied: {path}")
        except UnicodeDecodeError:
            raise ValueError(f"File is not a text file or has encoding issues: {path}")
    
    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Create a new file or overwrite an existing file with new content."""
        self._check_path_access(path)
        
        try:
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            return {
                "success": True,
                "path": path,
                "bytes_written": len(content.encode('utf-8'))
            }
        except PermissionError:
            raise PermissionError(f"Permission denied: {path}")
        except Exception as e:
            raise Exception(f"Error writing file {path}: {str(e)}")
    
    def list_directory(self, path: str) -> List[Dict[str, Any]]:
        """Get a detailed listing of all files and directories in a specified path."""
        self._check_path_access(path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory not found: {path}")
        
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Path is not a directory: {path}")
        
        try:
            items = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                stat = os.stat(item_path)
                
                items.append({
                    "name": item,
                    "path": item_path,
                    "type": "directory" if os.path.isdir(item_path) else "file",
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "permissions": oct(stat.st_mode)[-3:]
                })
            
            return sorted(items, key=lambda x: (x["type"] == "file", x["name"]))
        except PermissionError:
            raise PermissionError(f"Permission denied: {path}")
    
    def create_directory(self, path: str) -> Dict[str, Any]:
        """Create a new directory or ensure a directory exists."""
        self._check_path_access(path)
        
        try:
            os.makedirs(path, exist_ok=True)
            return {
                "success": True,
                "path": path,
                "created": not os.path.exists(path)
            }
        except PermissionError:
            raise PermissionError(f"Permission denied: {path}")
        except Exception as e:
            raise Exception(f"Error creating directory {path}: {str(e)}")
    
    def copy_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Copy files and directories."""
        self._check_path_access(source)
        self._check_path_access(destination)
        
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source not found: {source}")
        
        try:
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                # Create parent directories if needed
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                shutil.copy2(source, destination)
            
            return {
                "success": True,
                "source": source,
                "destination": destination,
                "type": "directory" if os.path.isdir(source) else "file"
            }
        except PermissionError:
            raise PermissionError(f"Permission denied copying from {source} to {destination}")
        except Exception as e:
            raise Exception(f"Error copying {source} to {destination}: {str(e)}")
    
    def move_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Move or rename files and directories."""
        self._check_path_access(source)
        self._check_path_access(destination)
        
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source not found: {source}")
        
        try:
            # Create parent directories if needed
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            shutil.move(source, destination)
            
            return {
                "success": True,
                "source": source,
                "destination": destination
            }
        except PermissionError:
            raise PermissionError(f"Permission denied moving from {source} to {destination}")
        except Exception as e:
            raise Exception(f"Error moving {source} to {destination}: {str(e)}")
    
    def search_files(self, path: str, pattern: str) -> List[Dict[str, Any]]:
        """Recursively search for files and directories matching a pattern."""
        self._check_path_access(path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")
        
        matches = []
        try:
            for root, dirs, files in os.walk(path):
                # Filter directories based on allowed paths
                if not self._is_path_allowed(root):
                    continue
                
                # Check directories
                for dir_name in dirs:
                    if fnmatch.fnmatch(dir_name, pattern):
                        dir_path = os.path.join(root, dir_name)
                        stat = os.stat(dir_path)
                        matches.append({
                            "name": dir_name,
                            "path": dir_path,
                            "type": "directory",
                            "size": stat.st_size,
                            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                        })
                
                # Check files
                for file_name in files:
                    if fnmatch.fnmatch(file_name, pattern):
                        file_path = os.path.join(root, file_name)
                        stat = os.stat(file_path)
                        matches.append({
                            "name": file_name,
                            "path": file_path,
                            "type": "file",
                            "size": stat.st_size,
                            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                        })
            
            return matches
        except PermissionError:
            raise PermissionError(f"Permission denied searching in: {path}")
    
    def get_file_info(self, path: str) -> Dict[str, Any]:
        """Retrieve detailed metadata about a file or directory."""
        self._check_path_access(path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")
        
        try:
            stat = os.stat(path)
            is_dir = os.path.isdir(path)
            
            info = {
                "name": os.path.basename(path),
                "path": path,
                "type": "directory" if is_dir else "file",
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
                "permissions": oct(stat.st_mode)[-3:],
                "is_symlink": os.path.islink(path)
            }
            
            if not is_dir:
                mime_type, _ = mimetypes.guess_type(path)
                info["mime_type"] = mime_type
            
            return info
        except PermissionError:
            raise PermissionError(f"Permission denied: {path}")
    
    def list_allowed_directories(self) -> List[str]:
        """Returns the list of directories that this server is allowed to access."""
        return self.allowed_dirs.copy()
    
    def read_multiple_files(self, paths: List[str]) -> Dict[str, Union[str, Dict[str, str]]]:
        """Read the contents of multiple files in a single operation."""
        results = {}
        
        for path in paths:
            try:
                results[path] = self.read_file(path)
            except Exception as e:
                results[path] = {"error": str(e)}
        
        return results
    
    def tree(self, path: str, depth: int = 3, follow_symlinks: bool = False) -> Dict[str, Any]:
        """Returns a hierarchical JSON representation of a directory structure."""
        self._check_path_access(path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")
        
        def _build_tree(current_path: str, current_depth: int) -> Dict[str, Any]:
            if current_depth > depth:
                return None
            
            if not self._is_path_allowed(current_path):
                return None
            
            try:
                stat = os.stat(current_path)
                is_dir = os.path.isdir(current_path)
                
                node = {
                    "name": os.path.basename(current_path),
                    "path": current_path,
                    "type": "directory" if is_dir else "file",
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                }
                
                if is_dir and current_depth < depth:
                    children = []
                    try:
                        for item in os.listdir(current_path):
                            item_path = os.path.join(current_path, item)
                            
                            if os.path.islink(item_path) and not follow_symlinks:
                                continue
                            
                            child = _build_tree(item_path, current_depth + 1)
                            if child:
                                children.append(child)
                        
                        node["children"] = sorted(children, key=lambda x: (x["type"] == "file", x["name"]))
                    except PermissionError:
                        node["children"] = []
                
                return node
            except (PermissionError, OSError):
                return None
        
        return _build_tree(path, 0)
    
    def delete_file(self, path: str, recursive: bool = False) -> Dict[str, Any]:
        """Delete a file or directory from the file system."""
        self._check_path_access(path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")
        
        # Check type before deletion
        is_directory = os.path.isdir(path)
        
        try:
            if is_directory:
                if recursive:
                    shutil.rmtree(path)
                else:
                    os.rmdir(path)
            else:
                os.remove(path)
            
            return {
                "success": True,
                "path": path,
                "type": "directory" if is_directory else "file"
            }
        except PermissionError:
            raise PermissionError(f"Permission denied: {path}")
        except OSError as e:
            if e.errno == 66:  # Directory not empty
                raise ValueError(f"Directory not empty (use recursive=True): {path}")
            raise
    
    def modify_file(self, path: str, find: str, replace: str, 
                   all_occurrences: bool = True, regex: bool = False) -> Dict[str, Any]:
        """Update file by finding and replacing text. Provides a simple pattern matching interface without needing exact character positions."""
        self._check_path_access(path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        if os.path.isdir(path):
            raise IsADirectoryError(f"Path is a directory: {path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            if regex:
                if all_occurrences:
                    new_content = re.sub(find, replace, content)
                    count = len(re.findall(find, content))
                else:
                    new_content = re.sub(find, replace, content, count=1)
                    count = 1 if re.search(find, content) else 0
            else:
                if all_occurrences:
                    count = content.count(find)
                    new_content = content.replace(find, replace)
                else:
                    count = 1 if find in content else 0
                    new_content = content.replace(find, replace, 1)
            
            with open(path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            return {
                "success": True,
                "path": path,
                "replacements": count,
                "regex": regex
            }
        except PermissionError:
            raise PermissionError(f"Permission denied: {path}")
        except UnicodeDecodeError:
            raise ValueError(f"File is not a text file or has encoding issues: {path}")
    
    def search_within_files(self, path: str, substring: str, 
                           depth: Optional[int] = None, max_results: int = 1000) -> List[Dict[str, Any]]:
        """Search for text within file contents."""
        self._check_path_access(path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")
        
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Path must be a directory: {path}")
        
        results = []
        current_results = 0
        
        def _search_in_file(file_path: str) -> List[Dict[str, Any]]:
            nonlocal current_results
            matches = []
            
            try:
                # Check if file is likely to be text
                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type and not mime_type.startswith('text/'):
                    return matches
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line_num, line in enumerate(file, 1):
                        if current_results >= max_results:
                            break
                        
                        if substring in line:
                            matches.append({
                                "file": file_path,
                                "line": line_num,
                                "content": line.strip(),
                                "position": line.find(substring)
                            })
                            current_results += 1
                
            except (UnicodeDecodeError, PermissionError, OSError):
                # Skip files that can't be read
                pass
            
            return matches
        
        try:
            for root, dirs, files in os.walk(path):
                # Check depth limit
                if depth is not None:
                    current_depth = root[len(path):].count(os.sep)
                    if current_depth >= depth:
                        dirs[:] = []  # Don't descend further
                        continue
                
                # Filter directories based on allowed paths
                if not self._is_path_allowed(root):
                    continue
                
                for file_name in files:
                    if current_results >= max_results:
                        break
                    
                    file_path = os.path.join(root, file_name)
                    matches = _search_in_file(file_path)
                    results.extend(matches)
                
                if current_results >= max_results:
                    break
        
        except PermissionError:
            raise PermissionError(f"Permission denied searching in: {path}")
        
        return results
    
    def handle_read_resource(self, uri: str) -> Dict[str, Any]:
        """Access to files and directories on the local file system."""
        if not uri.startswith("file://"):
            raise ValueError(f"Unsupported URI scheme: {uri}")
        
        # Extract path from file:// URI
        path = uri[7:]  # Remove "file://" prefix
        
        # Handle Windows paths if needed
        if path.startswith("/") and len(path) > 1 and path[2] == ":":
            path = path[1:]  # Remove leading slash for Windows paths like /C:/
        
        self._check_path_access(path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Resource not found: {path}")
        
        try:
            if os.path.isdir(path):
                # For directories, return a listing
                items = self.list_directory(path)
                return {
                    "uri": uri,
                    "mimeType": "application/json",
                    "text": json.dumps(items, indent=2)
                }
            else:
                # For files, return content
                content = self.read_file(path)
                mime_type, _ = mimetypes.guess_type(path)
                return {
                    "uri": uri,
                    "mimeType": mime_type or "text/plain",
                    "text": content
                }
        except Exception as e:
            raise Exception(f"Error reading resource {uri}: {str(e)}")
