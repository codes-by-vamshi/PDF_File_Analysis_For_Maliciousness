from .enabled_properties import PDFID_SIGNATURES, STATIC_PROPERTIES, PDFID_BIN_PATH
from .tool_adapter import _create_subprocess, create_sig, exception_handler
from feature_extractor.property_specs.pdf_property_spec  import PdfPropertySpec


class PdfIdAdapter:

    @exception_handler
    def collect_properties(self, file_path, prop_spec: PdfPropertySpec = None):
        """
        Function that processing pdfid output and adds the signatures to the report
        :return: None.
        """
        # Run pdfid to get the output
        
        pdfid_out, _ = _create_subprocess(PDFID_BIN_PATH, [file_path])
        # Search for static properties

        # adding signatures
        start_obj = 0
        end_obj = 0
        start_stream = 0
        end_stream = 0
        for line in pdfid_out.strip().split('\n'):
            prop_value = ((line.split()[-1]).split('('))[0]
            for key in STATIC_PROPERTIES:
                if line.startswith(" " + key):
                    value = STATIC_PROPERTIES[key]
                    for property_value in value:
                        value[property_value] = prop_value
                        setattr(prop_spec.static_properties, property_value, prop_value)

            if line.startswith(" obj"):
                start_obj = int(prop_value)
            elif line.startswith(" endobj"):
                end_obj = int(prop_value)
            elif line.startswith(" stream"):
                start_stream = int(prop_value)
            elif line.startswith(" endstream"):
                end_stream = int(prop_value)

            # check for one page documents signature
            elif line.startswith(" /Page"):
                if (prop_value == '0') or (prop_value == '1'):
                    prop_spec.pdfid_signatures.Page_Count = create_sig(PDFID_SIGNATURES["Page_Count"], line)

            # check for other signatures
            for key in PDFID_SIGNATURES:
                if line.startswith(" " + key):
                    if prop_value != '0':
                        setattr(prop_spec.pdfid_signatures, key, create_sig(PDFID_SIGNATURES[key], line))

            # add obfuscated signature
            if "(" in line:
                prop_spec.pdfid_signatures.Obfuscated_Obj = create_sig(PDFID_SIGNATURES["Obfuscated_Obj"], line)

        if start_obj != end_obj:
            prop_spec.pdfid_signatures.Object_Mismatch = create_sig(PDFID_SIGNATURES["Object_Mismatch"])
            prop_spec.pdfid_signatures.Stream_Mismatch = create_sig(PDFID_SIGNATURES["Stream_Mismatch"])
