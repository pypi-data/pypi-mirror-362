import subprocess
from ._abstract import AbstractFolderPicker


class MacOSFolderPicker(AbstractFolderPicker):
    def pick_folder(self) -> str | None:
        """
        Opens a native macOS folder picker dialog and returns the selected folder path.

        Returns:
            str: The path of the selected folder.
        """
        try:
            script = 'POSIX path of (choose folder with prompt "Select a folder")'
            result = subprocess.run(
                ["osascript", "-e", script], capture_output=True, text=True, check=True
            )
            folder_path = result.stdout.strip()
            return folder_path if folder_path else None
        except subprocess.CalledProcessError:
            return None
