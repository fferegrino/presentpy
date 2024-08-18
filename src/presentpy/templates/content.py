from pathlib import Path
from typing import Optional

from lxml import etree

from presentpy.constants import (
    CODE_HIGHLIGHT_PARAGRAPH_STYLE_NAME,
    DEFAULT_PAGE_LAYOUT_NAME,
    DEFAULT_STYLE_NAME,
    DRAWING_PAGE_STYLE_NAME,
    MASTER_CONTENT_STYLE_NAME,
    MASTER_TITLE_STYLE_NAME,
    OUTPUT_FRAME_STYLE_NAME,
)
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
            "office:automatic-styles",
            f"style:page-layout[@style:name='{DEFAULT_PAGE_LAYOUT_NAME}']",
            "style:page-layout-properties",
        )
        page_layout_properties.set(namespaces("fo:page-width"), f"{self.theme.width:.2f}in")
        page_layout_properties.set(namespaces("fo:page-height"), f"{self.theme.height:.2f}in")

        drawing_page_properties = self.xpath(
            "office:document-content",
            "office:automatic-styles",
            f"style:style[@style:name='{DEFAULT_STYLE_NAME}']",
            "style:drawing-page-properties",
        )
        drawing_page_properties.set(namespaces("draw:fill-color"), self.theme.background_color)

        master_title_text_properties = self.xpath(
            "office:document-content",
            "office:automatic-styles",
            f"style:style[@style:name='{MASTER_TITLE_STYLE_NAME}']",
            "style:text-properties",
        )
        master_title_text_properties.set(namespaces("fo:color"), self.theme.title_color)
        master_title_text_properties.set(namespaces("fo:font-size"), self.theme.title_font_size)
        master_title_text_properties.set(namespaces("style:font-size-asian"), self.theme.title_font_size)
        master_title_text_properties.set(namespaces("style:font-size-complex"), self.theme.title_font_size)

        master_content_text_properties = self.xpath(
            "office:document-content",
            "office:automatic-styles",
            f"style:style[@style:name='{MASTER_CONTENT_STYLE_NAME}']",
            "style:text-properties",
        )
        master_content_text_properties.set(namespaces("fo:color"), self.theme.content_color)
        master_content_text_properties.set(namespaces("fo:font-size"), self.theme.content_font_size)
        master_content_text_properties.set(namespaces("style:font-size-asian"), self.theme.content_font_size)
        master_content_text_properties.set(namespaces("style:font-size-complex"), self.theme.content_font_size)

        default_slide_properties = self.xpath(
            "office:document-content",
            "office:automatic-styles",
            f"style:style[@style:name='{DRAWING_PAGE_STYLE_NAME}']",
            "style:drawing-page-properties",
        )
        default_slide_properties.set(namespaces("draw:fill-color"), self.theme.background_color)

        highlighted_code_paragraph_style = self.xpath(
            "office:document-content",
            "office:automatic-styles",
            f"style:style[@style:name='{CODE_HIGHLIGHT_PARAGRAPH_STYLE_NAME}']",
            "style:text-properties",
        )
        highlighted_code_paragraph_style.set(namespaces("fo:background-color"), self.theme.highlight_color)
        highlighted_code_paragraph_style.set(namespaces("fo:font-weight"), "bold")

        output_frame_text_properties = self.xpath(
            "office:document-content",
            "office:automatic-styles",
            f"style:style[@style:name='{OUTPUT_FRAME_STYLE_NAME}']",
            "style:text-properties",
        )
        output_frame_text_properties.set(namespaces("fo:color"), self.theme.content_color)

        list_level_style_bullet = self.xpath(
            "office:document-content",
            "office:automatic-styles",
            "text:list-style[@style:name='list']",
            "text:list-level-style-bullet",
            single=False,
        )
        for bullet in list_level_style_bullet:
            text_properties = bullet.xpath("style:text-properties", namespaces=self.namespaces.data)[0]
            text_properties.set(namespaces("fo:color"), self.theme.content_color)

    def write(self, path: Optional[Path] = None, prettify: bool = False):
        etree.indent(self.automatic_styles)
        super().write(path, prettify=prettify)
