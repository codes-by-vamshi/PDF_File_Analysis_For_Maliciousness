import os
import yara
import timeout_decorator

from .tool_adapter import exception_handler
from feature_extractor.property_specs.pdf_property_spec  import FilePropertySpec
from feature_extractor.settings import YARA_RULES_PATH


class YaraAdapter:

    @exception_handler
    def collect_properties(self, file_path, prop_spec: FilePropertySpec = None):
        """
        Processing yara rules
        :return: Matched Yara signatures dict or None.
        """
        signatures = self.get_yara_signatures(file_path)
        if signatures:
            prop_spec.yara_signatures = signatures

    @timeout_decorator.timeout(55, use_signals=False)
    def get_yara_signatures(self, file_path):
        """Processing yara rules"""
        rules = yara.compile(YARA_RULES_PATH)
        match = rules.match(os.path.abspath(file_path))
        return [str(sig) for sig in match]