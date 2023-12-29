from concurrent.futures import ThreadPoolExecutor

from feature_extractor.adapters.yara_adapter import YaraAdapter
from feature_extractor.adapters.file_meta_adapter import FileMetaAdapter


class FilePropertyCollector:
    def __init__(self, file_path, property_spec=None):
        self.file_path = file_path
        self.property_spec = property_spec
        self.adapters = [
            FileMetaAdapter(),
            YaraAdapter()
        ]

    def collect_properties(self):
        with ThreadPoolExecutor(max_workers=8) as executor:
            [
                executor.submit(adapter.collect_properties, self.file_path, self.property_spec)
                for adapter in self.adapters
            ]
        return self.property_spec
