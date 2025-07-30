from abc import ABC, abstractmethod


class AbstractFolderPicker(ABC):
    """Abstract base class for cross-platform folder picker implementations."""

    @abstractmethod
    def pick_folder(
        self, title="Select a folder", icon: str | None = None
    ) -> str | None:
        """
        Opens a folder picker dialog with optional title and icon, and returns the selected folder path.

        Args:
            title (str, optional): The title or prompt to display in the folder picker dialog. Defaults to "Select a folder".
            icon (str | None, optional): Path to an icon file to display in the dialog window (if supported). Defaults to None.

        Returns:
            str | None: The absolute path of the selected folder, or None if no folder was selected or the dialog was cancelled.
        """
        pass
