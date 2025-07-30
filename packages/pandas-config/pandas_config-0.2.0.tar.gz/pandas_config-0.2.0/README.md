# pandas-config

A simple utility to load pandas configurations from INI files.

## Description

This package provides an elegant solution for managing pandas options through INI configuration files. 
It allows you to easily define and load different pandas configurations without modifying the source code (at least 
for the options accepting literal values).

## Installation

To install the required dependencies:

```bash
uv add pandas-config
```

## Usage

The main module `configfile.py` contains a `load()` function that loads pandas configurations from an INI file.

### Basic Example

1. Create a `.pandas.ini` configuration file:

```ini
[display]
width = 200
max_colwidth = 25
max_columns = 20
min_rows = 20
precision = 3

[display.html]
border = 4
```

2. Load the configuration in your code:

```python
from pandas.configfile import load

# Load configuration from default .pandas.ini file
load()

# Or specify a custom path
load("path/to/config.ini")
```

### Parameters

- `path` (optional): Path to the configuration file. Default: `.pandas.ini`
- `encoding` (optional): File encoding. Default: `utf-8`

## Configuration File Structure

The configuration file must follow the standard INI format:
- Sections define pandas option groups (e.g., `[display]`)
- Values must be valid Python literals
- Subsections use dot as separator (e.g., `[display.html]`)

## Dependencies

- pandas
- Python 3.x

## Notes

- Values in the configuration file must be valid Python literals (evaluated using `ast.literal_eval()`)
- The default configuration file is `.pandas.ini` in the current directory
- If no file is found at the specified location, no error will be raised

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
