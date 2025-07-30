import subprocess
import shutil
from ._abstract import AbstractFolderPicker


class LinuxFolderPicker(AbstractFolderPicker):
    def pick_folder(
        self, title="Select a folder", icon: str | None = None
    ) -> str | None:
        """
        Opens a folder picker dialog on Linux using zenity/kdialog/yad or falls back to manual input.

        Args:
            title (str): Title of the folder picker dialog.
            icon (str | None): Path to icon file to use for the dialog window.

        Returns:
            str | None: The path of the selected folder or None if cancelled.
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
            cmd = [
                "zenity",
                "--file-selection",
                "--directory",
                f"--title={title}",
            ]
            if icon:
                cmd.append(f"--window-icon={icon}")
            folder = run_cmd(cmd)
            if folder:
                return folder

        elif shutil.which("kdialog"):
            cmd = ["kdialog", "--getexistingdirectory", "~"]
            if icon:
                cmd.append(f"--icon={icon}")
            folder = run_cmd(cmd)
            if folder:
                return folder

        elif shutil.which("yad"):
            cmd = [
                "yad",
                "--file-selection",
                "--directory",
                f"--title={title}",
            ]
            if icon:
                cmd.append(f"--window-icon={icon}")
            folder = run_cmd(cmd)
            if folder:
                return folder
        else:
            raise RuntimeError(
                "You need to install zenity, kdialog, or yad to use this package."
            )

        return None
