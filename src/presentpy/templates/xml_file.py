import xml.dom.minidom
from pathlib import Path

from lxml import etree

from presentpy.namespaces import Namespaces


class XMLFile:

    def __init__(self, path: Path, namespaces: Namespaces):
        self.path = path
        self.namespaces = namespaces
        with open(path, "r") as f:
            self.xml = etree.fromstring(f.read())

    def xpath(self, *path_from_root, single=True):
        if len(path_from_root) == 1 and path_from_root[0].startswith("/"):
            xpath = path_from_root[0]
        else:
            xpath = "/" + ("/".join(path_from_root))

        result = self.xml.xpath(xpath, namespaces=self.namespaces.data)
        if single:
            return result[0]
        return result

    def write(self, output_path=None, prettify=False):
        if output_path is None:
            output_path = self.path
        with open(output_path, "w") as f:
            xml_string = etree.tostring(self.xml, pretty_print=True)
            if prettify:
                dom = xml.dom.minidom.parseString(xml_string)
                pretty_xml_as_string = dom.toprettyxml()
                pretty_xml_as_string = "\n".join([line for line in pretty_xml_as_string.split("\n") if line.strip()])
                f.write(pretty_xml_as_string)
            else:
                f.write(xml_string.decode())
