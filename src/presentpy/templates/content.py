from pathlib import Path
from typing import Optional

from lxml import etree

from presentpy.namespaces import Namespaces
from presentpy.templates.xml_file import XMLFile
from presentpy.writer.theme import Theme


class Content(XMLFile):

    def __init__(self, path: Path, namespaces: Namespaces, theme: Theme):
        super().__init__(path, namespaces)
        self.theme = theme
        self.automatic_styles = self.xpath("office:document-content", "office:automatic-styles")
        self.presentation = self.xpath("office:document-content", "office:body", "office:presentation")

    def write(self, path: Optional[Path] = None, prettify: bool = False):
        etree.indent(self.automatic_styles)
        super().write(path, prettify=prettify)
