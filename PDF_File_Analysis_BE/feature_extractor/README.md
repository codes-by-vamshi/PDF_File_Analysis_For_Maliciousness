# Instruction of running feature extraction tool 
First you need to login to the system using your credentials.

## About Dataset
We have a collection of pdf files prepared fot this project.
The /dataset/ folder contains two subfolders
- malicious   ( bad files )
- benign      ( good files )
Each folder contains 5000 pdf files in them.

## Feature Extraction
We have prepare a  feature extractor tool that will help you extracting relevant properties from pdf file.
it accept 3 parameters: 
- 1. input path [ --in ]( ex. /dataset/malicious)
- 2. category   [--cat ] ( malicious or benign)
- 3. output path [ --out ]( ex. features/ )

usage for malicious : extract_feature --in /dataset/malicious --cat malicious --out features
usage for benign    : extract_feature --in /dataset/benign    --cat benign    --out features

You can find the extracted features in json format in  respective category inside output directory .
for above example . features/malicious/ will contains all the extracted feature for malicious category

This feature extractor utilize the open source library if you are intrested you can check this link https://pypdf2.readthedocs.io/en/3.0.0/

## About extracted Features
1. exif_signatures
Description: Metadata signatures obtained from the Exchangeable image file format (EXIF).
Type: Dictionary
Example: {}
2. file_size
Description: Size of the file in bytes.
Type: Integer
Example: 116616
3. pdfid_signatures
Description: Signatures obtained using PDFiD tool.
Type: Dictionary
Example: {}
4. pypdf_uris
Description: List of URIs (Uniform Resource Identifiers) extracted using PyPDF2 library.
Type: List of Strings
Example:
perl
[
    "http://getpdf.pw/book?res=123&isbn=9780375864957&kwd=The%20Red%20Blazer%20Girls:%20The%20Secret%20Cellar",
    "https://img1.wsimg.com/blobby/go/74966dab-a283-4c4c-a9b9-f0069f6329e4/the-reception-year-in-action-revised-and-updat.pdf"
]


5. regex_uris
Description: List of URIs extracted using regular expressions.
Type: List of Strings
Example:
["https://static.s123-cdn-static-a.com/uploads/4660132/normal_61b0fa3584419.pdf"]


6. regex_urls
Description: List of URL patterns extracted using regular expressions.
Type: List of Strings
Example:


[    "http://getpdf.pw/book?res=123"]


7. scripts
Description: Information about scripts present in the document.
Type: Dictionary
Example:
{
    "iframe": [],
    "urls": []
}


8. static_properties
Description: Various static properties extracted from the document.
Type: Dictionary
- JBIG2Decode
        Description: This property indicates whether the JBIG2Decode filter is used in the PDF. JBIG2 is an image compression standard.
        Value: "0" (Not used), "1" (Used)

- XML_forms
        Description: Indicates the presence of XML forms in the PDF document.
        Value: "0" (Not present), "1" (Present)

- acro_form
        Description: Indicates the presence of AcroForms (interactive forms in PDF) in the document.
        Value: "0" (Not present), "1" (Present)

- auto_action
        Description: Indicates whether there are automatic actions defined in the PDF.
        Value: "0" (Not defined), "1" (Defined)

- colors
        Description: Indicates the use of color in the PDF.
        Value: "0" (No color), "1" (Color used)

- cross_reference_table
        Description: Indicates the integrity of the cross-reference table in the PDF.
        Value: "0" (Not valid), "1" (Valid)

- embedded_files
        Description: Indicates the presence of embedded files in the PDF.
        Value: "0" (Not present), "1" (Present)

- file_size
        Description: Size of the file in bytes.

- java_script
        Description: Indicates the presence of JavaScript in the PDF.
        Value: "0" (Not present), "1" (Present)

- js
        Description: Alias for JavaScript property.

- launch_action
        Description: Indicates the presence of launch actions in the PDF.
        Value: "0" (Not present), "1" (Present)

- object_end
        Description: Position of the end of an object in the PDF.

- object_start
        Description: Position of the start of an object in the PDF.

- object_streams
        Description: Indicates the use of object streams in the PDF.
        Value: "0" (Not used), "1" (Used)

- open_action
        Description: Indicates the presence of open actions in the PDF.
        Value: "0" (Not present), "1" (Present)

- page_count
        Description: Number of pages in the PDF.

- rich_media
        Description: Indicates the presence of rich media (audio, video) in the PDF.
        Value: "0" (Not present), "1" (Present)

- start_cross_reference_table
        Description: Indicates the start of the cross-reference table in the PDF.
        Value: "0" (Not present), "1" (Present)

- stream_end
        Description: Position of the end of a stream in the PDF.

- stream_start
        Description: Position of the start of a stream in the PDF.

- trailer_dictionary
        Description: Indicates the presence of the trailer dictionary in the PDF.
        Value: "0" (Not present), "1" (Present)

example: 
{
    "JBIG2Decode": "0",
    "XML_forms": "0",
    "acro_form": "0",
    "auto_action": "0",
    "colors": "0",
    "cross_reference_table": "1",
    "embedded_files": "0",
    "file_size": "117",
    "java_script": "0",
    "js": "0",
    "launch_action": "0",
    "object_end": "79",
    "object_start": "79",
    "object_streams": "0",
    "open_action": "0",
    "page_count": "8",
    "rich_media": "0",
    "start_cross_reference_table": "1",
    "stream_end": "15",
    "stream_start": "15",
    "trailer_dictionary": "1"
}


9. yara_signatures
Description: Signatures obtained using YARA rules.
Type: List of Strings
Example:
["without_attachments",    "without_images",    "with_urls",    "invalid_trailer_structure",    "contentis_base64"]
NOTE: these yara rules differs with every files 

