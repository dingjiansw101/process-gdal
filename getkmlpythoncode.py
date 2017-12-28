from pykml import parser
from os import path
from pykml.factory import write_python_script_for_kml_document

kml_file = r'G:\LocaSpaceViewer\LocaSpaceViewer\download\TaskIMG12131725\TaskIMG12131725.kml'
with open(kml_file) as f:
    doc = parser.parse(f)
    script = write_python_script_for_kml_document(doc)
    print script