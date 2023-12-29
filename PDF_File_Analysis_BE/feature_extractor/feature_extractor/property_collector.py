from feature_extractor.adapters import *
from feature_extractor.file_property_collector import FilePropertyCollector
from feature_extractor.property_specs.pdf_property_spec import PdfPropertySpec


class PdfPropertyCollector(FilePropertyCollector):
    def __init__(self, file_path):
        super().__init__(file_path, PdfPropertySpec())
        self.adapters.extend([
            ExifAdapter(),
            PdfIdAdapter(),
            #PeePdfAdapter(),
            URLRegexAdapter(),
            Pypdf2Adapter()
        ])
