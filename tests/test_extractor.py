"""Tests for the string extractor module."""

import json
import os
import tempfile
from pathlib import Path
import unittest

from python_string_extractor.extractor import extract_strings_from_file, scan_directory


class TestStringExtractor(unittest.TestCase):
    """Test cases for the string extractor functionality."""

    def test_extract_strings_from_file(self):
        """Test extracting strings from a Python file."""
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
            f.write('''
# Test file with various string literals
simple_string = "Hello, world!"
another_string = 'Single quotes'
multiline_string = """This is a
multiline string"""
f_string = f"Formatted {variable} string"
mixed_string = f"Mixed {f'nested'} string"
empty_string = ""
''')
            temp_file = Path(f.name)

        try:
            strings = extract_strings_from_file(temp_file)
            self.assertIsNotNone(strings)
            self.assertEqual(len(strings), 14)  # AST parser extracts 14 string literals from the file
            self.assertIn("Hello, world!", strings)
            self.assertIn("Single quotes", strings)
            self.assertIn("This is a\nmultiline string", strings)
            self.assertIn("Formatted ", strings)
            self.assertIn(" string", strings)
            self.assertIn("nested", strings)
            self.assertIn("", strings)
        finally:
            os.unlink(temp_file)

    def test_scan_directory(self):
        """Test scanning a directory for Python files and extracting strings."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test directory structure
            dir_path = Path(temp_dir)
            
            # Create a Python file in the root
            with open(dir_path / "main.py", "w") as f:
                f.write('print("Root file string")\n')
            
            # Create a subdirectory with a Python file
            subdir = dir_path / "subdir"
            subdir.mkdir()
            with open(subdir / "module.py", "w") as f:
                f.write('message = "Subdir string"\n')
            
            # Create a non-Python file that should be ignored
            with open(dir_path / "ignored.txt", "w") as f:
                f.write('This is not a Python file')

            # Scan the directory
            result = scan_directory(dir_path)
            
            # Check the results
            self.assertEqual(len(result), 2)  # Two Python files
            self.assertIn("main.py", result)
            self.assertIn("subdir/module.py", result)
            self.assertIn("Root file string", result["main.py"])
            self.assertIn("Subdir string", result["subdir/module.py"])


if __name__ == "__main__":
    unittest.main()
