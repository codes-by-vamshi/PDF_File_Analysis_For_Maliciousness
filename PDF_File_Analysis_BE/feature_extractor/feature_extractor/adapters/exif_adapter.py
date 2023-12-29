from .enabled_properties import EXIF_TOOL_SIGNATURES
from .tool_adapter import _create_subprocess, create_sig, exception_handler
from feature_extractor.property_specs.pdf_property_spec  import PdfPropertySpec


class ExifAdapter:

    @exception_handler
    def collect_properties(self, file_path=None, prop_spec: PdfPropertySpec = None):
        # Run ExifTool to get the output
        exif_out, exif_err = _create_subprocess('exiftool', [file_path])
        for line in exif_out.split('\n'):
            if "Invalid xref table" in line:
                prop_spec.exif_signatures.invalid_xref_table = create_sig(EXIF_TOOL_SIGNATURES['InvalidXrefTable'], line)

            if ("Linearized" in line) and ("Yes" in line):
                prop_spec.exif_signatures.linearized = create_sig(EXIF_TOOL_SIGNATURES["Linearized"], line)
            if "File Size" in line and 'Slug' not in line:
                # TODO needs to convert this to use kb,mb
                prop_spec.static_properties.file_size = line.split()[-2]
