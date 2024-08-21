import re
import sys
import xml.dom.minidom
from pathlib import Path

from lxml import etree


def sort_attributes(elem):
    """Sort attributes of an element alphabetically."""
    attrib = elem.attrib
    if len(attrib) > 0:
        sorted_attr = sorted(
            attrib.items(),
        )
        elem.attrib.clear()
        elem.attrib.update(sorted_attr)
    for child in elem:
        sort_attributes(child)


def pretty_print_xml(xml_string):
    """Pretty print XML string, preserving namespaces and sorting attributes."""
    # Parse the XML string
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(xml_string, parser)

    # Sort attributes
    sort_attributes(root)

    # Convert back to string with pretty printing
    xml_string = etree.tostring(root, pretty_print=True)
    dom = xml.dom.minidom.parseString(xml_string)
    pretty_xml_as_string = dom.toprettyxml()
    pretty_xml_as_string = "\n".join([line for line in pretty_xml_as_string.split("\n") if line.strip()])
    pretty_xml_as_string = re.sub(r'(xmlns:\w+="[^"]+")', r"\n\t\1", pretty_xml_as_string)
    pretty_xml_as_string = pretty_xml_as_string.replace(" office:version", "\noffice:version", 1)

    return pretty_xml_as_string


path = sys.argv[1]
check = sys.argv[2] if len(sys.argv) > 2 else None


path = Path(path)

for file in path.rglob("*.xml"):
    with open(file, "r") as f:
        xml_string = f.read()

    pretty_xml = pretty_print_xml(xml_string)

    if check:
        assert pretty_xml.rstrip() == xml_string.rstrip()

    else:
        with open(file, "w") as f:
            f.write(pretty_xml)
            f.write("\n")
