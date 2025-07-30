import sys


def open_folder_picker():
    """
    Opens a folder picker dialog and returns the selected folder path.

    Returns:
        str: The path of the selected folder.
    """
    match sys.platform:
        case "win32":
            from .bases import WindowsFolderPicker

            picker = WindowsFolderPicker()
        case "darwin":
            from .bases import MacOSFolderPicker

            picker = MacOSFolderPicker()
        case "linux":
            from .bases import LinuxFolderPicker

            picker = LinuxFolderPicker()
        case _:
            raise NotImplementedError(f"Unsupported platform: {sys.platform}")

    return picker.pick_folder()
