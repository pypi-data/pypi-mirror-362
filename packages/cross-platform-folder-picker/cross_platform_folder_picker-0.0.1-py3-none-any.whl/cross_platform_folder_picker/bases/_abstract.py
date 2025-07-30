from abc import ABC, abstractmethod


class AbstractFolderPicker(ABC):
    """Abstract base class for cross-device folder picker implementations."""

    @abstractmethod
    def pick_folder(self) -> str | None:
        """
        Opens a folder picker dialog and returns the selected folder path.

        Returns:
            str: The path of the selected folder.
        """
        pass
