from PyPDF2 import PdfReader

from .tool_adapter import exception_handler
from feature_extractor.property_specs.pdf_property_spec import PdfPropertySpec

class Pypdf2Adapter:

    @exception_handler
    def collect_properties(self, file_path, prop_spec: PdfPropertySpec = None):
        # TODO ff15b60eec02add11d2ecb79a8e8def3282c537df75e78ff18940c05e6ddee3d
        # file has uris obtained from peepdf/pypdf2 but not with regex matcher
        pdf = PdfReader(file_path)
        pages = len(pdf.pages)
        key, uri, anchor = '/Annots', '/URI', '/A'
        for page in range(pages):
            pageSliced = pdf.pages[page]
            pageObject = pageSliced.get_object()  # Change here
            try:
                if key in pageObject.keys():
                    for annots in pageObject[key]:
                        u = annots.get_object()  # Change here
                        if uri in u[anchor].keys():
                            prop_spec.pypdf_uris.append(u[anchor][uri])
            except Exception as exc:
                pass
