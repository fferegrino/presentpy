import re
from typing import Dict, List, Optional

from lxml import etree, objectify

from presentpy.namespaces import Namespaces


class Tag:
    def __init__(self, element_name: str, namespaces: Namespaces, attributes: Optional[Dict[str, str]] = None):
        self.namespaces = namespaces
        self.element_name = element_name
        self.attributes = attributes or {}
        self.text: Optional[str] = None
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
        element = re.sub(r"\sxmlns:[a-z]+=\"[\w:0-9.]+\"", "", element)
        return element

    def to_element(self):
        new_page = etree.Element(self.namespaces(self.element_name), nsmap=self.namespaces.data)

        if self.text is not None:
            new_page.text = self.text

        for attr, value in self.attributes.items():
            new_page.set(self.namespaces(attr), value)

        for child in self.children:
            new_page.append(child.to_element())

        return new_page

    def __str__(self):
        new_page = self.to_element()

        Tag._cleanup_xml(new_page)
        return Tag._to_xml_str(new_page)

    def __repr__(self) -> str:
        return str(self)
