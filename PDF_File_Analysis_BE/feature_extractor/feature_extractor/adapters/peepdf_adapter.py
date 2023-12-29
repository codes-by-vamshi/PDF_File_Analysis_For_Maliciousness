import peepdf

from .enabled_properties import PEEPDF_SIGNATURES
from .tool_adapter import _create_subprocess, create_sig, exception_handler
from feature_extractor.property_specs.pdf_property_spec  import PdfPropertySpec


class PeePdfAdapter:

    @exception_handler
    def collect_properties(self, file_path, prop_spec: PdfPropertySpec = None):
        # TODO PEEPDF use getStats() method to get suspicous elements
        peepdf_out, _ = _create_subprocess('peepdf', ['-f', file_path])
        suspicious_found = False
        # Search for beginning of suspicious objects
        for line in peepdf_out.split('\n'):
            if "Suspicious" in line:
                suspicious_found = True
                continue

            if not suspicious_found:
                continue
            # Search for each suspicous signature
            for key in PEEPDF_SIGNATURES:
                # IF this is current suspicious signature
                if key in line:
                    setattr(prop_spec.peepdf_signatures, key, create_sig(PEEPDF_SIGNATURES[key], line))

        p = peepdf.PDFCore.PDFParser()
        r, f = p.parse(
            file_path, forceMode=True,
            looseMode=True, manualAnalysis=False
        )
        if r:
            print("Error parsing PDF file, error code %s", r)
            return

        for version in range(f.updates + 1):
            for obj in f.body[version].objects.values():
                if obj.object.type == "dictionary":
                    for url in obj.object.urlsFound:
                        prop_spec.peepdf_signatures.urls.append(url)

                    for url in obj.object.uriList:
                        prop_spec.peepdf_signatures.urls.append(url)
