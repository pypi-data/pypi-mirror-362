# ABOUTME: Tree generation module for directory structures
# Handles gitignore patterns and creates formatted tree output

import os
from pathlib import Path
from typing import Optional, List, Set
import pathspec


class TreeGenerator:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.gitignore_spec = self._load_gitignore_patterns(root_path)
        
    def _load_gitignore_patterns(self, path: Path) -> Optional[pathspec.GitIgnoreSpec]:
        gitignore_path = path / '.gitignore'
        if gitignore_path.exists():
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                return pathspec.GitIgnoreSpec.from_lines(f)
        return None
    
    def _is_ignored(self, file_path: Path) -> bool:
        if self.gitignore_spec is None:
            return False
        
        # Get relative path from root
        try:
            relative_path = file_path.relative_to(self.root_path)
            # Check if file matches gitignore patterns
            return self.gitignore_spec.match_file(str(relative_path))
        except ValueError:
            # Path is not relative to root
            return False
    
    def _should_skip(self, path: Path, show_hidden: bool) -> bool:
        # Skip if gitignored
        if self._is_ignored(path):
            return True
            
        # Skip hidden files/dirs if not requested
        if not show_hidden and path.name.startswith('.'):
            return True
            
        return False
    
    def _generate_tree_recursive(
        self, 
        path: Path, 
        prefix: str = "",
        is_last: bool = True,
        current_depth: int = 0,
        max_depth: Optional[int] = None,
        show_hidden: bool = False,
        visited_dirs: Optional[Set[Path]] = None
    ) -> List[str]:
        if visited_dirs is None:
            visited_dirs = set()
            
        # Prevent infinite loops from symlinks
        real_path = path.resolve()
        if real_path in visited_dirs:
            return [f"{prefix}{'└── ' if is_last else '├── '}{path.name}/ [circular reference]"]
        
        lines = []
        
        # Add current item
        if path != self.root_path:
            connector = "└── " if is_last else "├── "
            suffix = "/" if path.is_dir() else ""
            lines.append(f"{prefix}{connector}{path.name}{suffix}")
        
        # Stop if we've reached max depth
        if max_depth is not None and current_depth >= max_depth:
            if path.is_dir() and any(path.iterdir()):
                lines.append(f"{prefix}{'    ' if is_last else '│   '}└── ...")
            return lines
        
        # Process directory contents
        if path.is_dir():
            visited_dirs.add(real_path)
            
            try:
                # Get and sort entries
                entries = list(path.iterdir())
                entries.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
                
                # Filter entries
                filtered_entries = [
                    entry for entry in entries 
                    if not self._should_skip(entry, show_hidden)
                ]
                
                # Generate tree for each entry
                for idx, entry in enumerate(filtered_entries):
                    is_last_entry = idx == len(filtered_entries) - 1
                    
                    if path == self.root_path:
                        child_prefix = ""
                    else:
                        child_prefix = prefix + ("    " if is_last else "│   ")
                    
                    child_lines = self._generate_tree_recursive(
                        entry,
                        child_prefix,
                        is_last_entry,
                        current_depth + 1,
                        max_depth,
                        show_hidden,
                        visited_dirs
                    )
                    lines.extend(child_lines)
                    
            except PermissionError:
                lines.append(f"{prefix}{'    ' if is_last else '│   '}[Permission Denied]")
            except Exception as e:
                lines.append(f"{prefix}{'    ' if is_last else '│   '}[Error: {str(e)}]")
        
        return lines
    
    def generate_tree(
        self, 
        path: Optional[Path] = None,
        max_depth: Optional[int] = None,
        show_hidden: bool = False
    ) -> str:
        if path is None:
            path = self.root_path
        
        if not path.exists():
            return f"Error: Path '{path}' does not exist"
        
        # Reload gitignore patterns if we're looking at a different directory
        if path != self.root_path:
            self.root_path = path
            self.gitignore_spec = self._load_gitignore_patterns(path)
        
        # Generate tree
        lines = [str(path)]
        tree_lines = self._generate_tree_recursive(
            path, 
            max_depth=max_depth,
            show_hidden=show_hidden
        )
        lines.extend(tree_lines)
        
        # Add summary statistics
        total_dirs = sum(1 for line in tree_lines if line.rstrip().endswith('/'))
        total_files = len(tree_lines) - total_dirs
        
        lines.append("")
        if max_depth is not None:
            lines.append(f"{total_dirs} directories, {total_files} files (max depth: {max_depth})")
        else:
            lines.append(f"{total_dirs} directories, {total_files} files")
        
        return '\n'.join(lines)


def generate_directory_tree(
    path: str = ".",
    max_depth: Optional[int] = None,
    show_hidden: bool = False
) -> str:
    path_obj = Path(path).resolve()
    generator = TreeGenerator(path_obj)
    return generator.generate_tree(path_obj, max_depth, show_hidden)