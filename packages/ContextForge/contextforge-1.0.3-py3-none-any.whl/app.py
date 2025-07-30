#!/usr/bin/env python3
"""
ContextForge Web - Flask application

A web-based version of ContextForge that can be accessed over SSH.
"""

from flask import Flask, render_template, request, jsonify, Response
from pathlib import Path
from typing import Dict, List, Tuple
import fnmatch
import re
import tiktoken
import json
from datetime import datetime
from diff_processor import DiffProcessor, FileChange
import threading
import time
import queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from xml_main import xml_formatting

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# File system monitoring
file_watchers = {}  # path -> observer
file_events_queue = queue.Queue()
sse_clients = []

# File system monitoring
file_watchers = {}  # path -> observer
file_events_queue = queue.Queue()
sse_clients = []

class FileChangeHandler(FileSystemEventHandler):
    """Handle file system events and queue them for SSE broadcast."""
    
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.last_event_time = {}
        self.debounce_delay = 0.5  # 500ms debounce
    
    def should_ignore_event(self, path):
        """Check if we should ignore this event based on patterns."""
        path_obj = Path(path)
        # Ignore hidden files and common editor temp files
        if path_obj.name.startswith('.'):
            return True
        if path_obj.suffix in ['.swp', '.tmp', '.temp', '~']:
            return True
        if '.git' in path_obj.parts:
            return True
        return False
    
    def debounce_event(self, path, event_type):
        """Debounce rapid file events."""
        current_time = time.time()
        event_key = f"{path}:{event_type}"
        
        if event_key in self.last_event_time:
            if current_time - self.last_event_time[event_key] < self.debounce_delay:
                return True  # Skip this event
        
        self.last_event_time[event_key] = current_time
        return False
    
    def queue_event(self, event_type, path):
        """Queue an event for broadcasting."""
        if self.should_ignore_event(path):
            return
            
        if self.debounce_event(path, event_type):
            return
        
        try:
            relative_path = Path(path).relative_to(self.root_path)
            event_data = {
                'type': event_type,
                'path': str(path),
                'relative_path': str(relative_path),
                'timestamp': time.time()
            }
            file_events_queue.put(event_data)
        except ValueError:
            # Path is outside root directory
            pass
    
    def on_created(self, event):
        if not event.is_directory:
            self.queue_event('created', event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.queue_event('deleted', event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory:
            self.queue_event('modified', event.src_path)
    
    def on_moved(self, event):
        if not event.is_directory:
            self.queue_event('moved', event.dest_path)

def normalized_path(value):
    """Normalize a path to ensure consistent handling across the application."""
    if isinstance(value, str):
        return str(Path(value).expanduser().resolve())
    elif isinstance(value, Path):
        return str(value.expanduser().resolve())
    else:
        raise ValueError(f"Invalid path type: {type(value)}")

class TokenCounter:
    """Handle token counting for different models."""
    
    def __init__(self):
        self.encodings = {
            'gpt-4': 'cl100k_base',
            'gpt-3.5-turbo': 'cl100k_base',
            'gpt-4-32k': 'cl100k_base',
            'text-davinci-003': 'p50k_base',
            'text-davinci-002': 'p50k_base',
            'code-davinci-002': 'p50k_base',
            'claude': 'cl100k_base'  # Approximation for Claude
        }
        self.current_encoding = None
        self.current_model = 'gpt-4'
        self._load_encoding(self.current_model)
    
    def _load_encoding(self, model: str):
        """Load the appropriate encoding for the model."""
        encoding_name = self.encodings.get(model, 'cl100k_base')
        try:
            self.current_encoding = tiktoken.get_encoding(encoding_name)
            self.current_model = model
        except Exception as e:
            print(f"Error loading encoding {encoding_name}: {e}")
            # Fallback to cl100k_base
            self.current_encoding = tiktoken.get_encoding('cl100k_base')
    
    def count_tokens(self, text: str, model: str = None) -> int:
        """Count tokens in the given text."""
        if model and model != self.current_model:
            self._load_encoding(model)
        
        try:
            return len(self.current_encoding.encode(text))
        except Exception as e:
            print(f"Error counting tokens: {e}")
            # Fallback to word-based estimation
            return int(len(text.split()) * 1.3)
    
    def estimate_file_tokens(self, file_path: Path) -> int:
        """Estimate tokens for a single file."""
        try:
            # Check if file is too large
            if file_path.stat().st_size > 1024 * 1024:  # 1MB
                # For large files, estimate based on size
                return int(file_path.stat().st_size / 4)  # Rough estimate: 4 chars per token
            
            content = file_manager.get_file_content(file_path)
            return self.count_tokens(content)
        except Exception:
            return 0
    
    def estimate_prompt_tokens(self, files: List[str], instructions: str, format_type: str) -> int:
        """Estimate total tokens for the complete prompt."""
        total_tokens = 0
        
        # Count instruction tokens
        if instructions:
            total_tokens += self.count_tokens(instructions)
        
        # Add format overhead
        if format_type == 'xml':
            total_tokens += 50  # XML tags overhead
        elif format_type == 'markdown':
            total_tokens += 30  # Markdown headers overhead
        else:
            total_tokens += 20  # Plain text overhead
        
        # Count tokens for each file
        for file_path in files:
            path = Path(file_path)
            if path.exists() and path.is_file():
                # Add file path tokens
                total_tokens += self.count_tokens(str(path))
                # Add file content tokens
                total_tokens += self.estimate_file_tokens(path)
                # Add format-specific overhead per file
                if format_type == 'xml':
                    total_tokens += 10
                elif format_type == 'markdown':
                    total_tokens += 15
                else:
                    total_tokens += 5
        
        return total_tokens

# Initialize token counter
token_counter = TokenCounter()

def start_file_watcher(path):
    """Start watching a directory for changes."""
    path_str = str(path)
    
    # Stop existing watcher if any
    stop_file_watcher(path_str)
    
    try:
        event_handler = FileChangeHandler(path)
        observer = Observer()
        observer.schedule(event_handler, path_str, recursive=True)
        observer.start()
        
        file_watchers[path_str] = observer
        print(f"Started watching: {path_str}")
    except Exception as e:
        print(f"Error starting file watcher: {e}")

def stop_file_watcher(path):
    """Stop watching a directory."""
    path_str = str(path)
    
    if path_str in file_watchers:
        observer = file_watchers[path_str]
        observer.stop()
        observer.join(timeout=1)
        del file_watchers[path_str]
        print(f"Stopped watching: {path_str}")

def stop_all_watchers():
    """Stop all active file watchers."""
    for path in list(file_watchers.keys()):
        stop_file_watcher(path)

# Background thread to process file events
def process_file_events():
    """Process file events and broadcast to SSE clients."""
    while True:
        try:
            # Wait for an event with timeout
            event = file_events_queue.get(timeout=1)
            
            # Broadcast to all connected clients
            event_data = f"data: {json.dumps(event)}\n\n"
            
            # Send to all clients and remove disconnected ones
            disconnected_clients = []
            for client in sse_clients:
                try:
                    client.put(event_data)
                except:
                    disconnected_clients.append(client)
            
            # Remove disconnected clients
            for client in disconnected_clients:
                sse_clients.remove(client)
                
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Error processing file events: {e}")

# Start the event processor thread
event_processor_thread = threading.Thread(target=process_file_events, daemon=True)
event_processor_thread.start()

class GitIgnoreParser:
    """Parse and apply .gitignore rules."""
    
    def __init__(self):
        self.rules = []
    
    def parse_gitignore(self, gitignore_path: Path) -> None:
        """Parse a .gitignore file and add rules."""
        if not gitignore_path.exists():
            return
            
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.add_rule(line)
        except Exception:
            pass
    
    def add_rule(self, pattern: str) -> None:
        """Add a gitignore rule."""
        negated = False
        if pattern.startswith('!'):
            negated = True
            pattern = pattern[1:]
        
        # Convert gitignore pattern to regex
        if pattern.endswith('/'):
            # Directory only
            regex_pattern = self._gitignore_to_regex(pattern[:-1]) + '(/.*)?$'
        else:
            regex_pattern = self._gitignore_to_regex(pattern)
        
        try:
            regex = re.compile(regex_pattern)
            self.rules.append((regex, negated))
        except re.error:
            pass
    
    def _gitignore_to_regex(self, pattern: str) -> str:
        """Convert gitignore pattern to regex."""
        # Handle special cases
        if pattern.startswith('/'):
            # Anchored to root
            pattern = '^' + pattern[1:]
        else:
            # Can match anywhere
            pattern = '(^|/)' + pattern
        
        # Escape special regex characters except * and ?
        pattern = re.escape(pattern)
        pattern = pattern.replace(r'\*', '[^/]*')
        pattern = pattern.replace(r'\?', '[^/]')
        pattern = pattern.replace(r'\[', '[')
        pattern = pattern.replace(r'\]', ']')
        
        return pattern
    
    def is_ignored(self, path: str, is_dir: bool = False) -> bool:
        """Check if a path should be ignored."""
        # Normalize path
        path = path.replace('\\', '/')
        if path.startswith('./'):
            path = path[2:]
        
        # Check all rules in order
        ignored = False
        for regex, negated in self.rules:
            if regex.search(path):
                ignored = not negated
        
        return ignored


class FileTreeManager:
    """Manages file tree operations for the web interface."""
    
    def __init__(self):
        self.default_ignored_patterns = {
            '.git', '__pycache__', 'node_modules', '.idea', '.vscode', 
            'venv', '.env', '.DS_Store', 'dist', 'build', '*.egg-info',
            '.pytest_cache', '.coverage', 'coverage', '.nyc_output'
        }
        self.gitignore_parser = None
        self.user_settings = {
            'use_gitignore': True,
            'custom_ignore_patterns': [],
            'whitelist_patterns': []
        }
        
    def get_file_icon(self, path: Path) -> str:
        """Get appropriate icon for a file or folder."""
        if path.is_dir():
            return "📁"
        else:
            ext = path.suffix.lower()
            icon_map = {
                '.py': "🐍", '.js': "📜", '.jsx': "📜", '.ts': "📜", '.tsx': "📜",
                '.md': "📝", '.txt': "📄", '.json': "⚙", '.yaml': "⚙", '.yml': "⚙",
                '.xml': "📋", '.html': "🌐", '.css': "🎨", '.gitignore': "⚙", '.env': "⚙",
                '.java': "☕", '.cpp': "🔧", '.c': "🔧", '.h': "🔧", '.hpp': "🔧",
                '.go': "🐹", '.rs': "🦀", '.php': "🐘", '.rb': "💎", '.swift': "🦉"
            }
            return icon_map.get(ext, "📄")
    
    def should_ignore(self, path: Path, root_path: Path) -> bool:
        """Check if a path should be ignored based on all rules."""
        name = path.name
        
        # Check whitelist first - if whitelisted, never ignore
        relative_path = str(path.relative_to(root_path))
        for pattern in self.user_settings.get('whitelist_patterns', []):
            if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(name, pattern):
                return False
        
        # Check default patterns
        for pattern in self.default_ignored_patterns:
            if fnmatch.fnmatch(name, pattern):
                return True
        
        # Check custom ignore patterns
        for pattern in self.user_settings.get('custom_ignore_patterns', []):
            if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(name, pattern):
                return True
        
        # Check gitignore if enabled
        if self.user_settings.get('use_gitignore', True) and self.gitignore_parser:
            if self.gitignore_parser.is_ignored(relative_path, path.is_dir()):
                return True
        
        # Don't ignore dotfiles by default except for specific ones
        if name.startswith('.') and name not in {'.gitignore', '.env', '.env.example', '.eslintrc', '.prettierrc'}:
            return True
        
        return False
    
    def update_settings(self, settings: Dict) -> None:
        """Update user settings."""
        self.user_settings.update(settings)
    
    def get_directory_tree(self, directory: Path, max_depth: int = 20, show_ignored: bool = False) -> Tuple[Dict, Dict]:
        """Get directory tree structure as a nested dictionary."""
        if not directory.exists() or not directory.is_dir():
            return {}, {}
        
        # Parse gitignore if enabled
        if self.user_settings.get('use_gitignore', True):
            self.gitignore_parser = GitIgnoreParser()
            gitignore_path = directory / '.gitignore'
            if gitignore_path.exists():
                self.gitignore_parser.parse_gitignore(gitignore_path)
        
        stats = {
            'total_files': 0,
            'ignored_files': 0,
            'total_dirs': 0,
            'ignored_dirs': 0
        }
        
        def build_tree(path: Path, depth: int = 0) -> Dict:
            if depth > max_depth:
                return {}
                
            is_ignored = self.should_ignore(path, directory)
            
            tree = {
                'name': path.name,
                'path': str(path),
                'is_dir': path.is_dir(),
                'icon': self.get_file_icon(path),
                'ignored': is_ignored,
                'children': []
            }
            
            if path.is_dir():
                stats['total_dirs'] += 1
                if is_ignored:
                    stats['ignored_dirs'] += 1
                    
                try:
                    items = sorted(path.iterdir(), 
                                 key=lambda x: (not x.is_dir(), x.name.lower()))
                    for item in items:
                        item_ignored = self.should_ignore(item, directory)
                        if show_ignored or not item_ignored:
                            child_tree = build_tree(item, depth + 1)
                            if child_tree:
                                tree['children'].append(child_tree)
                except PermissionError:
                    pass
            else:
                stats['total_files'] += 1
                if is_ignored:
                    stats['ignored_files'] += 1
            
            return tree
        
        return build_tree(directory), stats
    
    def get_file_content(self, file_path: Path) -> str:
        """Get file content safely."""
        try:
            # Check if file is too large
            if file_path.stat().st_size > 1024 * 1024:  # 1MB limit
                return f"[File too large: {file_path.stat().st_size / (1024*1024):.1f}MB]"
            
            # Try to read as text
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except:
                return "[Binary file or encoding error]"
        except Exception as e:
            return f"[Error reading file: {str(e)}]"

file_manager = FileTreeManager()

# -------- BACKUP MANAGEMENT --------
# Only track backups for undo functionality

@app.route('/')
def index():
    """Main application page."""
    return render_template('index.html')

@app.route('/api/file-events')
def file_events_stream():
    """Server-Sent Events endpoint for file change notifications."""
    def generate():
        client_queue = queue.Queue()
        sse_clients.append(client_queue)
        
        try:
            # Send initial connection message
            yield f"data: {json.dumps({'type': 'connected'})}\n\n"
            
            while True:
                try:
                    # Wait for events with heartbeat
                    event_data = client_queue.get(timeout=30)
                    yield event_data
                except queue.Empty:
                    # Send heartbeat to keep connection alive
                    yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
                    
        finally:
            # Clean up when client disconnects
            if client_queue in sse_clients:
                sse_clients.remove(client_queue)
    
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'  # Disable Nginx buffering
        }
    )

@app.route('/api/browse', methods=['POST'])
def browse_directory():
    """Browse directory and return file tree."""
    data = request.get_json()
    directory_path = data.get('path', '.')
    settings = data.get('settings', {})
    show_ignored = data.get('show_ignored', False)
    max_depth = data.get('max_depth', 20)  # Allow custom depth, default to 20
    
    try:
        path = Path(directory_path).expanduser().resolve()
        if not path.exists():
            return jsonify({'error': 'Directory does not exist'}), 400
        
        # Update settings if provided
        if settings:
            file_manager.update_settings(settings)
        
        tree, stats = file_manager.get_directory_tree(path, max_depth=max_depth, show_ignored=show_ignored)
        
        # Start watching this directory if max_depth > 1 (not just browsing)
        if max_depth > 1:
            start_file_watcher(path)
        
        return jsonify({
            'tree': tree,
            'path': str(path),
            'stats': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/file-content', methods=['POST'])
def get_file_content():
    """Get content of a specific file."""
    data = request.get_json()
    file_path = data.get('path')
    
    try:
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            return jsonify({'error': 'File does not exist'}), 400
        
        content = file_manager.get_file_content(path)
        return jsonify({
            'content': content,
            'path': str(path),
            'size': path.stat().st_size if path.exists() else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-prompt', methods=['POST'])
def generate_prompt():
    """Generate prompt from selected files."""
    data = request.get_json()
    selected_files = data.get('files', [])
    instructions = data.get('instructions', '')
    use_xml_formatting = data.get('use_xml_formatting', False)
    
    try:
        # Build the prompt
        prompt = generate_xml_prompt(selected_files, instructions, use_xml_formatting)
        
        # Get accurate token count
        token_count = token_counter.count_tokens(prompt)
        
        # Also calculate tokens per file for statistics
        file_token_counts = {}
        for file_path in selected_files:
            path = Path(file_path)
            if path.exists() and path.is_file():
                file_token_counts[file_path] = token_counter.estimate_file_tokens(path)
        
        return jsonify({
            'prompt': prompt,
            'token_count': token_count,
            'file_count': len(selected_files),
            'file_token_counts': file_token_counts,
            'average_tokens_per_file': sum(file_token_counts.values()) // len(file_token_counts) if file_token_counts else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_file_tree(files: List[str]) -> str:
    """Generate a tree representation of selected files."""
    if not files:
        return ""
    
    # Convert all paths to Path objects and get absolute paths
    paths = [Path(f).resolve() for f in files]
    
    # Find common root directory
    if len(paths) == 1:
        common_root = paths[0].parent
    else:
        # Find the common parent directory
        common_parts = []
        for part in paths[0].parts:
            if all(len(p.parts) > len(common_parts) and
                   p.parts[len(common_parts)] == part for p in paths):
                common_parts.append(part)
            else:
                break
        common_root = Path(*common_parts) if common_parts else Path('/')
    
    # Build tree structure
    tree_dict = {}
    for path in paths:
        try:
            relative_path = path.relative_to(common_root)
            parts = relative_path.parts
            
            current = tree_dict
            for i, part in enumerate(parts):
                if i == len(parts) - 1:  # It's a file
                    current[part] = None
                else:  # It's a directory
                    if part not in current:
                        current[part] = {}
                    current = current[part]
        except ValueError:
            # If relative_to fails, use the full path
            current = tree_dict
            parts = path.parts
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    current[part] = None
                else:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
    
    # Generate tree visualization
    def format_tree(tree, prefix="", is_last=True):
        lines = []
        items = list(tree.items())
        
        for i, (name, subtree) in enumerate(items):
            is_last_item = i == len(items) - 1
            
            # Add the tree branch characters
            if prefix == "":  # Root level
                connector = ""
            else:
                connector = "└── " if is_last_item else "├── "
            
            lines.append(f"{prefix}{connector}{name}")
            
            # If it's a directory, recurse
            if subtree is not None:
                extension = "    " if is_last_item else "│   "
                sub_lines = format_tree(subtree, prefix + extension, is_last_item)
                lines.extend(sub_lines)
        
        return lines
    
    tree_lines = [str(common_root)]
    if tree_dict:
        tree_lines.extend(format_tree(tree_dict))
    
    return "\n".join(tree_lines)

def generate_xml_prompt(files: List[str], instructions: str, use_xml_formatting: bool = True) -> str:
    """Generate XML format prompt."""
    prompt = ""
    
    # Add file map at the beginning
    file_tree = generate_file_tree(files)
    prompt += f"<file_map>\n{file_tree}\n</file_map>\n\n"
    
    # Add repository with all file contents
    prompt += "<file_contents>"
    
    for file_path in files:
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                content = file_manager.get_file_content(path)
                prompt += f"\n<file path='{path}'>\n{content}\n</file>\n"
        except Exception as e:
            prompt += f"\n<file path='{file_path}' error='{str(e)}'>\n[Could not read file]\n</file>\n"
    
    prompt += "</file_contents>\n"

    # add xml formatting instructions from the txt file
    if use_xml_formatting:
        prompt += f"\n{xml_formatting}"
    
    # Add user instructions at the very end
    if instructions:
        prompt += f"\n<user_instructions>\n{instructions}\n</user_instructions>"
    
    return prompt

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get current ignore settings."""
    return jsonify({
        'settings': file_manager.user_settings,
        'default_patterns': list(file_manager.default_ignored_patterns)
    })

@app.route('/api/settings', methods=['POST'])
def update_settings():
    """Update ignore settings."""
    data = request.get_json()
    settings = data.get('settings', {})
    
    file_manager.update_settings(settings)
    return jsonify({
        'success': True,
        'settings': file_manager.user_settings
    })

@app.route('/api/estimate-tokens', methods=['POST'])
def estimate_tokens():
    """Estimate token count for selected files by generating the actual prompt."""
    data = request.get_json()
    selected_files = data.get('files', [])
    instructions = data.get('instructions', '')
    model = data.get('model', 'gpt-4')
    use_xml_formatting = data.get('use_xml_formatting', True)
    
    try:
        # Set the model for token counting
        if model != token_counter.current_model:
            token_counter._load_encoding(model)
        
        # Generate the actual prompt based on format
        prompt = generate_xml_prompt(selected_files, instructions, use_xml_formatting)

        # Count tokens from the actual generated prompt
        total_tokens = token_counter.count_tokens(prompt)
        
        # Get per-file estimates for additional stats
        file_estimates = {}
        for file_path in selected_files:
            path = Path(file_path)
            if path.exists() and path.is_file():
                file_estimates[file_path] = token_counter.estimate_file_tokens(path)
        
        return jsonify({
            'total_tokens': total_tokens,
            'file_estimates': file_estimates,
            'model': model,
            'encoding': token_counter.encodings.get(model, 'cl100k_base')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models', methods=['GET'])
def get_supported_models():
    """Get list of supported models for token counting."""
    return jsonify({
        'models': list(token_counter.encodings.keys()),
        'current_model': token_counter.current_model
    })

# -------- DIFF PROCESSOR ROUTES --------

@app.route('/api/diff/parse', methods=['POST'])
def api_diff_parse():
    """Parse XML diff and return preview of changes."""
    data = request.get_json()
    xml_content = data.get('xml', '')
    
    if not xml_content:
        return jsonify({'error': 'No XML content provided'}), 400
    
    try:
        # Get project root from request data, defaulting to current directory
        project_root_str = data.get('project_root', '.')
        project_root = Path(project_root_str).expanduser().resolve()
        dp = DiffProcessor(project_root)
        
        # Parse the XML
        changes = dp.parse(xml_content)
        
        # Generate previews for each change
        previews = []
        change_dicts = []
        
        for change in changes:
            preview = dp.preview_diff(change)
            previews.append(preview)
            
            # Check if this change is already applied
            is_applied = dp.change_is_applied(change)
            
            # For modify actions, check individual changes
            individual_applied_states = []
            if change.action == 'modify' and change.changes:
                for idx, (search, replace) in enumerate(change.changes):
                    individual_applied_states.append(
                        dp.is_individual_change_applied(change.path, idx, search, replace)
                    )
            
            # Convert FileChange to dict for JSON serialization
            # Always use relative paths for consistency
            try:
                relative_path = str(change.path.relative_to(project_root))
            except ValueError:
                # Path is outside project root, use absolute path
                relative_path = str(change.path)
            
            change_dict = {
                'path': str(change.path),
                'action': change.action,
                'new_path': str(change.new_path) if change.new_path else None,
                'changes': change.changes,
                'content': change.content,
                'contents': getattr(change, 'contents', []),  # Include contents list
                'relative_path': relative_path,
                'applied': is_applied,
                'individual_applied': individual_applied_states if change.action == 'modify' else []
            }
            change_dicts.append(change_dict)
        
        return jsonify({
            'success': True,
            'changes': change_dicts,
            'previews': previews,
            'total_changes': len(changes)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diff/apply', methods=['POST'])
def api_diff_apply():
    """Apply selected file changes."""
    data = request.get_json()
    selected_changes = data.get('selected_changes', [])
    
    if not selected_changes:
        return jsonify({'error': 'No changes selected'}), 400
    
    try:
        project_root_str = data.get('project_root', '.')
        project_root = Path(project_root_str).expanduser().resolve()
        dp = DiffProcessor(project_root)
        
        results = []
        for change_dict in selected_changes:
            # Reconstruct FileChange object
            fc = FileChange(
                path=Path(change_dict['path']),
                action=change_dict['action'],
                new_path=Path(change_dict['new_path']) if change_dict.get('new_path') else None,
                changes=change_dict.get('changes', []),
                content=change_dict.get('content'),
                contents=change_dict.get('contents', [])
            )
            
            # Log for debugging
            print(f"Toggle request - Action: {fc.action}, Path: {fc.path}, Changes count: {len(fc.changes)}")
            if fc.action == 'modify' and fc.changes:
                print(f"First change preview: {fc.changes[0][0][:50]}... -> {fc.changes[0][1][:50]}...")
            
            # Check if already applied
            if dp.change_is_applied(fc):
                try:
                    relative_path = str(fc.path.relative_to(project_root))
                except ValueError:
                    relative_path = str(fc.path)
                results.append({
                    'success': False,
                    'error': 'Change already applied',
                    'path': relative_path
                })
                continue
            
            # Apply the change
            result = dp.apply(fc)
            results.append(result)
        
        # Count successes and failures
        successes = sum(1 for r in results if r['success'])
        failures = sum(1 for r in results if not r['success'])
        
        return jsonify({
            'success': True,
            'results': results,
            'summary': {
                'total': len(results),
                'succeeded': successes,
                'failed': failures
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diff/check-applied', methods=['POST'])
def api_diff_check_applied():
    """Check if changes are currently applied."""
    data = request.get_json()
    changes = data.get('changes', [])
    
    try:
        project_root_str = data.get('project_root', '.')
        project_root = Path(project_root_str).expanduser().resolve()
        dp = DiffProcessor(project_root)
        
        results = {}
        for change_dict in changes:
            # Reconstruct FileChange object
            fc = FileChange(
                path=Path(change_dict['path']),
                action=change_dict['action'],
                new_path=Path(change_dict['new_path']) if change_dict.get('new_path') else None,
                changes=change_dict.get('changes', []),
                content=change_dict.get('content')
            )
            
            # Check if applied and use relative path as key for consistency
            try:
                relative_path = str(fc.path.relative_to(project_root))
            except ValueError:
                relative_path = str(fc.path)
            
            results[relative_path] = dp.change_is_applied(fc)
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diff/toggle-change', methods=['POST'])
def api_diff_toggle_change():
    """Toggle an individual change within a file on/off."""
    data = request.get_json()
    file_path = data.get('file_path')
    change_index = data.get('change_index')
    search = data.get('search')
    replace = data.get('replace')
    apply = data.get('apply', True)
    
    if not file_path or change_index is None or not search or not replace:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        project_root_str = data.get('project_root', '.')
        project_root = Path(project_root_str).expanduser().resolve()
        dp = DiffProcessor(project_root)
        
        # Apply or revert the specific change
        if apply:
            result = dp.apply_individual_change(Path(file_path), change_index, search, replace)
        else:
            result = dp.revert_individual_change(Path(file_path), change_index, search, replace)
        
        if result['success']:
            return jsonify({
                'success': True,
                'applied': apply,
                'change_index': change_index,
                'backup': result.get('backup')
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Failed to toggle change')
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diff/toggle', methods=['POST'])
def api_diff_toggle():
    """Toggle a file change on/off."""
    data = request.get_json()
    change_dict = data.get('change')
    apply = data.get('apply', True)
    
    if not change_dict:
        return jsonify({'error': 'Missing change data'}), 400
    
    try:
        project_root_str = data.get('project_root', '.')
        project_root = Path(project_root_str).expanduser().resolve()
        dp = DiffProcessor(project_root)
        
        # Reconstruct FileChange object
        fc = FileChange(
            path=Path(change_dict['path']),
            action=change_dict['action'],
            new_path=Path(change_dict['new_path']) if change_dict.get('new_path') else None,
            changes=change_dict.get('changes', []),
            content=change_dict.get('content')
        )
        
        # Check current state - consider applied if ANY individual change is applied
        if fc.action == 'modify' and fc.changes:
            # For modify actions, check if any individual change is applied
            is_currently_applied = any(
                dp.is_individual_change_applied(fc.path, idx, search, replace)
                for idx, (search, replace) in enumerate(fc.changes)
            )
        else:
            # For other actions (create, delete, move), use the original logic
            is_currently_applied = dp.change_is_applied(fc)
        
        # Get relative path for response
        try:
            relative_path = str(fc.path.relative_to(project_root))
        except ValueError:
            relative_path = str(fc.path)
        
        if apply:
            if is_currently_applied:
                # Attempt to revert the change
                result = dp.revert(fc)
            
            # Apply the change
            result = dp.apply(fc)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'applied': True,
                    'path': relative_path,
                    'backup': result.get('backup')
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Failed to apply change')
                }), 500
                
        else:
            if not is_currently_applied:
                return jsonify({
                    'success': False,
                    'error': 'Change not currently applied'
                }), 400
            
            # Revert the change by doing the reverse operation
            result = dp.revert(fc)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'applied': False,
                    'path': relative_path,
                    'backup': result.get('backup')
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Failed to revert change')
                }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        # Clean up file watchers on shutdown
        stop_all_watchers()