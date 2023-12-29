import re

from bs4 import BeautifulSoup
from collections import defaultdict

from .tool_adapter import exception_handler
from feature_extractor.property_specs.pdf_property_spec  import PdfPropertySpec


class ScriptsAdaptor:
    """Match urls/js/iframe tags"""
    regex_types = {
        'iframe': rb'<iframe[^>]*>[^<]*</iframe>',
        'urls': rb'https|http://[a-zA-Z0-9/?@:%.\-_\+~#=]+|www\.[a-zA-Z0-9/?@:%.\-_\+~#=]+'
    }

    script_pattern = rb"<\s*script[^>]*>[^<]*</\s*script\s*\n?>"

    @exception_handler
    def collect_properties(self, file_path, prop_spec: FilePropertySpec):
        data = open(file_path, 'rb').read()
        prop_spec.scripts.script_types = dict(self.get_script_matches(data))

        for key, regex in self.regex_types.items():
            matches = [i.decode('utf-8') for i in re.findall(regex, data, re.I | re.S)]
            setattr(prop_spec.scripts, key, matches)

    def get_script_matches(self, source):
        script_types = defaultdict(list)
        # remove comments
        source = re.sub(rb"/\*\n?.*\n?\*/", b"", source, re.DOTALL, flags=re.S)
        for script in re.findall(self.script_pattern, source, re.I | re.S):
            try:
                x = BeautifulSoup(script, "html.parser")
                language = x.script.attrs.get("language", "").lower() or x.script.attrs.get("type", "").lower()
            except:
                language = None
            if not language:
                matches = re.search(rb'language\s*=\s*[\'|\"](\w+([\-_.]*\w+)*)[\'|\"]\s*', script, re.S)
                if matches:
                    language = language.group(2).decode().lower()
                else:
                    language = 'default_scripts'
            script_types[language].append(script.decode())
        return script_types
