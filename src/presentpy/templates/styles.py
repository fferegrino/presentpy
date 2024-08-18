from pathlib import Path

from presentpy.constants import (
    CODE_HIGHLIGHT_PARAGRAPH_STYLE_NAME,
    DEFAULT_PAGE_LAYOUT_NAME,
    DEFAULT_STYLE_NAME,
    DRAWING_PAGE_STYLE_NAME,
    OUTPUT_FRAME_STYLE_NAME,
)
from presentpy.namespaces import Namespaces
from presentpy.templates.xml_file import XMLFile
from presentpy.writer.slide_tag import (
    BlankSlide,
    ImageSlide,
    TitleAndCodeSlide,
    TitleAndContentSlide,
    TitleAndImageSlide,
    TitleAndObjectSlide,
    TitleCodeAndOutputSlide,
    TitleSlide,
)
from presentpy.writer.tag import Tag
from presentpy.writer.theme import Theme


class Styles(XMLFile):

    def __init__(self, path: Path, namespaces: Namespaces, theme: Theme):
        super().__init__(path, namespaces)
        self.theme = theme

        self.automatic_styles = self.xpath("office:document-styles", "office:automatic-styles")
        self.styles = self.xpath("office:document-styles", "office:styles")

        page_layout_properties = self.xpath(
            "office:document-styles",
            "office:automatic-styles",
            f"style:page-layout[@style:name='{DEFAULT_PAGE_LAYOUT_NAME}']",
            "style:page-layout-properties",
        )
        page_layout_properties.set(namespaces("fo:page-width"), f"{self.theme.width:.2f}in")
        page_layout_properties.set(namespaces("fo:page-height"), f"{self.theme.height:.2f}in")

        drawing_page_properties = self.xpath(
            "office:document-styles",
            "office:automatic-styles",
            f"style:style[@style:name='{DEFAULT_STYLE_NAME}']",
            "style:drawing-page-properties",
        )
        drawing_page_properties.set(namespaces("draw:fill-color"), self.theme.background_color)

        master_title_text_properties = self.xpath(
            "office:document-styles",
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
                "office:document-styles",
                "office:automatic-styles",
                f"style:style[@style:name='{span_styles}']",
                "style:text-properties",
            )
            master_content_text_properties.set(namespaces("fo:color"), self.theme.content_color)
            master_content_text_properties.set(namespaces("fo:font-size"), self.theme.content_font_size)
            master_content_text_properties.set(namespaces("style:font-size-asian"), self.theme.content_font_size)
            master_content_text_properties.set(namespaces("style:font-size-complex"), self.theme.content_font_size)

        default_slide_properties = self.xpath(
            "office:document-styles",
            "office:automatic-styles",
            f"style:style[@style:name='{DRAWING_PAGE_STYLE_NAME}']",
            "style:drawing-page-properties",
        )
        default_slide_properties.set(namespaces("draw:fill-color"), self.theme.background_color)

        highlighted_code_paragraph_style = self.xpath(
            "office:document-styles",
            "office:automatic-styles",
            f"style:style[@style:name='{CODE_HIGHLIGHT_PARAGRAPH_STYLE_NAME}']",
            "style:text-properties",
        )
        highlighted_code_paragraph_style.set(namespaces("fo:background-color"), self.theme.highlight_color)
        highlighted_code_paragraph_style.set(namespaces("fo:font-weight"), "bold")

        output_frame_text_properties = self.xpath(
            "office:document-styles",
            "office:automatic-styles",
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
            TitleAndImageSlide("TitleAndImage", self.namespaces, self.theme),
            ImageSlide("Image", self.namespaces, self.theme),
            TitleAndObjectSlide("TitleAndObject", self.namespaces, self.theme),
        ]

        for slide in slides:
            master_page = slide.to_master_page(DEFAULT_PAGE_LAYOUT_NAME, DEFAULT_STYLE_NAME)
            maaster_styles.append(master_page.to_element())
            background_style = Tag(
                "style:style",
                self.namespaces,
                {
                    "style:name": f"{master_page['style:name']}-background",
                    "style:family": "presentation",
                },
            )
            graphic_properties = Tag(
                "style:graphic-properties",
                self.namespaces,
                {
                    "draw:stroke": "none",
                    "draw:fill": "solid",
                    "draw:fill-color": self.theme.background_color,
                },
            )
            background_style.append(graphic_properties)
            self.automatic_styles.append(background_style.to_element())
