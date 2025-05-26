# Python String Extractor

A Python tool that scans Python source code and extracts string literals using AST analysis.

## Features

- Recursively scans directories for Python files
- Uses AST (Abstract Syntax Tree) to reliably extract string literals
- Supports different types of string literals (single quotes, double quotes, triple quotes, f-strings)
- Outputs results in JSON format
- Minimal dependencies - uses only the Python standard library

## Installation

```bash
# Install using Poetry
poetry install
```

## Usage

```bash
# Run the extractor on a directory
python -m python_string_extractor.extractor /path/to/python/code
```

The output is a JSON object where:
- Keys are relative file paths
- Values are arrays of string literals found in each file

## Example Output

```json
{
  "main.py": [
    "Hello, world!",
    "This is a test"
  ],
  "lib/utils.py": [
    "Utility functions",
    "Helper string"
  ]
}
```
