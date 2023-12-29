from typing import Dict, List

from .file_property_spec import FilePropertySpec


""" class PeePdf:
    Javascript: Dict
    AutoAction: Dict
    OpenAction: Dict
    ObfuscatedNames: Dict
    AcroForm: Dict
    LaunchEvent: Dict
    EmbeddedFiles: Dict
    XMLForms: Dict
    CVE: Dict
    urls: List = [] """


class Static:
    page_count: int
    object_start: int
    object_end: int
    stream_start: int
    stream_end: int
    cross_reference_table: int
    trailer_dictionary: int
    start_cross_reference_table: int
    object_streams: int
    js: int
    java_script: int
    auto_action: int
    open_action: int
    acro_form: int
    rich_media: int
    launch_action: int
    embedded_files: int
    JBIG2Decode: int
    XML_forms: int
    colors: int
    file_size: int


class Exif:
    invalid_xref_table: Dict
    Linearized: Dict


class Pdfid:
    Page_Count: Dict
    Object_Mismatch: Dict
    Stream_Mismatch: Dict
    Rich_Media: Dict
    Encrypted: Dict
    Obfuscated_Obj: Dict


class PdfPropertySpec(FilePropertySpec):
    # peepdf_signatures: PeePdf
    exif_signatures: Exif
    static_properties: Static
    pdfid_signatures: Pdfid
    pypdf_uris: List
    regex_uris: List
    regex_urls: List

    def __init__(self):
        super().__init__()
        # self.peepdf_signatures: PeePdf = PeePdf()
        self.exif_signatures: Exif = Exif()
        self.static_properties: Static = Static()
        self.pdfid_signatures: Pdfid = Pdfid()
        self.pypdf_uris: List = []
        self.regex_uris: List = []
        self.regex_urls: List = []
