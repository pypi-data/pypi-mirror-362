from pathlib import Path
from dataclasses import dataclass, field
import shutil
import re
from datetime import datetime
from typing import List, Optional, Dict, Tuple
import difflib
import json
import os
import hashlib

@dataclass
class FileChange:
    path: Path
    action: str                # create | rewrite | modify | delete | rename
    new_path: Optional[Path] = None
    changes: list = field(default_factory=list)  # for modify (list of (search, replace) tuples)
    content: Optional[str] = None                # for create/rewrite (final merged content)
    contents: list = field(default_factory=list) # for create/rewrite (list of individual content blocks)

class DiffProcessor:
    def __init__(self, project_root: Path):
        self.root = project_root
        
        # Get system cache directory
        self.backup_dir = self._get_backup_directory()
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Legacy backup directory for migration
        self.legacy_backup_dir = self.root / '.contextforge_backups'
        
        self.state_file = self.backup_dir / 'change_states.json'
        self.change_states = self._load_change_states()
    
    def _get_backup_directory(self) -> Path:
        """Get platform-specific cache directory for backups."""
        # Create a unique identifier for this project based on its path
        project_id = hashlib.md5(str(self.root.resolve()).encode()).hexdigest()[:12]
        project_name = self.root.name
        
        # Try to use platformdirs if available
        try:
            import platformdirs
            cache_dir = Path(platformdirs.user_cache_dir('contextforge', 'contextforge'))
        except ImportError:
            # Fallback to manual platform detection
            if os.name == 'nt':  # Windows
                cache_dir = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local')) / 'contextforge'
            elif os.name == 'posix':
                if 'darwin' in os.sys.platform:  # macOS
                    cache_dir = Path.home() / 'Library' / 'Caches' / 'contextforge'
                else:  # Linux and others
                    xdg_cache = os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache')
                    cache_dir = Path(xdg_cache) / 'contextforge'
            else:
                # Unknown platform, use home directory
                cache_dir = Path.home() / '.contextforge_cache'
        
        # Create subdirectory for this specific project
        backup_dir = cache_dir / 'backups' / f"{project_name}_{project_id}"
        return backup_dir
    
    def change_is_applied(self, fc: FileChange) -> bool:
        """Return True when the change described by `fc` is already present on disk."""
        if fc.action == "create":
            return fc.path.exists()
        if fc.action == "delete":
            return not fc.path.exists()
        if fc.action == "rename":
            return fc.new_path and fc.new_path.exists() and not fc.path.exists()
        if fc.action in {"rewrite", "modify"}:
            if not fc.path.exists():
                return False
            # Always read fresh content from disk
            current = fc.path.read_text(encoding="utf-8", errors="ignore")
            if fc.action == "rewrite":
                return current.strip() == (fc.content or "").strip()
            
            # For modify actions, we should instead check if the replace strings are all present
            for search, replace in fc.changes:
                if replace not in current:
                    return False
            return True
        return False
    
    def _load_change_states(self) -> Dict[str, Dict]:
        """Load saved change states from file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_change_states(self):
        """Save change states to file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.change_states, f, indent=2)
        except Exception:
            pass
    
    def _get_change_key(self, path: Path, change_index: int) -> str:
        """Generate a unique key for tracking individual changes."""
        try:
            rel_path = str(path.relative_to(self.root))
        except ValueError:
            rel_path = str(path)
        return f"{rel_path}:{change_index}"
    
    def is_individual_change_applied(self, path: Path, change_index: int, search: str, replace: str) -> bool:
        """Check if an individual search/replace change is applied."""
        if not path.exists():
            return False
        
        try:
            current = path.read_text(encoding="utf-8", errors="ignore")
            # Check if the replacement text exists
            # Also check our state tracking for more reliable detection
            key = self._get_change_key(path, change_index)
            state_says_applied = self.change_states.get(key, {}).get('applied', False)
            
            # Verify against actual file content
            replace_exists = replace in current
            
            # If state and reality disagree, trust reality
            actual_applied = replace_exists
            if state_says_applied != actual_applied:
                # Update state to match reality
                if actual_applied:
                    self.change_states[key] = {'applied': True, 'search': search, 'replace': replace}
                else:
                    self.change_states.pop(key, None)
                self._save_change_states()
            
            return actual_applied
        except Exception:
            return False
    
    def apply_individual_change(self, path: Path, change_index: int, search: str, replace: str) -> Dict[str, any]:
        """Apply a single search/replace change within a file."""
        result = {
            'success': False,
            'change_index': change_index,
            'path': str(path),
            'backup': None,
            'error': None
        }
        
        try:
            self.is_individual_change_applied(path, change_index, search, replace)

            if not path.exists():
                raise ValueError(f"File does not exist: {path}")
            
            if self.is_individual_change_applied(path, change_index, search, replace):
                raise ValueError(f"Change {change_index} is already applied")
            
            # Create backup before modifying
            backup = self.create_backup(path)
            if backup:
                result['backup'] = str(backup)
            
            # Read current content
            content = path.read_text(encoding='utf-8')
            
            # Apply the change
            if search not in content:
                raise ValueError(f"Search text not found in file for change {change_index}")
            
            new_content = content.replace(search, replace, 1)  # Only replace first occurrence
            
            # Write the modified content
            path.write_text(new_content, encoding='utf-8')
            
            # Track the change state
            key = self._get_change_key(path, change_index)
            self.change_states[key] = {
                'applied': True,
                'search': search,
                'replace': replace,
                'backup': str(backup) if backup else None
            }
            self._save_change_states()
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            
        return result
    
    def revert_individual_change(self, path: Path, change_index: int, search: str, replace: str) -> Dict[str, any]:
        """Revert a single search/replace change within a file."""
        result = {
            'success': False,
            'change_index': change_index,
            'path': str(path),
            'backup': None,
            'error': None
        }
        
        try:
            self.is_individual_change_applied(path, change_index, search, replace)

            if not path.exists():
                raise ValueError(f"File does not exist: {path}")
            
            if not self.is_individual_change_applied(path, change_index, search, replace):
                raise ValueError(f"Change {change_index} is not currently applied")
            
            # Create backup before reverting
            backup = self.create_backup(path)
            if backup:
                result['backup'] = str(backup)
            
            # Read current content
            content = path.read_text(encoding='utf-8')
            
            # Revert the change (replace back with search)
            if replace not in content:
                raise ValueError(f"Replace text not found in file for change {change_index}")
            
            new_content = content.replace(replace, search, 1)  # Only replace first occurrence
            
            # Write the reverted content
            path.write_text(new_content, encoding='utf-8')
            
            # Update change state
            key = self._get_change_key(path, change_index)
            self.change_states.pop(key, None)  # Remove from applied states
            self._save_change_states()
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            
        return result
        
    # -------- CUSTOM PARSER --------
    def parse(self, input_string: str) -> List[FileChange]:
        """Parse custom XML-like diff format with === delimited content blocks."""
        file_changes: List[FileChange] = []
        
        # Ensure input is a proper Unicode string
        if isinstance(input_string, bytes):
            input_string = input_string.decode('utf-8')
        
        # Clean input
        input_string = input_string.strip()
        
        # Remove outer ```
        if input_string.startswith('```xml'):
            input_string = input_string[6:]
        if input_string.startswith('```'):
            input_string = input_string[3:]
        if input_string.endswith('```'):
            input_string = input_string[:-3]
        input_string = input_string.strip()
        
        # Extract all file blocks
        file_blocks = self._extract_file_blocks(input_string)
        
        # Group file blocks by path
        blocks_by_path = {}
        for block in file_blocks:
            # Extract path from block
            file_match = re.match(r'<file\s+([^>]+)>', block)
            if file_match:
                attrs = self._parse_attributes(file_match.group(1))
                path_str = attrs.get('path', '').strip('"\'')
                
                if path_str:
                    if path_str not in blocks_by_path:
                        blocks_by_path[path_str] = []
                    blocks_by_path[path_str].append(block)
        
        # Process merged blocks for each unique path
        for path_str, blocks in blocks_by_path.items():
            file_change = self._parse_merged_file_blocks(path_str, blocks)
            if file_change:
                file_changes.append(file_change)
        
        return file_changes

    def _extract_file_blocks(self, content: str) -> List[str]:
        """Extract individual file blocks from the input."""
        blocks = []
        
        # Find all <file> tags and their corresponding closing tags
        # We need to be careful to match the correct closing tag
        file_pattern = re.compile(r'<file\s+[^>]+>', re.MULTILINE | re.DOTALL)
        
        pos = 0
        while True:
            match = file_pattern.search(content, pos)
            if not match:
                break
            
            start_pos = match.start()
            start_tag = match.group()
            
            # Find the matching closing </file> tag
            # Count nested <file> tags to ensure we get the right closing tag
            end_pos = self._find_closing_tag(content, match.end(), 'file')
            
            if end_pos == -1:
                # No closing tag found, skip this block
                pos = match.end()
                continue
            
            # Extract the complete block including tags
            block = content[start_pos:end_pos]
            blocks.append(block)
            
            pos = end_pos
        
        return blocks
    
    def _find_closing_tag(self, content: str, start_pos: int, tag_name: str) -> int:
        """Find the position after the closing tag, handling nested tags."""
        depth = 1
        pos = start_pos
        
        # Pattern to find either opening or closing tags
        tag_pattern = re.compile(rf'<(/)?{tag_name}(?:\s+[^>]*)?>') 
        
        while depth > 0 and pos < len(content):
            match = tag_pattern.search(content, pos)
            if not match:
                return -1
            
            if match.group(1):  # Closing tag
                depth -= 1
                if depth == 0:
                    return match.end()
            else:  # Opening tag
                depth += 1
            
            pos = match.end()
        
        return -1
    
    def _parse_merged_file_blocks(self, path_str: str, blocks: List[str]) -> Optional[FileChange]:
        """Parse and merge multiple file blocks for the same path."""
        # Resolve path
        if Path(path_str).is_absolute():
            path = Path(path_str).resolve()
        else:
            path = (self.root / path_str).resolve()
        
        # Collect all changes from all blocks
        all_changes = []
        all_contents = []
        action = None
        new_path = None
        
        for block in blocks:
            # Parse attributes
            file_match = re.match(r'<file\s+([^>]+)>', block)
            if not file_match:
                continue
                
            attrs = self._parse_attributes(file_match.group(1))
            block_action = attrs.get('action', '').strip('"\'').lower()
            
            # Set action (should be consistent across blocks)
            if action is None:
                action = block_action
            elif action != block_action:
                # Log warning about inconsistent actions
                print(f"Warning: Inconsistent actions for {path_str}: {action} vs {block_action}")
            
            # Handle rename
            new_path_match = re.search(r'<new\s+path\s*=\s*["\']([^"\']+)["\']', block)
            if new_path_match and new_path is None:
                new_path_str = new_path_match.group(1)
                if Path(new_path_str).is_absolute():
                    new_path = Path(new_path_str).resolve()
                else:
                    new_path = (self.root / new_path_str).resolve()
            
            # Extract changes from this block
            change_blocks = self._extract_change_blocks(block)
            
            for change_block in change_blocks:
                if action == 'modify':
                    search_text = self._extract_content_between_markers(change_block, 'search')
                    replace_text = self._extract_content_between_markers(change_block, 'content')
                    
                    if search_text is not None and replace_text is not None:
                        all_changes.append((search_text, replace_text))
                else:  # create or rewrite
                    content_text = self._extract_content_between_markers(change_block, 'content')
                    if content_text is not None:
                        all_contents.append(content_text)
        
        # Now validate all collected changes
        if action == 'modify' and path.exists():
            # Validate changes against actual file content
            try:
                file_content = path.read_text(encoding='utf-8')
                valid_changes = []
                
                # Apply changes sequentially to validate each one
                temp_content = file_content
                for search, replace in all_changes:
                    if search in temp_content:
                        valid_changes.append((search, replace))
                        temp_content = temp_content.replace(search, replace, 1)
                
                # Always return a FileChange, even if empty
                return FileChange(
                    path=path,
                    action=action,
                    new_path=new_path,
                    changes=valid_changes,
                    content=None,
                    contents=[]
                )
            except Exception:
                # If file can't be read, return with all changes (let apply handle the error)
                return FileChange(
                    path=path,
                    action=action,
                    new_path=new_path,
                    changes=all_changes,
                    content=None,
                    contents=[]
                )
        
        # For non-modify actions or if file doesn't exist
        if all_contents:
            content = all_contents[-1]  # Use last content as before
        else:
            content = None
        
        return FileChange(
            path=path,
            action=action,
            new_path=new_path,
            changes=all_changes if action == 'modify' else [],
            content=content,
            contents=all_contents if action in {'create', 'rewrite'} else []
        )

    def _parse_file_block(self, block: str) -> Optional[FileChange]:
        """Parse a single file block."""
        # Extract file attributes
        file_match = re.match(r'<file\s+([^>]+)>', block)
        if not file_match:
            return None
        
        attrs_str = file_match.group(1)
        attrs = self._parse_attributes(attrs_str)
        
        path_str = attrs.get('path', '').strip('"\'')
        action = attrs.get('action', '').strip('"\'').lower()
        
        if not path_str or not action:
            return None
        
        # Resolve path - handle both relative and absolute paths
        if Path(path_str).is_absolute():
            path = Path(path_str).resolve()
        else:
            path = (self.root / path_str).resolve()
        
        # Handle rename action - look for <new path="..."/>
        new_path = None
        new_path_match = re.search(r'<new\s+path\s*=\s*["\']([^"\']+)["\']', block)
        if new_path_match:
            new_path_str = new_path_match.group(1)
            # Handle both relative and absolute paths for rename
            if Path(new_path_str).is_absolute():
                new_path = Path(new_path_str).resolve()
            else:
                new_path = (self.root / new_path_str).resolve()
        
        # Extract change blocks
        changes = []
        contents = []
        content = None
        
        if action in {'create', 'rewrite', 'modify'}:
            # For modify actions, first read the file content to validate changes
            file_content_for_validation = None
            if action == 'modify' and path.exists():
                try:
                    file_content_for_validation = path.read_text(encoding='utf-8')
                except Exception:
                    file_content_for_validation = None

            change_blocks = self._extract_change_blocks(block)
            
            for change_block in change_blocks:
                if action == 'modify':
                    search_text = self._extract_content_between_markers(change_block, 'search')
                    replace_text = self._extract_content_between_markers(change_block, 'content')
                    
                    # Only add the change if it's valid
                    if search_text is not None and replace_text is not None:
                        # If we have file content, validate that the search block exists
                        if file_content_for_validation:
                            if search_text in file_content_for_validation:
                                changes.append((search_text, replace_text))
                                # Apply change to our temporary content to validate subsequent changes
                                file_content_for_validation = file_content_for_validation.replace(search_text, replace_text, 1)
                        else:
                             # If file doesn't exist, we can't validate, so we add it tentatively
                            changes.append((search_text, replace_text))

                else: # create or rewrite
                    content_text = self._extract_content_between_markers(change_block, 'content')
                    if content_text is not None:
                        contents.append(content_text)
        
        # For create/rewrite, merge all contents (last one wins for now, matching current behavior)
        if contents:
            content = contents[-1]  # Use the last content block as the final content
        
        return FileChange(
            path=path,
            action=action,
            new_path=new_path,
            changes=changes,
            content=content,
            contents=contents if action in {'create', 'rewrite'} else []
        )
    
    def _parse_attributes(self, attrs_str: str) -> Dict[str, str]:
        """Parse attributes from a tag."""
        attrs = {}
        # Match attribute patterns like: key="value" or key='value'
        attr_pattern = re.compile(r'(\w+)\s*=\s*["\']([^"\']*)["\']')
        
        for match in attr_pattern.finditer(attrs_str):
            key = match.group(1)
            value = match.group(2)
            attrs[key] = value
        
        return attrs
    
    def _extract_change_blocks(self, file_block: str) -> List[str]:
        """Extract all <change> blocks from a file block."""
        blocks = []
        
        # Find all <change> blocks
        pos = 0
        while True:
            start_match = re.search(r'<change>', file_block[pos:])
            if not start_match:
                break
            
            # Adjust match positions to account for slicing
            actual_start = pos + start_match.start()
            actual_end = pos + start_match.end()
            
            # Find the matching </change>
            end_pos = self._find_simple_closing_tag(file_block, actual_end, 'change')
            if end_pos == -1:
                break
            
            block = file_block[actual_start:end_pos]
            blocks.append(block)
            
            pos = end_pos
        
        return blocks
    
    def _find_simple_closing_tag(self, content: str, start_pos: int, tag_name: str) -> int:
        """Find closing tag position for simple tags (no nesting expected)."""
        pattern = re.compile(rf'</{tag_name}>')
        match = pattern.search(content, start_pos)
        return match.end() if match else -1
    
    def _extract_content_between_markers(self, block: str, tag_name: str) -> Optional[str]:
        """Extract content between === markers within a specific tag."""
        # First, find the tag boundaries
        tag_start = re.search(rf'<{tag_name}>', block)
        if not tag_start:
            return None
        
        tag_end = re.search(rf'</{tag_name}>', block[tag_start.end():])
        if not tag_end:
            return None
        
        # Extract the content between the tags
        # Adjust tag_end position since it's relative to the slice
        tag_end_pos = tag_start.end() + tag_end.start()
        tag_content = block[tag_start.end():tag_end_pos]
        
        # Now look for === markers
        # Match content between === markers, handling multiline content
        marker_pattern = re.compile(r'===\s*\n(.*?)\n\s*===', re.DOTALL)
        match = marker_pattern.search(tag_content)
        
        if match:
            # Return the content between the markers
            return match.group(1)
        
        # Fallback: if no === markers, try to extract any text content
        # (for backward compatibility or simpler formats)
        stripped = tag_content.strip()
        if stripped:
            return stripped
        
        return None
    
    # -------- DIFF / PREVIEW --------
    def preview_diff(self, fc: FileChange) -> str:
        """Generate a unified diff preview for a file change."""
        # Check if change is already applied FIRST
        if self.change_is_applied(fc):
            return ""  # nothing to preview - change is already applied
            
        if fc.action in {"create", "rewrite"}:
            if fc.action == "create":
                old_lines = []
                from_file = "/dev/null"
            else:
                if fc.path.exists():
                    old_lines = fc.path.read_text(encoding='utf-8').splitlines(keepends=True)
                else:
                    old_lines = []
                try:
                    from_file = str(fc.path.relative_to(self.root.resolve()))
                except ValueError:
                    # Path is outside project root, use absolute path
                    from_file = str(fc.path)
            
            new_lines = fc.content.splitlines(keepends=True) if fc.content else []
            try:
                to_file = str(fc.path.relative_to(self.root.resolve()))
            except ValueError:
                # Path is outside project root, use absolute path
                to_file = str(fc.path)
            
            return "".join(difflib.unified_diff(
                old_lines, new_lines, 
                fromfile=from_file, 
                tofile=to_file,
                lineterm=''
            ))
            
        elif fc.action == "delete":
            if fc.path.exists():
                old_lines = fc.path.read_text(encoding='utf-8').splitlines(keepends=True)
            else:
                try:
                    rel_path = fc.path.relative_to(self.root.resolve())
                    return f"File {rel_path} does not exist\n"
                except ValueError:
                    return f"File {fc.path} does not exist\n"
                
            return "".join(difflib.unified_diff(
                old_lines, [], 
                fromfile=str(fc.path.relative_to(self.root.resolve())) if fc.path.is_relative_to(self.root.resolve()) else str(fc.path),
                tofile="/dev/null",
                lineterm=''
            ))
            
        elif fc.action == "rename":
            try:
                rel_path = fc.path.relative_to(self.root.resolve())
            except ValueError:
                rel_path = fc.path
            
            try:
                new_rel_path = fc.new_path.relative_to(self.root.resolve()) if fc.new_path else "unknown"
            except ValueError:
                new_rel_path = fc.new_path if fc.new_path else "unknown"
            
            return f"RENAME: {rel_path} → {new_rel_path}\n"
            
        elif fc.action == "modify":
            if not fc.path.exists():
                try:
                    rel_path = fc.path.relative_to(self.root.resolve())
                    return f"ERROR: File {rel_path} does not exist\n"
                except ValueError:
                    return f"ERROR: File {fc.path} does not exist\n"

            # Work with a single up-to-date copy of the file
            current_text = fc.path.read_text(encoding="utf-8")
            rel_path = (
                fc.path.relative_to(self.root.resolve())
                if fc.path.is_relative_to(self.root.resolve())
                else fc.path
            )

            previews = []
            valid_change_count = 0
            for idx, (search, replace) in enumerate(fc.changes, start=1):
                if search not in current_text:
                    snippet = search[:80] + "..." if len(search) > 80 else search
                    previews.append(
                        f"⚠️  Change {idx}: search block not found:\n{snippet}\n"
                    )
                    continue

                valid_change_count += 1
                next_text = current_text.replace(search, replace, 1)

                diff = difflib.unified_diff(
                    current_text.splitlines(keepends=True),
                    next_text.splitlines(keepends=True),
                    fromfile=f"{rel_path} (before {idx})",
                    tofile=f"{rel_path} (after  {idx})",
                    lineterm="",
                    n=3,  # a little context around each change
                )
                previews.append("".join(diff))

                # Move forward so subsequent diffs are relative to the latest state
                current_text = next_text

            return "\n\n".join(previews)
        
        return ""
    
    # -------- BACKUP --------
    def create_backup(self, path: Path) -> Optional[Path]:
        """Create a timestamped backup of a file."""
        if not path.exists():
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        # Include relative path in backup name to avoid conflicts
        try:
            rel_path = path.relative_to(self.root)
            # Replace path separators with underscores for the filename
            safe_rel_path = str(rel_path).replace(os.sep, '_').replace('/', '_')
            backup_name = f"{safe_rel_path}.{timestamp}.bak"
        except ValueError:
            # If path is outside project root, just use the filename
            backup_name = f"{path.name}.{timestamp}.bak"
        
        backup_path = self.backup_dir / backup_name
        
        # Ensure backup directory exists (in case it was deleted)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(path, backup_path)
        
        # Also save metadata about the backup
        metadata_path = backup_path.with_suffix('.bak.json')
        metadata = {
            'original_path': str(path),
            'project_root': str(self.root),
            'timestamp': timestamp,
            'relative_path': str(rel_path) if 'rel_path' in locals() else None
        }
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return backup_path
    
    # -------- APPLY --------
    def apply(self, fc: FileChange) -> Dict[str, any]:
        """Apply a single file change and return result info."""
        result = {
            'success': False,
            'action': fc.action,
            'path': str(fc.path),
            'backup': None,
            'error': None
        }
        
        try:
            if fc.action == "create":
                if fc.path.exists():
                    raise ValueError(f"File already exists: {fc.path}")
                fc.path.parent.mkdir(parents=True, exist_ok=True)
                fc.path.write_text(fc.content or "", encoding='utf-8')
                result['success'] = True
                
            elif fc.action == "rewrite":
                backup = self.create_backup(fc.path)
                if backup:
                    result['backup'] = str(backup)
                fc.path.write_text(fc.content or "", encoding='utf-8')
                result['success'] = True
                
            elif fc.action == "delete":
                if not fc.path.exists():
                    raise ValueError(f"File does not exist: {fc.path}")
                backup = self.create_backup(fc.path)
                if backup:
                    result['backup'] = str(backup.relative_to(self.root.resolve()))
                fc.path.unlink()
                result['success'] = True
                
            elif fc.action == "rename":
                if not fc.path.exists():
                    raise ValueError(f"File does not exist: {fc.path}")
                if not fc.new_path:
                    raise ValueError("No new path specified for rename")
                if fc.new_path.resolve() == fc.path.resolve():
                    raise ValueError("New path equals old path")
                if fc.new_path.exists():
                    raise ValueError(f"Target file already exists: {fc.new_path}")
                fc.new_path.parent.mkdir(parents=True, exist_ok=True)
                fc.path.rename(fc.new_path)
                result['new_path'] = str(fc.new_path)
                result['success'] = True
                
            elif fc.action == "modify":
                if not fc.path.exists():
                    raise ValueError(f"File does not exist: {fc.path}")
                    
                backup = self.create_backup(fc.path)
                if backup:
                    result['backup'] = str(backup)
                    
                text = fc.path.read_text(encoding='utf-8')
                for search, replace in fc.changes:
                    if search not in text:
                        # Provide more context about what wasn't found
                        preview = search[:100] + "..." if len(search) > 100 else search
                        lines = search.split('\n')
                        line_info = f" ({len(lines)} lines)" if len(lines) > 1 else ""
                        raise ValueError(f"Search block not found in {fc.path.name}{line_info}: {preview}")
                    text = text.replace(search, replace, 1)
                    
                fc.path.write_text(text, encoding='utf-8')
                result['success'] = True
                
        except Exception as e:
            result['error'] = str(e)
            
        return result
    
    # -------- UNDO --------
    def get_recent_backups(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get list of recent backups."""
        backups = []
        if not self.backup_dir.exists():
            return backups
            
        for backup_file in sorted(self.backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if backup_file.is_file() and backup_file.suffix == '.bak':
                # Try to load metadata
                metadata_path = backup_file.with_suffix('.bak.json')
                metadata = {}
                if metadata_path.exists():
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                    except:
                        pass
                
                # Extract info from filename as fallback
                parts = backup_file.stem.split('.')
                if len(parts) >= 2:
                    # New format: path_components.timestamp
                    original_name = '.'.join(parts[:-1]).replace('_', os.sep)
                    timestamp = parts[-1]
                else:
                    original_name = backup_file.stem
                    timestamp = 'unknown'
                
                # Use metadata if available, otherwise use extracted info
                backup_info = {
                    'backup_path': str(backup_file),
                    'original_name': original_name,
                    'original_path': metadata.get('original_path', ''),
                    'timestamp': timestamp,
                    'size': backup_file.stat().st_size,
                    'relative_path': metadata.get('relative_path', original_name)
                }
                backups.append(backup_info)
                
                if len(backups) >= limit:
                    break
        
        return backups
    
    def restore_backup(self, backup_path: Path, target_path: Path) -> bool:
        """Restore a backup file to its original location."""
        if not backup_path.exists():
            raise ValueError(f"Backup file not found: {backup_path}")
            
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup_path, target_path)
        return True

    # -------- REVERT --------
    def revert(self, fc: FileChange) -> Dict[str, any]:
        """Revert a change by doing the reverse operation."""
        result = {
            'success': False,
            'action': f'revert_{fc.action}',
            'path': str(fc.path),
            'backup': None,
            'error': None
        }
        
        try:
            if fc.action == "create":
                # Delete the created file
                if not fc.path.exists():
                    raise ValueError(f"File to revert does not exist: {fc.path}")
                backup = self.create_backup(fc.path)
                if backup:
                    result['backup'] = str(backup)
                fc.path.unlink()
                result['success'] = True
                
            elif fc.action == "delete":
                # Try to restore from a backup
                backups = self.get_recent_backups(limit=50)  # Check more backups
                
                # Find a backup for this specific file
                found_backup = None
                for backup_info in backups:
                    # Check both original_path and original_name for compatibility
                    matches = False
                    if backup_info.get('original_path'):
                        matches = Path(backup_info['original_path']) == fc.path
                    else:
                        # Fallback to name matching for old backups
                        matches = backup_info['original_name'] == fc.path.name or \
                                 backup_info['original_name'].endswith(fc.path.name)
                    
                    if matches:
                        backup_path = Path(backup_info['backup_path'])
                        if backup_path.exists():
                            found_backup = backup_path
                            break
                
                if found_backup:
                    # Restore from backup
                    fc.path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(found_backup, fc.path)
                    result['success'] = True
                    result['restored_from_backup'] = str(found_backup)
                else:
                    # No backup found, can't revert
                    raise ValueError("Cannot revert delete action - no backup found")
                
            elif fc.action == "rename":
                # Reverse the rename
                if not fc.new_path or not fc.new_path.exists():
                    raise ValueError(f"Cannot reverse rename - target file not found: {fc.new_path}")
                if fc.path.exists():
                    raise ValueError(f"Cannot reverse rename - original path already exists: {fc.path}")
                fc.new_path.rename(fc.path)
                result['success'] = True
                
            elif fc.action == "rewrite":
                # Try to restore from a backup
                if not fc.path.exists():
                    raise ValueError(f"File to revert does not exist: {fc.path}")
                    
                backups = self.get_recent_backups(limit=50)  # Check more backups
                
                # Find a backup for this specific file
                found_backup = None
                for backup_info in backups:
                    if backup_info['original_name'] == fc.path.name:
                        backup_path = Path(backup_info['backup_path'])
                        if backup_path.exists():
                            # Verify this backup is from before the rewrite
                            # by checking if content differs from current
                            try:
                                backup_content = backup_path.read_text(encoding='utf-8')
                                current_content = fc.path.read_text(encoding='utf-8')
                                if backup_content.strip() != current_content.strip():
                                    found_backup = backup_path
                                    break
                            except Exception:
                                # If we can't read files, skip this backup
                                continue
                
                if found_backup:
                    # Create a new backup of current state before reverting
                    new_backup = self.create_backup(fc.path)
                    if new_backup:
                        result['backup'] = str(new_backup)
                    
                    # Restore from the found backup
                    shutil.copy2(found_backup, fc.path)
                    result['success'] = True
                    result['restored_from_backup'] = str(found_backup)
                else:
                    # No suitable backup found
                    raise ValueError("Cannot revert rewrite action - no suitable backup found")
                
            elif fc.action == "modify":
                if not fc.path.exists():
                    raise ValueError(f"File does not exist: {fc.path}")
                
                # First try to restore from backup if available
                backups = self.get_recent_backups(limit=50)
                found_backup = None
                
                for backup_info in backups:
                    if backup_info['original_name'] == fc.path.name:
                        backup_path = Path(backup_info['backup_path'])
                        if backup_path.exists():
                            # Verify this backup is from before the modification
                            try:
                                backup_content = backup_path.read_text(encoding='utf-8')
                                current_content = fc.path.read_text(encoding='utf-8')
                                if backup_content.strip() != current_content.strip():
                                    found_backup = backup_path
                                    break
                            except Exception:
                                continue
                
                if found_backup:
                    # Restore from backup
                    new_backup = self.create_backup(fc.path)
                    if new_backup:
                        result['backup'] = str(new_backup)
                    
                    shutil.copy2(found_backup, fc.path)
                    result['success'] = True
                    result['restored_from_backup'] = str(found_backup)
                else:
                    # Fallback to simple text replacement
                    backup = self.create_backup(fc.path)
                    if backup:
                        result['backup'] = str(backup)
                        
                    text = fc.path.read_text(encoding='utf-8')
                    
                    # Reverse each change: replace the "replace" text back with "search" text
                    for search, replace in fc.changes:
                        if replace not in text:
                            raise ValueError(f"Cannot revert - replacement text not found: {replace[:50]}...")
                        text = text.replace(replace, search, 1)  # Only replace first occurrence
                        
                    fc.path.write_text(text, encoding='utf-8')
                    result['success'] = True
                
        except Exception as e:
            result['error'] = str(e)
            
        return result