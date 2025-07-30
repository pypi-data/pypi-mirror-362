# Cross-Platform-Folder-Picker

> A (near zero dependency) cross platform folder picker


![Example GIF](https://raw.githubusercontent.com/baseplate-admin/Cross-Platform-Folder-Picker/refs/heads/master/assets/example.gif)


# Features

* Opens a folder dialog using:

    - `tkinter` for windows
    - `zenity`/`kdialog` for linux
    - `osascript` for macOS

* Customize the window and icon of the dialog

# Installation

```shell
pip install cross_platform_folder_picker
```

# Usage

```python
from cross_platform_folder_picker import open_folder_picker

res = open_folder_picker()
```

# Roadmap

- Investigate a better way to handle folder open dialog
- Reduce dependency on tkinter on windows
