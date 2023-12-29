PDFID_BIN_PATH = f'/feature_extractor/bin/pdfid/pdfid.py'
PDFID_SIGNATURES = {
    "Page_Count":
        {"name": "Page_Count", "description": "This PDF has only one page", "severity": 1},
    "Object_Mismatch":
        {"name": "Object_Mismatch",
         "description": "The number of start objects does not match with end objects.",
         "severity": 1},
    "Stream_Mismatch":
        {"name": "Stream_Mismatch", "description": "The number of start stream does not match with end streams",
         "severity": 1},
    "RichMedia":
        {"name": "Rich_Media", "description": "The document contains rich media.", "severity": 1},
    "Encrypt":
        {"name": "Encrypted", "description": "The document is password protected.", "severity": 1},
    "Obfuscated_Obj":
        {"name": "Obfuscated_Obj", "description": "The document has objects with obfuscated names.",
         "severity": 1}
}

PEEPDF_SIGNATURES = {
    "JavaScript":
        {"name": "Javascript", "description": "This PDF file contains Javascript blocks.",
         "severity": 1},
    "XFA":
        {"name": "XMLForms", "description": "This PDF file contains XML forms.",
         "severity": 2},
    "AA":
        {"name": "AutoAction", "description": "This PDF file contains autoactions.",
         "severity": 2},
    "OpenAction":
        {"name": "OpenAction", "description": "This PDF file contains open actions at pages.",
         "severity": 2},
    "Names":
        {"name": "ObfuscatedNames", "description": "This PDF file contains obfuscated names.",
         "severity": 2},
    "AcroForm":
        {"name": "AcroForm", "description": "This PDF file contains acroforms.",
         "severity": 2},
    "Launch":
        {"name": "LaunchEvent", "description": "This PDF file contains launch events.",
         "severity": 3},
    "Embedded":
        {"name": "EmbeddedFiles", "description": "This PDF file contains Embedded files.",
         "severity": 3},
    "CVE":
        {"name": "CVE",
         "description": "This PDF file tries to exploit known CVE vulnerability.",
         "severity": 10}
}

# Static properties Dictionary from pdfid
STATIC_PROPERTIES = {
    "/Page": {"page_count": 0},
    "obj": {"object_start": 0},
    "endobj": {"object_end": 0},
    "stream": {"stream_start": 0},
    "endstream": {"stream_end": 0},
    "xref": {"cross_reference_table": 0},
    "trailer": {"trailer_dictionary": 0},
    "startxref": {"start_cross_reference_table": 0},
    "/ObjStm": {"object_streams": 0},
    "/JS": {"js": 0},
    "/JavaScript": {"java_script": 0},
    "/AA": {"auto_action": 0},
    "/OpenAction": {"open_action": 0},
    "/AcroForm": {"acro_form": 0},
    "/RichMedia": {"rich_media": 0},
    "/Launch": {"launch_action": 0},
    "/EmbeddedFile": {"embedded_files": 0},
    "/JBIG2Decode": {"JBIG2Decode": 0},
    "/XFA": {"XML_forms": 0},
    "/Colors": {"colors": 0},
    # TODO remove
    # "File Size": {"file_size": 0},
    "invalidxref": {"invalid_xref": 0}
}

GOOGLE_API_SIGNATURES = {
    "Black_listed_URL":
        {
            "name": "Black_listed_URL",
            "description": "This PDF file contains URLs that are black "
                           "listed by Google.", "severity": 10
        }
}

EXIF_TOOL_SIGNATURES = {
    "InvalidXrefTable": {
        "name": "invalid_xref_table",
        "description": "This PDF file contains invalid cross reference table.",
        "severity": 5
    },
    "Linearized": {
        "name": "linearized",
        "description": "This PDF is linearized",
        "severity": 1
    }
}
