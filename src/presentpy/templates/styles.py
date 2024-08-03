from pathlib import Path

from presentpy.constants import *
from presentpy.namespaces import Namespaces
from presentpy.templates.xml_file import XMLFile
from presentpy.writer.slide_tag import (
    BlankSlide,
    TitleAndCodeSlide,
    TitleAndContentSlide,
    TitleCodeAndOutputSlide,
    TitleSlide,
)
from presentpy.writer.theme import Theme


class Styles(XMLFile):

    def __init__(self, path: Path, namespaces: Namespaces, theme: Theme):
        super().__init__(path, namespaces)
        self.theme = theme

        page_layout_properties = self.xpath(
            "office:document-styles",
            "office:styles",
            "style:page-layout[@style:name='pageLayout1']",
            "style:page-layout-properties",
        )
        page_layout_properties.set(namespaces("fo:page-width"), f"{self.theme.width:.2f}in")
        page_layout_properties.set(namespaces("fo:page-height"), f"{self.theme.height:.2f}in")

        drawing_page_properties = self.xpath(
            "office:document-styles",
            "office:styles",
            "style:style[@style:name='masterStyle']",
            "style:drawing-page-properties",
        )
        drawing_page_properties.set(namespaces("draw:fill-color"), self.theme.background_color)

        master_title_text_properties = self.xpath(
            "office:document-styles",
            "office:styles",
            f"style:style[@style:name='{MASTER_TITLE_STYLE_NAME}']",
            "style:text-properties",
        )
        master_title_text_properties.set(namespaces("fo:color"), self.theme.title_color)
        master_title_text_properties.set(namespaces("fo:font-size"), self.theme.font_size(48))
        master_title_text_properties.set(namespaces("style:font-size-asian"), self.theme.font_size(48))
        master_title_text_properties.set(namespaces("style:font-size-complex"), self.theme.font_size(48))

        master_content_text_properties = self.xpath(
            "office:document-styles",
            "office:styles",
            f"style:style[@style:name='{MASTER_CONTENT_STYLE_NAME}']",
            "style:text-properties",
        )

        master_content_text_properties.set(namespaces("fo:color"), self.theme.content_color)
        master_content_text_properties.set(namespaces("fo:font-size"), self.theme.font_size(24))
        master_content_text_properties.set(namespaces("style:font-size-asian"), self.theme.font_size(24))
        master_content_text_properties.set(namespaces("style:font-size-complex"), self.theme.font_size(24))

        default_slide_properties = self.xpath(
            "office:document-styles",
            "office:styles",
            f"style:style[@style:name='{DRAWING_PAGE_STYLE_NAME}']",
            "style:drawing-page-properties",
        )
        default_slide_properties.set(namespaces("draw:fill-color"), self.theme.background_color)

        highlighted_code_paragraph_style = self.xpath(
            "office:document-styles",
            "office:styles",
            f"style:style[@style:name='{CODE_HIGHLIGHT_PARAGRAPH_STYLE_NAME}']",
            "style:text-properties",
        )
        highlighted_code_paragraph_style.set(namespaces("fo:background-color"), self.theme.highlight_color)
        highlighted_code_paragraph_style.set(namespaces("fo:font-weight"), "bold")

        output_frame_text_properties = self.xpath(
            "office:document-styles",
            "office:styles",
            f"style:style[@style:name='{OUTPUT_FRAME_STYLE_NAME}']",
            "style:text-properties",
        )
        output_frame_text_properties.set(namespaces("fo:color"), self.theme.content_color)

        # Add Master Slide Styles

        maaster_styles = self.xpath(
            "office:document-styles",
            "office:master-styles",
        )
        slides = [
            BlankSlide("Blank", self.namespaces, self.theme),
            TitleSlide("Title", self.namespaces, self.theme),
            TitleAndContentSlide("TitleAndContent", self.namespaces, self.theme),
            TitleAndCodeSlide("TitleAndCode", self.namespaces, self.theme),
            TitleCodeAndOutputSlide("TitleCodeAndOutput", self.namespaces, self.theme),
        ]

        for idx, slide in enumerate(slides):
            prefix = MASTER_SLIDE_PREFIX
            if idx > 0:
                prefix = f"{prefix}-Layout{idx}"
            prefix = f"{prefix}-thing"
            master_page = slide.to_master_page(prefix, DEFAULT_PAGE_LAYOUT_NAME, DEFAULT_STYLE_NAME)
            maaster_styles.append(master_page.to_element())
