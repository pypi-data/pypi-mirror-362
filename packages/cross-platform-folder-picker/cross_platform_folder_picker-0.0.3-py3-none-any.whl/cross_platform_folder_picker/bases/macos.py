import subprocess
from ._abstract import AbstractFolderPicker


class MacOSFolderPicker(AbstractFolderPicker):
    def pick_folder(
        self, title="Select a folder", icon: str | None = None
    ) -> str | None:
        """
        Opens a native macOS folder picker dialog and returns the selected folder path.

        Args:
            title (str): The prompt text in the folder picker dialog.
            icon (str | None): Ignored on macOS (not supported).

        Returns:
            str | None: The path of the selected folder or None.
        """
        try:
            # Escape double quotes in title if needed
            safe_title = title.replace('"', '\\"')
            script = f'POSIX path of (choose folder with prompt "{safe_title}")'
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                check=True,
            )
            folder_path = result.stdout.strip()
            return folder_path if folder_path else None
        except subprocess.CalledProcessError:
            return None
