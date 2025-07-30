""" Defines the configuration values of the module.
    Values in the ProStore are saved and loaded during application startup/shutdown automatically
Copyright Nanosurf AG 2021
License - MIT
"""

from datetime import datetime
import pathlib
import os

import nanosurf as nsf

class ProjectSettings():
    def __init__(self, project_name: str) -> None:
        self.project_name = project_name
        self.author = ""
        self.date = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        self.file_path = pathlib.Path("")

class StartSettings(nsf.PropStore):
    def __init__(self) -> None:
        super().__init__()
        self.save_path = nsf.PropVal(pathlib.Path(os.getenv(r"UserProfile")) / "Desktop")
        # self.last_used_author = nsf.PropVal("Unknown")
        # self.last_used_project = nsf.PropVal("Noname")

