import os

from .tool_adapter import exception_handler
from feature_extractor.property_specs.pdf_property_spec  import FilePropertySpec


class FileMetaAdapter:

    @exception_handler
    def collect_properties(self, file_path, prop_spec: FilePropertySpec = None):
        """Processing file meta to retrieve file size"""
        prop_spec.file_size = os.path.getsize(os.path.abspath(file_path))
