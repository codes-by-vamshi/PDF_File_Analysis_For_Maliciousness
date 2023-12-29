from .file_feature_spec import FileFeatureSpec, fields, Schema, Signatures, SignaturesMeta, Count


class Static(Schema):
    page_count = fields.Integer()
    object_start = fields.Integer()
    object_end = fields.Integer()
    stream_start = fields.Integer()
    stream_end = fields.Integer()
    cross_reference_table = fields.Integer()
    trailer_dictionary = fields.Integer()
    start_cross_reference_table = fields.Integer()
    object_streams = fields.Integer()
    js = fields.Integer()
    java_script = fields.Integer()
    auto_action = fields.Integer()
    open_action = fields.Integer()
    acro_form = fields.Integer()
    rich_media = fields.Integer()
    launch_action = fields.Integer()
    embedded_files = fields.Integer()
    JBIG2Decode = fields.Integer()
    XML_forms = fields.Integer()
    colors = fields.Integer()
    # TODO remove
    #file_size = fields.Float()


class Pdfid(SignaturesMeta):
    Page_Count = fields.Nested(Signatures)
    Object_Mismatch = fields.Nested(Signatures)
    Stream_Mismatch = fields.Nested(Signatures)
    Rich_Media = fields.Nested(Signatures)
    Encrypted = fields.Nested(Signatures)
    Obfuscated_Obj = fields.Nested(Signatures)


class Exif(SignaturesMeta):
    invalid_xref_table = fields.Nested(Signatures)
    linearized = fields.Nested(Signatures)


""" class PeePdf(SignaturesMeta):
    JavaScript = fields.Nested(Signatures)
    AutoAction = fields.Nested(Signatures)
    OpenAction = fields.Nested(Signatures)
    Names = fields.Nested(Signatures)
    AcroForm = fields.Nested(Signatures)
    LaunchEvent = fields.Nested(Signatures)
    EmbeddedFiles = fields.Nested(Signatures)
    XMLForms = fields.Nested(Signatures)
    CVE = fields.Nested(Signatures)
    urls = Count() """


class PdfFeatureSpec(FileFeatureSpec):
    # peepdf_signatures = fields.Nested(PeePdf)
    static_properties = fields.Nested(Static)
    pdfid_signatures = fields.Nested(Pdfid)
    exif_signatures = fields.Nested(Exif)
    pypdf_uris = Count()
    regex_uris = Count()
    regex_urls = Count()
