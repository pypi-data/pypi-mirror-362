""" File Validation Methods.
 - These Methods all raise SystemExit exceptions.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from sys import exit

from treescript_builder.input.string_validation import validate_name


def validate_input_file(file_name: str) -> str | None:
    """ Read the Input File, Validate (non-blank) data, and return Input str.

**Parameters:**
 - file_name (str): The Name of the Input File.

**Returns:**
 str - The String Contents of the Input File.

**Raises:**
 SystemExit - If the File does not exist, or is empty or blank, or read failed.
    """
    file_path = Path(file_name)
    if not file_path.exists():
        exit("The Input File does not Exist.")
    try:
        if (data := file_path.read_text()) is not None and validate_name(data):
            return data
    except OSError:
        exit("Failed to Read from File.")
    return None


def validate_directory(dir_path_str: str | None) -> Path | None:
    """ Ensure that if the Directory is present, it Exists.

**Parameters:**
- dir_path_str (str, optional): The String representation of the Path to the Directory.

**Returns:**
 Path? - The , or None if given input is None.

**Raises:**
 SystemExit - If a given path does not exist.
    """
    if dir_path_str is None:
        return None
    if not validate_name(dir_path_str):
        exit("Data Directory is invalid")
    if (path := Path(dir_path_str)).exists():
        return path
    exit("The given Directory does not exist!")