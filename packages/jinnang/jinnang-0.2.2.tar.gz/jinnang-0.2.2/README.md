# Jinnang Utils

A comprehensive collection of Python utility functions and classes for common programming tasks.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)

## Overview

Jinnang Utils is a comprehensive Python utility library designed to simplify common programming tasks. It provides a structured collection of reusable functions and classes, organized for clarity, efficiency, and ease of use.

## Module Structure

The `jinnang` package is organized into logical sub-packages to enhance discoverability and maintainability:

```
src/
└── jinnang/
    ├── __init__.py
    ├── ai/                   # AI-related functionalities (e.g., LLM utilities)
    │   ├── __init__.py
    │   └── llm_utils.py
    ├── arithmetic/           # Arithmetic and numerical utilities
    │   ├── __init__.py
    │   └── arithmetic.py
    ├── common/               # Generic, cross-cutting utilities (decorators, patterns, collections, exceptions, hashing)
    │   ├── __init__.py
    │   ├── collections.py
    │   ├── decorators.py
    │   ├── exceptions.py     # Custom exception classes
    │   ├── hash.py
    │   └── patterns.py
    ├── geo/                  # Geographical data utilities
    │   └── __init__.py
    ├── date/                 # Date and time utilities
    │   ├── __init__.py
    │   └── date.py
    ├── debug/                # Debugging utilities
    │   ├── __init__.py
    │   └── debug.py
    ├── io/                   # Input/Output operations (file, system interactions)
    │   ├── __init__.py
    │   ├── file.py
    │   └── system.py         # System-related functions
    ├── media/                # Media-related utilities
    │   └── resolution.py    # Video resolution presets
    ├── path/                 # Path resolution utilities
    │   ├── __init__.py
    │   └── path.py
    ├── string/               # String manipulation and formatting utilities
    │   ├── __init__.py
    │   └── string.py
    └── verbosity/            # Verbosity level management
        ├── __init__.py
        └── verbosity.py
```

## Features

-   **AI Tools**: Utilities for Large Language Models and other AI-related tasks.
-   **Arithmetic Utilities**: Essential arithmetic and numerical functions.
-   **Common Helpers**: Reusable components like decorators, design patterns, collections, and hashing.
-   **Geographical Utilities**: Tools for geographical data calculations.
-   **Date Utilities**: Tools for handling date and time operations.
-   **Debugging**: Helpers for inspecting Python execution and class information.
-   **I/O Operations**: Tools for file system interactions and system-level utilities.
-   **Media Utilities**: Tools for media-related functionalities.
-   **Path Utilities**: Functions for resolving file paths.
-   **String Utilities**: Functions specifically designed for string analysis and transformation.
-   **Verbosity Management**: Utilities for controlling output verbosity.

## Installation

```bash
pip install jinnang-utils
```

## Usage

### Data Handling

```python
from jinnang.common import hash

# Create a stable hash for any object
hash_value = hash.stable_hash({"key": "value"})
print(hash_value)  # Outputs a consistent MD5 hash

# Calculate MD5 hash
md5_hash = hash.md5("string to hash")

# Generate partial file hash
file_hash = hash.partial_file_hash("path/to/file")
```

### I/O Operations

```python
from jinnang.io import file, system

# Check if a folder name is valid
if file.is_bad_folder_name("folder/with/invalid:chars"):
    print("Invalid folder name")

# Check if a caption has too many question marks
if file.is_bad_llm_caption("Is this a question? Or this? Or maybe this? Or this one too?"):
    print("Too many questions in caption")

# Suppress stdout and stderr
with system.suppress_stdout_stderr():
    print("This will not be displayed")
    
# Suppress only C-level stdout
with system.suppress_c_stdout_stderr(suppress_stdout=True, suppress_stderr=False):
    # Code that generates C-level output
    pass
```

### Arithmetic Utilities

```python
from jinnang.arithmetic import arithmetic

# Find the mode of a list
mode = arithmetic.get_mode([1, 2, 2, 3, 3, 3, 4])
print(mode)  # Outputs: 3
```

### String Utilities

```python
from jinnang.string import string

# Safe string formatting
result = string.safe_format("Hello {name}", {"name": "World", "age": 30})
print(result)

# Calculate tokens for image dimensions
tokens = string.calculate_tokens(width=512, height=512)
print(tokens)
```

### Date Utilities

```python
from jinnang.date import date

# Get the current UTC datetime
now_utc = date.get_now_utc()
print(f"Current UTC time: {now_utc}")

# Convert UTC to local time
local_time = date.utc_to_local(now_utc)
print(f"Local time: {local_time}")

# Format datetime to string
formatted_date = date.format_datetime(now_utc, "%Y-%m-%d %H:%M:%S")
print(f"Formatted date: {formatted_date}")
```

### Verbosity Management

```python
from jinnang.verbosity import verbosity
from jinnang.verbosity.verbosity import Verbosity

# Set the global verbosity level
verbosity.set_verbosity(Verbosity.INFO)

# Check the current verbosity level
current_level = verbosity.get_verbosity()
print(f"Current verbosity level: {current_level}")

# Conditionally execute code based on verbosity
if verbosity.is_verbose(Verbosity.DEBUG):
    print("This message only appears in DEBUG mode or higher.")
```

### Debugging

```python
from jinnang import debug

# Get Python execution information
exec_info = debug.get_python_execution_info()
print(exec_info["version"])

# Get class information
class_info = debug.get_class_info(MyClass)
print(class_info)

# Print execution information
debug.print_execution_info()

# Print class information
debug.print_class_info(MyClass)
```

### Common Helpers

```python
from jinnang.common import mock_when, fail_recover, custom_retry
from jinnang.common.exceptions import BadInputException

# Use decorators
@mock_when(condition=lambda: is_test_environment)
def function_to_mock():
    # Real implementation
    pass

@fail_recover(default_value=None)
def function_that_might_fail():
    # Implementation that might raise exceptions
    pass

@custom_retry(max_attempts=3, delay=1)
def function_to_retry():
    # Implementation that might need retrying
    pass

# Use exceptions
raise BadInputException("Invalid input provided")
```

### Path Utilities

```python
from jinnang.path.path import RelPathSeeker
import os

# Resolve a file path relative to the caller module
# Assuming 'my_config.json' is in the same directory as the script calling this
resolved_path = RelPathSeeker.resolve_file_path(
    filename="my_config.json",
    caller_module_path=__file__
)
print(f"Resolved path: {resolved_path}")

# Example with a non-existent file (will raise FileNotFoundError)
try:
    RelPathSeeker.resolve_file_path(
        filename="non_existent_file.txt",
        caller_module_path=__file__
    )
except FileNotFoundError as e:
    print(f"Error: {e}")
```

### AI Tools

```python
from jinnang.ai import llm_utils

# Example usage of LLM utilities
# result = llm_utils.process_text_with_llm("Your text here")
# print(result)
```

## Testing

To run the tests, navigate to the root directory of the project and execute:

```bash
pytest -v
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.