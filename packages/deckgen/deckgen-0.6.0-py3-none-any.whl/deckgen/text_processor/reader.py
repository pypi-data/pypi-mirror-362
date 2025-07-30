from typing import Union
from pathlib import Path


ALLOWED_FILE_TYPES = [
    ".txt"
]  # Extend this list as needed. For now, only text files are allowed.


class Reader:
    """
    A class to read content from a file.

    It provides methods to read the entire content or read it line by line.
    """

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = file_path if isinstance(file_path, Path) else Path(file_path)

    def read(self):

        valid_extension = self._is_valid_extension()
        if not valid_extension:
            raise ValueError(
                f"Invalid file type. Allowed types are: {', '.join(ALLOWED_FILE_TYPES)}"
            )

        if not self.file_path.exists():
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")

        with open(self.file_path, "r") as file:
            # Read the entire content of the file
            # This assumes the file is a text file.
            # In this case, we are assuming the file is relatively small and can be read into memory.
            # For larger files, consider reading in chunks or using a generator.
            content = file.read()

        return content

    def _is_valid_extension(self):
        """
        Checks if the file extension is valid.
        :return: True if the file extension is valid, False otherwise.
        """
        return self.file_path.suffix in ALLOWED_FILE_TYPES
