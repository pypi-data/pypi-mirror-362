from ._abstract import AbstractFolderPicker


class WindowsFolderPicker(AbstractFolderPicker):
    def pick_folder(self, title="Select a folder", icon: str | None = None) -> str:
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
        if icon:
            try:
                root.iconbitmap(icon)
            except tk.TclError:
                print(f"Warning: Unable to set icon from {icon}. Using default icon.")

        root.withdraw()
        root.attributes("-topmost", True)  # Keep dialog on top

        folder_path = filedialog.askdirectory(title=title)

        root.destroy()
        return folder_path
