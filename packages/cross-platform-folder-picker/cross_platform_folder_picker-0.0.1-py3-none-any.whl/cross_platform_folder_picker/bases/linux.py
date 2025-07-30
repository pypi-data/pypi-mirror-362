import subprocess
import shutil
from ._abstract import AbstractFolderPicker


class LinuxFolderPicker(AbstractFolderPicker):
    def pick_folder(self) -> str | None:
        """
        Opens a folder picker dialog on Linux using zenity/kdialog/yad or falls back to manual input.

        Returns:
            str: The path of the selected folder.
        """

        def run_cmd(cmd):
            try:
                result = subprocess.run(
                    cmd, capture_output=True, text=True, check=True, timeout=30
                )
                path = result.stdout.strip()
                return path if path else None
            except (subprocess.CalledProcessError, FileNotFoundError):
                return None

        if shutil.which("zenity"):
            folder = run_cmd(
                ["zenity", "--file-selection", "--directory", "--title=Select a folder"]
            )
            if folder:
                return folder

        elif shutil.which("kdialog"):
            folder = run_cmd(["kdialog", "--getexistingdirectory", "~"])
            if folder:
                return folder

        elif shutil.which("yad"):
            folder = run_cmd(
                ["yad", "--file-selection", "--directory", "--title=Select a folder"]
            )
            if folder:
                return folder
        else:
            raise RuntimeError(
                "You need to install zenity, kdialog, or yad to use this package."
            )

        return folder if folder else None
