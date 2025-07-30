from ._abstract import AbstractFolderPicker


class WindowsFolderPicker(AbstractFolderPicker):
    def pick_folder(self) -> str:
        """
        Opens a folder picker dialog and returns the selected folder path.

        Returns:
            str: The path of the selected folder.
        """

        try:
            import tkinter as tk
            from tkinter import filedialog
        except ImportError:
            raise ImportError("`tkinter` is required for Windows folder picking.")

        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Select Folder")
        return folder_path
