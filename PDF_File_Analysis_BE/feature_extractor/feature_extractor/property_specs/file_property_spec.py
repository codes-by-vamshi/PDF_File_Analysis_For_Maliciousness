from typing import List, Dict


class Scripts:
    script_types: Dict
    iframe: List = []
    urls: List = []


class FilePropertySpec:
    # This is the size in bytes of the file
    file_size: int
    yara_signatures: List
    scripts: Scripts

    def __init__(self):
        self.file_size = 0
        self.yara_signatures = []
        self.scripts = Scripts()
