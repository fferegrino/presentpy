from pathlib import Path
from typing import Optional

from lxml import etree

from presentpy.constants import (
    CODE_HIGHLIGHT_PARAGRAPH_STYLE_NAME,
    DEFAULT_STYLE_NAME_FOR_CONTENT,
    DRAWING_PAGE_STYLE_NAME,
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
        self.styles = self.xpath("office:document-content", "office:styles")
        self.presentation = self.xpath("office:document-content", "office:body", "office:presentation")

        drawing_page_properties = self.xpath(
            "office:document-content",
            "office:automatic-styles",
            f"style:style[@style:name='{DEFAULT_STYLE_NAME_FOR_CONTENT}']",
            "style:drawing-page-properties",
        )
        drawing_page_properties.set(namespaces("draw:fill-color"), self.theme.background_color)

        master_title_text_properties = self.xpath(
            "office:document-content",
            "office:automatic-styles",
            "style:style[@style:name='masterTitleSpan']",
            "style:text-properties",
        )
        master_title_text_properties.set(namespaces("fo:color"), self.theme.title_color)
        master_title_text_properties.set(namespaces("fo:font-size"), self.theme.title_font_size)
        master_title_text_properties.set(namespaces("style:font-size-asian"), self.theme.title_font_size)
        master_title_text_properties.set(namespaces("style:font-size-complex"), self.theme.title_font_size)

        for span_styles in [
            "content_span",
            "content_span__strong",
            "content_span__strikethrough",
            "content_span__emphasis",
            "content_span__underline",
        ]:
            master_content_text_properties = self.xpath(
                "office:document-content",
                "office:automatic-styles",
                f"style:style[@style:name='{span_styles}']",
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
