#!/usr/bin/env python3
"""
    ╔════════════════════════════════════════════════════════════════════════════════╗
    ║                                                                                ║
    ║       █████╗ ██████╗  ██████╗██╗  ██╗██╗████████╗███████╗ ██████╗████████╗     ║
    ║      ██╔══██╗██╔══██╗██╔════╝██║  ██║██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝     ║
    ║      ███████║██████╔╝██║     ███████║██║   ██║   █████╗  ██║        ██║        ║
    ║      ██╔══██║██╔══██╗██║     ██╔══██║██║   ██║   ██╔══╝  ██║        ██║        ║
    ║      ██║  ██║██║  ██║╚██████╗██║  ██║██║   ██║   ███████╗╚██████╗   ██║        ║
    ║      ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝        ║
    ║                                                                                ║
    ║                           CLI File structure builder                           ║
    ║                                    v 1.0.0                                     ║                                                                                                ║
    ╚════════════════════════════════════════════════════════════════════════════════╝
                                                                     
"""

import os
import sys
import argparse
from pathlib import Path
import re
import json
import yaml
from typing import List, Dict, Any, Optional

class ArchitectureBuilder:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        
    def parse_tree_structure(self, content):
        lines = content.strip().split('\n')
        structure = []
        
        for line in lines:
            if not line.strip() or line.strip() == '---':
                continue
                
            indent_level = self._calculate_indent_level(line)
            
            name = self._extract_name(line)
            #print(f"DEBUG: Line: '{line}' -> Level: {indent_level}, Name: '{name}'")

            if name:
                is_directory = name.endswith('/')
                if is_directory:
                    name = name[:-1]
                
                structure.append({
                    'name': name,
                    'level': indent_level,
                    'is_directory': is_directory,
                    'path': None
                })
        
        return self._build_paths(structure)
    
    def _calculate_indent_level(self, line):
        if not line.strip():
            return 0

        # Find where the actual content starts
        content_match = re.search(r'[^\s│├└─]+', line)
        if not content_match:
            return 0

        prefix = line[:content_match.start()]

        if any(char in prefix for char in ['│', '├', '└', '─']):
            return self._calculate_tree_level(prefix)

        return self._calculate_regular_indent_level(prefix)
    
    def _calculate_tree_level(self, prefix):
        level = 0
        i = 0

        while i < len(prefix):
            # Check for 4-character tree patterns
            if i + 4 <= len(prefix):
                four_chars = prefix[i:i+4]
                if four_chars in ['│   ', '    ']:
                    level += 1
                    i += 4
                    continue
                elif four_chars[:3] in ['├──', '└──']:
                    level += 1
                    break
                
            # Check for 3-character tree patterns
            if i + 3 <= len(prefix):
                three_chars = prefix[i:i+3]
                if three_chars in ['├──', '└──']:
                    level += 1
                    break
                
            i += 1

        return level

    def _calculate_regular_indent_level(self, prefix):
        tab_count = prefix.count('\t')
        if tab_count > 0:
            return tab_count

        space_count = len(prefix)
        if space_count == 0:
            return 0

        for indent_size in [2, 4, 8]:
            if space_count % indent_size == 0:
                return space_count // indent_size

        # Fallback: assume 4-space indentation
        return space_count // 4

    def _auto_detect_indentation(self, lines):
        """Auto-detect the indentation style from the content"""
        indent_sizes = []
        
        for line in lines:
            if not line.strip():
                continue
                
            # Skip tree characters
            if any(char in line for char in ['│', '├', '└', '─']):
                continue
                
            # Count leading spaces
            leading_spaces = len(line) - len(line.lstrip(' '))
            if leading_spaces > 0:
                indent_sizes.append(leading_spaces)
        
        if not indent_sizes:
            return 4  # Default
        
        import math
        gcd = indent_sizes[0]
        for size in indent_sizes[1:]:
            gcd = math.gcd(gcd, size)
        
        return gcd if gcd > 0 else 4

    def _extract_name(self, line):
        name = re.sub(r'^[\s│├└─]+', '', line).strip()
        
        if '#' in name:
            name = name.split('#')[0].strip()
        
        return name
    
    def _build_paths(self, structure):
        if not structure:
            return structure

        path_stack = []

        for item in structure:
            level = item['level']

            path_stack = path_stack[:level]

            if path_stack:
                full_path = '/'.join(path_stack + [item['name']])
            else:
                full_path = item['name']

            item['path'] = full_path

            if item['is_directory']:
                path_stack.append(item['name'])

        return structure
    
    def create_structure(self, structure, dry_run=False):
        created_items = []

        for item in structure:
            full_path = self.base_path / item['path']

            if dry_run:
                action = "MKDIR" if item['is_directory'] else "TOUCH"
                print(f"[DRY RUN] {action}: {full_path}")
                created_items.append(str(full_path))
                continue
            
            try:
                if item['is_directory']:
                    full_path.mkdir(parents=True, exist_ok=True)
                    print(f"✓ Directory created: {full_path}")
                else:
                    # Ensure parent directories exist
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.touch()
                    print(f"✓ File created: {full_path}")

                created_items.append(str(full_path))

            except Exception as e:
                print(f"✗ Error while creating {full_path}: {e}")

        return created_items
    
    def create_structure_interactive(self, structure):
        created_items = []
        overwrite_all = False
        
        for item in structure:
            full_path = self.base_path / item['path']
            
            if full_path.exists() and not overwrite_all:
                choice = input(f"⚠ Path '{full_path}' already exists. Overwrite? (y/n/all/cancel): ").lower().strip()
                if choice == 'n':
                    print(f"✗ Skipped: {full_path}")
                    continue
                elif choice == 'cancel':
                    print("Operation cancelled by user.")
                    return []
                elif choice == 'all':
                    overwrite_all = True
                elif choice != 'y':
                    print(f"✗ Invalid choice. Skipped: {full_path}")
                    continue
            
            try:
                if item['is_directory']:
                    full_path.mkdir(parents=True, exist_ok=True)
                    print(f"✓ Directory created/updated: {full_path}")
                else:
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.touch(exist_ok=True)
                    print(f"✓ File created/updated: {full_path}")
                
                created_items.append(str(full_path))
                
            except Exception as e:
                print(f"✗ Error while creating {full_path}: {e}")
        
        return created_items

    def parse_from_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_tree_structure(content)
        except Exception as e:
            print(f"Error while reading file {file_path}: {e}")
            return []

class DirectoryScanner:
    def __init__(self, ignore_patterns=None):
        self.ignore_patterns = ignore_patterns or [
            '.git', '__pycache__', '.DS_Store', 'node_modules', '.env',
            '*.pyc', '*.pyo', '*.pyd', '.pytest_cache', '.vscode'
        ]
    
    def should_ignore(self, path: Path) -> bool:
        for pattern in self.ignore_patterns:
            if pattern.startswith('*'):
                if path.name.endswith(pattern[1:]):
                    return True
            else:
                if path.name == pattern:
                    return True
        return False
    
    def scan_directory(self, directory: Path, max_depth: Optional[int] = None) -> List[Dict[str, Any]]:
        if not directory.exists():
            raise FileNotFoundError(f"Le dossier {directory} n'existe pas")
        
        if not directory.is_dir():
            raise ValueError(f"{directory} n'est pas un dossier")
        
        structure = []
        self._scan_recursive(directory, structure, 0, max_depth)
        return structure
    
    def _scan_recursive(self, current_path: Path, structure: List[Dict], level: int, max_depth: Optional[int]):
        if max_depth is not None and level > max_depth:
            return
        
        try:
            items = sorted(current_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for item in items:
                if self.should_ignore(item):
                    continue
                
                relative_path = item.relative_to(current_path.parent) if level == 0 else item.relative_to(current_path.parents[level])
                
                item_info = {
                    'name': item.name,
                    'level': level,
                    'is_directory': item.is_dir(),
                    'path': str(relative_path),
                    'size': item.stat().st_size if item.is_file() else None,
                    'modified': item.stat().st_mtime
                }
                
                structure.append(item_info)
                
                if item.is_dir():
                    self._scan_recursive(item, structure, level + 1, max_depth)
                    
        except PermissionError:
            print(f"⚠  Permission denied for {current_path}")
        except Exception as e:
            print(f"⚠  Error while scanning {current_path}: {e}")

class StructureFormatter:
    @staticmethod
    def to_tree_ascii(structure: List[Dict], show_size: bool = False, folder_name: str = None) -> str:
        if not structure:
            return ""

        result = []
        
        # Add header if folder_name is provided
        if folder_name:
            result.append(f"{folder_name}/")
        
        prefix_stack = []

        for i, item in enumerate(structure):
            level = item['level']
            name = item['name']
            is_dir = item['is_directory']
            
            is_last = True
            for j in range(i + 1, len(structure)):
                if structure[j]['level'] < level:
                    break
                if structure[j]['level'] == level:
                    is_last = False
                    break
            
            while len(prefix_stack) > level:
                prefix_stack.pop()
            
            prefix = "".join(prefix_stack)
            
            connector = "└── " if is_last else "├── "
            
            display_name = f"{name}/" if is_dir else name
            if show_size and not is_dir and item.get('size') is not None:
                size_str = StructureFormatter._format_size(item['size'])
                display_name += f" ({size_str})"
            
            result.append(prefix + connector + display_name)
            
            prefix_stack.append("    " if is_last else "│   ")
            
        return "\n".join(result)
    
    @staticmethod
    def to_simple_tree(structure: List[Dict], show_size: bool = False, folder_name: str = None) -> str:
        if not structure:
            return ""
        
        result = []
        
        # Add header if folder_name is provided
        if folder_name:
            result.append(f"Structure of {folder_name}")
            result.append("")
            result.append(f"{folder_name}/")
        
        for item in structure:
            indent = "  " * item['level']
            name = item['name']
            is_dir = item['is_directory']
            
            display_name = f"{name}/" if is_dir else name
            
            if show_size and not is_dir and item.get('size') is not None:
                size_str = StructureFormatter._format_size(item['size'])
                display_name += f" ({size_str})"
            
            result.append(indent + display_name)
        
        return "\n".join(result)
    
    @staticmethod
    def to_json(structure: List[Dict], pretty: bool = True) -> str:
        hierarchy = StructureFormatter._build_hierarchy(structure)
        
        if pretty:
            return json.dumps(hierarchy, indent=2, ensure_ascii=False)
        else:
            return json.dumps(hierarchy, ensure_ascii=False)
    
    @staticmethod
    def to_yaml(structure: List[Dict]) -> str:
        hierarchy = StructureFormatter._build_hierarchy(structure)
        
        try:
            return yaml.dump(hierarchy, default_flow_style=False, allow_unicode=True, sort_keys=False)
        except ImportError:
            return "✘ PyYAML is not installed. Install it with: pip install pyyaml"
    
    @staticmethod
    def to_xml(structure: List[Dict]) -> str:
        result = ['<?xml version="1.0" encoding="UTF-8"?>']
        result.append('<directory_structure>')
        
        for item in structure:
            indent = "  " * (item['level'] + 1)
            tag = "directory" if item['is_directory'] else "file"
            name = item['name']
            
            if item['is_directory']:
                result.append(f'{indent}<{tag} name="{name}"/>')
            else:
                size = item.get('size', 0)
                result.append(f'{indent}<{tag} name="{name}" size="{size}"/>')
        
        result.append('</directory_structure>')
        return "\n".join(result)
    
    @staticmethod
    def to_markdown(structure: List[Dict], show_size: bool = False, folder_name: str = None) -> str:
        result = []
        
        if folder_name:
            result.append(f"# Structure of {folder_name}")
            result.append("")
        else:
            result.append("# Directory Structure")
            result.append("")
        
        for item in structure:
            indent = "  " * item['level']
            name = item['name']
            is_dir = item['is_directory']
            
            if is_dir:
                result.append(f"{indent}- 🗁  {name}/")
            else:
                size_info = ""
                if show_size and item.get('size') is not None:
                    size_info = f" `({StructureFormatter._format_size(item['size'])})`"
                result.append(f"{indent}- 🗎 {name}{size_info}")
        
        return "\n".join(result)
    
    @staticmethod
    def _build_hierarchy(structure: List[Dict]) -> Dict:
        if not structure:
            return {}
        
        root = {"name": "root", "type": "directory", "children": []}
        stack = [root]
        
        for item in structure:
            level = item['level']
            
            stack = stack[:level + 1]
            
            element = {
                "name": item['name'],
                "type": "directory" if item['is_directory'] else "file",
                "path": item['path']
            }
            
            if not item['is_directory']:
                element["size"] = item.get('size', 0)
            else:
                element["children"] = []
            
            if stack:
                parent = stack[-1]
                if "children" not in parent:
                    parent["children"] = []
                parent["children"].append(element)
            
            if item['is_directory']:
                stack.append(element)
        
        return root
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        if size_bytes == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        i = 0
        while size_bytes >= 1024 and i < len(units) - 1:
            size_bytes /= 1024
            i += 1
        
        return f"{size_bytes:.1f} {units[i]}"

def run_interactive_mode():
    print("    ╔════════════════════════════════════════════════════════════════════════════════╗")
    print("    ║                                                                                ║")
    print("    ║       █████╗ ██████╗  ██████╗██╗  ██╗██╗████████╗███████╗ ██████╗████████╗     ║")
    print("    ║      ██╔══██╗██╔══██╗██╔════╝██║  ██║██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝     ║")
    print("    ║      ███████║██████╔╝██║     ███████║██║   ██║   █████╗  ██║        ██║        ║")
    print("    ║      ██╔══██║██╔══██╗██║     ██╔══██║██║   ██║   ██╔══╝  ██║        ██║        ║")
    print("    ║      ██║  ██║██║  ██║╚██████╗██║  ██║██║   ██║   ███████╗╚██████╗   ██║        ║")
    print("    ║      ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝        ║")
    print("    ║                                                                                ║")
    print("    ║                           CLI File structure builder                           ║")
    print("    ║                              > interactive mode <                              ║")
    print("    ╚════════════════════════════════════════════════════════════════════════════════╝")
    
    while True:
        choice = input("What would you like to do? (create/scan/exit): ").lower().strip()
        if choice == 'create':
            interactive_create_wizard()
            break
        elif choice == 'scan':
            interactive_scan_wizard()
            break
        elif choice == 'exit':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 'create', 'scan', or 'exit'.")

def interactive_create_wizard():
    print("\n[- Create Structure Wizard -]")
    
    source = ""
    while source not in ['file', 'text']:
        source = input("Enter structure source (file/text): ").lower().strip()

    content = ""
    if source == 'file':
        while True:
            file_path = input("Enter path to the structure file: ")
            if Path(file_path).is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    break
                except Exception as e:
                    print(f"Error reading file: {e}")
            else:
                print(f"File not found: {file_path}")
    else:
        print("Enter the file structure (end with CTRL+D on Unix or CTRL+Z on Windows):")
        content = sys.stdin.read()

    output_dir = input("Enter the output directory (default: current directory): ") or "."

    builder = ArchitectureBuilder(output_dir)
    structure = builder.parse_tree_structure(content)

    if not structure:
        print("Could not parse any valid structure from the input.")
        return

    print("\n[- Structure Preview -]")
    for item in structure:
        indent = "  " * item['level']
        type_str = "🗁" if item['is_directory'] else "🗎"
        print(f"{indent}{type_str} {item['name']}")
    print("------------------------")

    confirm = input(f"Proceed with creating this structure in '{os.path.abspath(output_dir)}'? (y/n): ").lower().strip()
    if confirm == 'y':
        builder.create_structure_interactive(structure)
        print("\n✓ Structure creation process finished!")
    else:
        print("Operation cancelled.")

def interactive_scan_wizard():
    print("\n--- Scan Directory Wizard ---")

    dir_path = None
    while True:
        dir_path_str = input("Enter directory to scan (default: current directory): ") or "."
        path_obj = Path(dir_path_str)
        if path_obj.is_dir():
            dir_path = path_obj
            break
        else:
            print(f"Directory not found: {dir_path_str}")

    formats = ['tree', 'simple', 'json', 'yaml', 'xml', 'markdown']
    format_choice = ""
    while format_choice not in formats:
        format_choice = input(f"Choose output format ({'/'.join(formats)}) [default: tree]: ").lower().strip() or "tree"

    max_depth = None
    while True:
        try:
            depth_str = input("Enter max scan depth (e.g., 3, or press Enter for no limit): ")
            if not depth_str:
                break
            max_depth = int(depth_str)
            break
        except ValueError:
            print("Please enter a valid number.")

    show_size = input("Show file sizes? (y/n): ").lower().strip() == 'y'

    ignore_str = input("Enter comma-separated patterns to ignore (e.g., *.log,temp*): ")
    ignore_patterns = [p.strip() for p in ignore_str.split(',')] if ignore_str else []

    scanner = DirectoryScanner(ignore_patterns)
    print(f"\n⛶ Scanning directory: {dir_path.absolute()}...")
    try:
        structure = scanner.scan_directory(dir_path, max_depth)
        if not structure:
            print("✘ No structure found (empty directory or all files ignored).")
            return

        formatter = StructureFormatter()
        output = ""
        pretty = input("Pretty print JSON/XML output? (y/n): ").lower().strip() == 'y'

        if format_choice == 'tree':
            output = formatter.to_tree_ascii(structure, show_size, dir_path.name)
        elif format_choice == 'simple':
            output = formatter.to_simple_tree(structure, show_size, dir_path.name)
        elif format_choice == 'json':
            output = formatter.to_json(structure, pretty)
        elif format_choice == 'yaml':
            output = formatter.to_yaml(structure)
        elif format_choice == 'xml':
            output = formatter.to_xml(structure)
        elif format_choice == 'markdown':
            output = formatter.to_markdown(structure, show_size, dir_path.name)

        print("\n--- Scan Result Preview (first 20 lines) ---")
        preview_lines = output.split('\n')
        print('\n'.join(preview_lines[:20]))
        if len(preview_lines) > 20:
            print(f"... and {len(preview_lines) - 20} more lines.")
        print("-------------------------------------------")

        save_choice = input("Save to file? (enter file path or press Enter to print to console): ")
        if save_choice:
            try:
                with open(save_choice, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"✓ Structure saved to {save_choice}")
            except Exception as e:
                print(f"✘ Error saving file: {e}")
        else:
            print(f"\n🗁  {dir_path.name}/")
            print(output)
            print("=" * 50)
            print(f"-> Total: {len(structure)} elements")

    except Exception as e:
        print(f"✘ An error occurred during scan: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Architect - File Architecture Builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
User Guide:

1. create a structure from a file:
   python architect.py create -f structure.txt

2. create a structure from stdin:
   echo "project/
   ├── dummy_dir/
   │   └── example.foo
   └── READHIM.md" | python architect.py create

3. scan an existing directory:
   python architect.py scan /path/to/directory

4. scan with different formats:
   python architect.py scan . --format json
   python architect.py scan . --format yaml
   python architect.py scan . --format xml
   python architect.py scan . --format markdown
   python architect.py scan . --format tree
   python architect.py scan . --format simple

5. scan with options:
   # Scan with depth limit
   python architect.py scan . --max-depth 3 --show-size
   
   # Ignore specific patterns
   python architect.py scan . --ignore "*.log" --ignore "temp*"

   # Save output to a file
   python architect.py scan . --output structure.json
   
   # Run in interactive mode
   python architect.py --interactive

Supported formats:
- tree: ASCII tree with linking chars (default)
- simple: simple tree with indentation
- json: Structure in JSON format
- yaml: YAML format (pyYAML required)
- xml: XML format
- markdown: Markdown Format

Examples:
python architect.py scan ./my_project --format json --output structure.json
python architect.py scan . --format tree --show-size --max-depth 2
python architect.py create -f structure.txt --dry-run
python architect.py -i
        """
    )
    
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive wizard mode')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    create_parser = subparsers.add_parser('create', help='Create a file structure')
    create_parser.add_argument('-f', '--file', help='Specify a file with the project structure')
    create_parser.add_argument('-o', '--output', default='.', help='Output dir (default: .)')
    create_parser.add_argument('--dry-run', action='store_true', help='simulate creation without writing files')
    create_parser.add_argument('-v', '--verbose', action='store_true', help='Detailed parsing output')
    
    scan_parser = subparsers.add_parser('scan', help='Scan an existing directory and generate its structure')
    scan_parser.add_argument('directory', nargs='?', default='.', help='Directory to scan (default: .)')
    scan_parser.add_argument('--format', choices=['tree', 'simple', 'json', 'yaml', 'xml', 'markdown', 'terminal'], 
                            default='tree', help='Output format (default: tree)')
    scan_parser.add_argument('--output', '-o', help='Output file (default: terminal display)')
    scan_parser.add_argument('--max-depth', type=int, help='Maximum scan depth')
    scan_parser.add_argument('--show-size', action='store_true', help='Show file sizes')
    scan_parser.add_argument('--ignore', action='append', help='Patterns to ignore (can be repeated)')
    scan_parser.add_argument('--pretty', action='store_true', help='Pretty print JSON/XML output')
    
    args = parser.parse_args()
    
    if args.interactive:
        run_interactive_mode()
        return

    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'create':
        builder = ArchitectureBuilder(args.output)
        
        if args.file:
            structure = builder.parse_from_file(args.file)
        else:
            if sys.stdin.isatty():
                print("Enter the file structure (end with CTRL+D):")
                print("Supported formats: spaces, tabs, ASCII tree characters")
            content = sys.stdin.read()
            structure = builder.parse_tree_structure(content)
        
        if not structure:
            print("No valid structure found. Please check your input format.")
            sys.exit(1)
        
        print("\nDetected structure:")
        for item in structure:
            indent = "  " * item['level']
            type_str = "🗁 " if item['is_directory'] else "🗎"
            if args.verbose:
                print(f"{indent}{type_str} {item['name']} (level: {item['level']}, path: {item['path']})")
            else:
                print(f"{indent}{type_str} {item['name']}")
        
        print(f"\nCreation in: {os.path.abspath(args.output)}")
        
        created = builder.create_structure(structure, dry_run=args.dry_run)
        
        if not args.dry_run:
            print(f"\n✓ {len(created)} elements successfully created!")
        else:
            print(f"\n⌕︎ {len(created)} elements would be created")
    
    elif args.command == 'scan':
        directory = Path(args.directory)
        
        if not directory.exists():
            print(f"✘ Directory {directory} does not exist")
            sys.exit(1)
        
        ignore_patterns = args.ignore or []
        scanner = DirectoryScanner(ignore_patterns)
        
        print(f"⛶ Scanning directory: {directory.absolute()}")
        
        try:
            structure = scanner.scan_directory(directory, args.max_depth)
            
            if not structure:
                print("✘ No structure found (empty directory or all files ignored)")
                return
            
            formatter = StructureFormatter()
            
            if args.format == 'tree':
                output = formatter.to_tree_ascii(structure, args.show_size, directory.name)
            elif args.format == 'simple':
                output = formatter.to_simple_tree(structure, args.show_size, directory.name)
            elif args.format == 'json':
                output = formatter.to_json(structure, args.pretty)
            elif args.format == 'yaml':
                output = formatter.to_yaml(structure)
            elif args.format == 'xml':
                output = formatter.to_xml(structure)
            elif args.format == 'markdown':
                output = formatter.to_markdown(structure, args.show_size, directory.name)
            elif args.format == 'terminal':
                output = formatter.to_tree_ascii(structure, args.show_size, directory.name)
            
            if args.output:
                try:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(output)
                    print(f"✓ Structure saved to {args.output}")
                except Exception as e:
                    print(f"✘ Error during saving: {e}")
            else:
                print(f"\n🗁  {directory.name}/")
                print(output)
                print("=" * 50)
                print(f"-> Total: {len(structure)} elements")
        
        except Exception as e:
            print(f"✘ Error during scan: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()