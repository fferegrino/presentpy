import os
import re
import sys
import xml.dom.minidom

from lxml import etree


def inches_to_cm(inches):
    return float(inches) * 2.54


def convert_attributes(element):
    for attr, value in element.attrib.items():
        if isinstance(value, str) and value.endswith("in"):
            match = re.match(r"([\d.]+)in", value)
            if match:
                inches = float(match.group(1))
                cm = inches_to_cm(inches)
                element.attrib[attr] = f"{cm:.2f}cm"

    for child in element:
        convert_attributes(child)


def process_xml_file(file_path):
    # Parse the XML file and get the root
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()

    # Convert attributes
    convert_attributes(root)

    # Save the modified XML

    xml_string = etree.tostring(root, pretty_print=True)
    dom = xml.dom.minidom.parseString(xml_string)
    pretty_xml_as_string = dom.toprettyxml()
    pretty_xml_as_string = "\n".join([line for line in pretty_xml_as_string.split("\n") if line.strip()])
    pretty_xml_as_string = re.sub(r'(xmlns:\w+="[^"]+")', r"\n\t\1", pretty_xml_as_string)
    pretty_xml_as_string = pretty_xml_as_string.replace(" office:version", "\noffice:version", 1)
    with open(file_path, "w") as f:
        f.write(pretty_xml_as_string)
        f.write("\n")


def main():

    directory = sys.argv[1]
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory, filename)
            print(f"Processing: {file_path}")
            process_xml_file(file_path)


if __name__ == "__main__":
    main()
