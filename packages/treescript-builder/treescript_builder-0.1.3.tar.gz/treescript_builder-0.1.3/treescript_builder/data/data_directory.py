"""Data Directory Management.
 Author: DK96-OS 2024 - 2025
"""
from pathlib import Path
from sys import exit

from treescript_builder.data.tree_data import TreeData
from treescript_builder.input.string_validation import validate_data_label


class DataDirectory:
    """ Manages Access to the Data Directory.
 - Search for a Data Label, and obtain the Path to the Data File.

**Method Summary:**
 - validate_build(TreeData): Path?
 - validate_trim(TreeData): Path?
    """

    def __init__(self, data_dir: Path):
        if not isinstance(data_dir, Path) or not data_dir.exists():
            exit('The Data Directory must be a Path that Exists!')
        self._data_dir = data_dir
        # todo: Create a map of used Data Labels

    def validate_build(self, node: TreeData) -> Path | None:
        """ Determine if the Data File supporting this Tree node is available.

        Parameters:
        - node (TreeData): The TreeData to validate.

        Returns:
        Path - The Path to the Data File in the Data Directory.

        Raises:
        SystemExit - When the Data label is invalid, or the Data File does not exist.
        """
        if node.data_label == '' or node.is_dir:
            return None
        if node.data_label == '!':
            data_path = self._search_label(node.name)
        else:
            data_path = self._search_label(node.data_label)
        if data_path is None:
            exit(f'Data Label ({node.data_label}) not found in Data Directory on line: {node.line_number}')
        return data_path

    def validate_trim(self, node: TreeData) -> Path | None:
        """ Determine if the File already exists in the Data Directory.

        Parameters:
        - node (TreeData): The TreeData to validate.

        Returns:
        Path - The Path to a new File in the Data Directory.

        Raises:
        SystemExit - When the Data label is invalid, or the Data File already exists.
        """
        # Ensure that the name of the Label is valid
        if node.data_label == '' or node.is_dir:
            return None
        data_label = node.name if node.data_label == '!' else node.data_label
        if not validate_data_label(data_label):
            exit(f'Invalid Data Label on line: {node.line_number}')
        # Check if the Data File already exists
        data_path = self._search_label(data_label)
        if data_path is not None:
            exit(f'Data File already exists!\n({data_label}) on line: {node.line_number}')
        # Create the Data Label Path in the Directory
        return self._data_dir / data_label

    def _search_label(self, data_label: str) -> Path | None:
        """ Search for a Data Label in this Data Directory.

        Parameters:
        - data_label (str): The Data Label to search for.

        Returns:
        Path (optional) - The Path to the Data File, or None.
        """
        if not validate_data_label(data_label):
            return None
        # Find the Data Label File
        data_files = self._data_dir.glob(data_label)
        try:
            return next(data_files)
        except StopIteration:
            return None