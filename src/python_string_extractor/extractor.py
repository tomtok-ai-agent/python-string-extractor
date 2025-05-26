"""
AST-based string literal extractor for Python code.

This module provides functionality to scan Python source code files,
extract string literals using AST analysis, and output the results in JSON format.
"""

import ast
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class StringVisitor(ast.NodeVisitor):
    """AST visitor that collects string literals from Python code."""
    
    def __init__(self):
        self.string_literals: List[str] = []
        
    def visit_Str(self, node: ast.Str) -> None:
        """Visit string literals in Python 3.7 and earlier."""
        self.string_literals.append(node.s)
        self.generic_visit(node)
        
    def visit_Constant(self, node: ast.Constant) -> None:
        """Visit constant nodes (including strings) in Python 3.8+."""
        if isinstance(node.value, str):
            self.string_literals.append(node.value)
        self.generic_visit(node)
        
    def visit_JoinedStr(self, node: ast.JoinedStr) -> None:
        """Visit f-strings."""
        # Extract only the constant string parts of f-strings
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                self.string_literals.append(value.value)
        self.generic_visit(node)


def extract_strings_from_file(file_path: Path) -> Optional[List[str]]:
    """
    Extract string literals from a Python file using AST analysis.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        List of string literals or None if parsing failed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
            
        tree = ast.parse(source_code)
        visitor = StringVisitor()
        visitor.visit(tree)
        return visitor.string_literals
    except (SyntaxError, UnicodeDecodeError, PermissionError, FileNotFoundError) as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None


def scan_directory(directory: Path) -> Dict[str, List[str]]:
    """
    Recursively scan a directory for Python files and extract string literals.
    
    Args:
        directory: Path to the directory to scan
        
    Returns:
        Dictionary mapping file paths to lists of string literals
    """
    result: Dict[str, List[str]] = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                strings = extract_strings_from_file(file_path)
                if strings:
                    # Use relative path from the scanned directory
                    rel_path = file_path.relative_to(directory)
                    result[str(rel_path)] = strings
    
    return result


def main() -> None:
    """
    Main entry point for the string extractor.
    
    Usage: python -m python_string_extractor.extractor <directory>
    """
    if len(sys.argv) != 2:
        print("Usage: python -m python_string_extractor.extractor <directory>", file=sys.stderr)
        sys.exit(1)
        
    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print(f"Error: {directory} is not a directory", file=sys.stderr)
        sys.exit(1)
        
    result = scan_directory(directory)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
