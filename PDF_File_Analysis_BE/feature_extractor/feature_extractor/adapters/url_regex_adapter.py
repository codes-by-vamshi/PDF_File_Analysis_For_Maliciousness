import re

from .tool_adapter import exception_handler
from feature_extractor.property_specs.pdf_property_spec  import PdfPropertySpec


class URLRegexAdapter:

    @exception_handler
    def collect_properties(self, file_path, prop_spec: PdfPropertySpec = None):

        url_pattern = rb'https|http://[a-zA-Z0-9/?@:%.\-_\+~#=]*|www\.[a-zA-Z0-9/?@:%.\-_\+~#=]*'

        data = open(file_path, 'rb').read()
        prop_spec.regex_urls = [i.decode('utf-8', 'backslashreplace') for i in re.findall(url_pattern, data)]
        prop_spec.regex_uris = [i.decode('utf-8', 'backslashreplace') for i in re.findall(rb"/URI \((.*)\)", data)]
