""" Line Reader.

The Default Input Reader.
 - Processes a single line at a time, and determines its key properties.
 - The Depth is the Integer number of directories between the current line and the root.
 - The Directory Boolean indicates whether the line represents a Directory.
 - The Name String is the name of the line.
 Author: DK96-OS 2024 - 2025
"""
from itertools import groupby
from sys import exit
from typing import Generator

from treescript_builder.data.tree_data import TreeData
from treescript_builder.input.string_validation import validate_dir_name, validate_name

SPACE_CHARS = (' ', ' ', ' ', ' ')


def read_input_tree(input_tree_data: str) -> Generator[TreeData, None, None]:
    """ Generate structured Tree Data from the Input Data String.

**Parameters:**
 - input_data (InputData): The Input.

**Yields:**
 TreeData - Produces TreeData from the Input Data.

**Raises:**
 SystemExit - When any Line cannot be read successfully.
    """
    line_number = 1
    for is_newline, group in groupby(input_tree_data, lambda x: x in ["\n", "\r"]):
        if is_newline:
            line_number += sum(1 for _ in group) # Line number increase by size of group
        else:
            line = ''.join(group)
            if len(lstr := line.lstrip()) == 0 or lstr.startswith('#'):
                continue
            yield _process_line(line_number, line)


def _process_line(
    line_number: int,
    line: str,
) -> TreeData:
    """ Processes a single line of the input tree structure.
 - Returns a tuple indicating the depth, type (file or directory), name of file or dir, and file data if available.

**Parameters:**
 - line_number (int): The line-number in the input tree structure, starting from 1.
 - line (str): A line from the input tree structure.

**Returns:**
 tuple: (int, bool, str, str) where int is the depth, bool is true when is Directory, and str is name, followed by str data.

**Raises:**
 SystemExit - When Line cannot be read successfully.
    """
    # Calculate the Depth
    depth = _calculate_depth(line)
    if depth < 0:
        exit(f"Invalid Space Count in Line: {line_number}")
    # Remove Space
    args = line.strip()
    # Try to split line into multiple arguments
    for space_char in SPACE_CHARS:
        if space_char in args:
            args = args.split(space_char)
            break
    # Check whether line was split or not
    if isinstance(args, str):
        name = args
        data_label = ""
    elif isinstance(args, list) and len(args) >= 2:
        name = args[0]
        data_label = args[1]
    else:
        exit(f"Invalid Line: {line_number}")
    # Validate the Node Name and Type.
    node_info = _validate_node_name(name)
    if node_info is None:
        exit(f'Invalid Node on Line: {line_number}')
    (is_dir, name) = node_info
    return TreeData(
        line_number,
        depth,
        is_dir,
        name,
        data_label
    )


def _validate_node_name(node_name: str) -> tuple[bool, str] | None:
    """ Determine whether this Tree Node is a Directory, and validate the name.

**Parameters:**
 - node_name (str): The argument received for the node name.

**Returns:**
 tuple[bool, str] - Node information, first whether it is a directory, then the valid name of the node.
    
**Raises:**
 SystemExit - When the directory name is invalid.
    """
    try:
        # Check if the line contains any slash characters
        if (dir_name := validate_dir_name(node_name)) is not None:
            return (True, dir_name)
        # Fall-Through to File Node
    except ValueError:
        # An error in the dir name, such that it cannot be a file either
        return None
    # Is a File
    if validate_name(node_name):
        return (False, node_name)
    return None


def _calculate_depth(line: str) -> int:
    """ Calculates the depth of a line in the tree structure.

**Parameters:**
 - line (str): A line from the tree command output.

**Returns:**
 int: The depth of the line in the tree structure, or -1 if space count is invalid.
    """
    from itertools import takewhile
    space_count = len(list(
        takewhile(lambda c: c in SPACE_CHARS, line)
    ))
    # Bit Shift Shuffle Equivalence Validation (space_count is divisible by 2)
    if (depth := space_count >> 1) << 1 == space_count:
        return depth
    return -1  # Invalid Space Count! Someone made an off-by-one whitespace mistake!