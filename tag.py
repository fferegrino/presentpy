import re
from typing import Dict, List, Optional

from lxml import etree, objectify

from ns import namespaces, ns


class Tag:
    def __init__(self, element_name: str, attributes: Optional[Dict[str, str]] = None):
        self.element_name = element_name
        self.attributes = attributes or {}
        self.children: List[Tag] = []

    def append(self, tag: "Tag"):
        self.children.append(tag)

    @staticmethod
    def _cleanup_xml(element):
        objectify.deannotate(element, cleanup_namespaces=True)
        return element

    @staticmethod
    def _to_xml_str(element):
        element = etree.tostring(element).decode()
        # Remove strings matching `\sxmlns:[a-z]+=\"[\w:0-9.]+\"`
        element = re.sub(r"\sxmlns:[a-z]+=\"[\w:0-9.]+\"", "", element)
        return element

    def to_element(self):
        new_page = etree.Element(ns(self.element_name), nsmap=namespaces)

        for attr, value in self.attributes.items():
            new_page.set(ns(attr), value)

        for child in self.children:
            new_page.append(child.to_element())

        return new_page

    def __str__(self):

        new_page = self.to_element()

        Tag._cleanup_xml(new_page)
        return Tag._to_xml_str(new_page)

    def __repr__(self) -> str:
        return str(self)
