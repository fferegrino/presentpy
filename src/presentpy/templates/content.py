from pathlib import Path
from typing import Optional

from lxml import etree

from presentpy.constants import *
from presentpy.namespaces import Namespaces
from presentpy.templates.xml_file import XMLFile
from presentpy.writer.theme import Theme


class Content(XMLFile):

    def __init__(self, path: Path, namespaces: Namespaces, theme: Theme):
        super().__init__(path, namespaces)
        self.theme = theme
        self.automatic_styles = self.xpath("office:document-content", "office:automatic-styles")
        self.presentation = self.xpath("office:document-content", "office:body", "office:presentation")

        page_layout_properties = self.xpath(
            "office:document-content",
            "office:styles",
            "style:page-layout[@style:name='pageLayout1']",
            "style:page-layout-properties",
        )
        page_layout_properties.set(namespaces("fo:page-width"), f"{self.theme.width:.2f}in")
        page_layout_properties.set(namespaces("fo:page-height"), f"{self.theme.height:.2f}in")

        drawing_page_properties = self.xpath(
            "office:document-content",
            "office:styles",
            "style:style[@style:name='masterStyle']",
            "style:drawing-page-properties",
        )
        drawing_page_properties.set(namespaces("draw:fill-color"), self.theme.background_color)

        master_title_style = self.xpath(
            "office:document-content",
            "office:styles",
            "style:style[@style:name='masterTitle']",
        )
        text_properties = master_title_style.xpath("style:text-properties", namespaces=namespaces.data)[0]
        text_properties.set(namespaces("fo:color"), self.theme.title_color)
        text_properties.set(namespaces("fo:font-size"), self.theme.font_size(48))
        text_properties.set(namespaces("style:font-size-asian"), self.theme.font_size(48))
        text_properties.set(namespaces("style:font-size-complex"), self.theme.font_size(48))

        master_content_style = self.xpath(
            "office:document-content",
            "office:styles",
            "style:style[@style:name='masterContent']",
        )
        text_properties = master_content_style.xpath("style:text-properties", namespaces=namespaces.data)[0]
        text_properties.set(namespaces("fo:color"), self.theme.content_color)
        text_properties.set(namespaces("fo:font-size"), self.theme.font_size(18))
        text_properties.set(namespaces("style:font-size-asian"), self.theme.font_size(18))
        text_properties.set(namespaces("style:font-size-complex"), self.theme.font_size(18))

        default_slide_properties = self.xpath(
            "office:document-content",
            "office:styles",
            f"style:style[@style:name='{DRAWING_PAGE_STYLE_NAME}']",
            "style:drawing-page-properties",
        )
        default_slide_properties.set(namespaces("draw:fill-color"), self.theme.background_color)

        highlighted_code_paragraph_style = self.xpath(
            "office:document-content",
            "office:styles",
            f"style:style[@style:name='{CODE_HIGHLIGHT_PARAGRAPH_STYLE_NAME}']",
            "style:text-properties",
        )
        highlighted_code_paragraph_style.set(namespaces("fo:background-color"), self.theme.highlight_color)
        highlighted_code_paragraph_style.set(namespaces("fo:font-weight"), "bold")

    def write(self, path: Optional[Path] = None, prettify: bool = False):
        etree.indent(self.automatic_styles)
        super().write(path, prettify=prettify)
