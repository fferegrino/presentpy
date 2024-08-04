import importlib.resources
import shutil
import zipfile
from pathlib import Path
from typing import List

import mistletoe
from lxml import etree

from presentpy.code_slide_source import CodeSlideSource
from presentpy.constants import *
from presentpy.namespaces import Namespaces
from presentpy.templates import Content, Styles
from presentpy.writer.slide_tag import (
    BlankSlide,
    SlideTag,
    TitleAndContentSlide,
    TitleCodeAndOutputSlide,
    TitleSlide,
)
from presentpy.writer.tag import Tag
from presentpy.writer.theme import Theme


class Presentation:
    def __init__(self, theme: Theme, namespaces: Namespaces):
        self.theme = theme
        self.namespaces = namespaces
        self.styles: List[Tag] = []
        self.slides: List[SlideTag] = []
        self.current_slide_count = 0

    def new_slide(self, name=None, slide_type: SlideTag = TitleCodeAndOutputSlide):
        if name is None:
            name = f"slide{self.current_slide_count}"
        slide_tag = slide_type(name, self.namespaces, self.theme)
        self.slides.append(slide_tag)
        self.current_slide_count += 1
        return slide_tag

    def new_empty_slide(self, name=None):
        if name is None:
            name = f"slide{self.current_slide_count}"
        slide_tag = BlankSlide(name, self.namespaces, self.theme)
        self.slides.append(slide_tag)
        self.current_slide_count += 1
        return slide_tag

    def add_content(self, document: mistletoe.Document, slide_name: str = None):
        if not document.children:
            raise ValueError("Document has no children")

        slide = self.new_slide(slide_name, slide_type=TitleAndContentSlide)

        for idx, child in enumerate(document.children):
            if idx == 0 and isinstance(child, mistletoe.block_token.Heading):

                title = child.children[0].content

                output_p = Tag(
                    "text:p",
                    self.namespaces,
                )
                span = Tag(
                    "text:span",
                    self.namespaces,
                )
                span.text = title
                output_p.append(span)
                slide.title_text_box.append(output_p)
            else:
                if isinstance(child, mistletoe.block_token.Paragraph):
                    p = self.process_markdown_paragraph(child, CONTENT_PARAGRAPH_STYLE_NAME)
                    slide.content_text_box.append(p)

                elif isinstance(child, mistletoe.block_token.List):
                    list_tag = Tag(
                        "text:list",
                        self.namespaces,
                        {
                            "text:style-name": "list",
                        },
                    )
                    for list_item in child.children:
                        list_item_tag = Tag(
                            "text:list-item",
                            self.namespaces,
                        )

                        if isinstance(list_item.children[0], mistletoe.block_token.Paragraph):
                            p = self.process_markdown_paragraph(
                                list_item.children[0], CONTENT_LIST_PARAGRAPH_STYLE_NAME
                            )
                            list_item_tag.append(p)
                        else:
                            print(f"Skipping {list_item.__class__.__name__}")
                        list_tag.append(list_item_tag)
                    slide.content_text_box.append(list_tag)
                else:
                    print(f"Skipping {child.__class__.__name__}")

                # Add a new paragraph after the last element if it's not the end of content
                if idx != len(document.children) - 1:
                    output_p = Tag(
                        "text:p",
                        self.namespaces,
                    )
                    slide.content_text_box.append(output_p)

    def process_markdown_paragraph(self, child, paragraph_style_name):
        p = Tag(
            "text:p",
            self.namespaces,
            {
                "text:style-name": paragraph_style_name,
            },
        )
        for span in child.children:

            attributes = {}

            if not isinstance(span, mistletoe.span_token.RawText):
                attributes["text:style-name"] = f"span__{span.__class__.__name__}".lower()

            span_tag = Tag(
                "text:span",
                self.namespaces,
                attributes,
            )
            span_tag.text = get_raw_text(span)
            p.append(span_tag)
        return p

    def add_source_code(self, code: CodeSlideSource, slide_name: str = None):
        for highlight in code.highlights:
            new_slide = self.new_slide(slide_name)
            for line_no, line in enumerate(code.lines, 1):
                p = Tag(
                    "text:p",
                    self.namespaces,
                    {
                        "text:style-name": (
                            CODE_PARAGRAPH_STYLE_NAME
                            if line_no not in highlight
                            else CODE_HIGHLIGHT_PARAGRAPH_STYLE_NAME
                        ),
                        "text:class-names": "",
                        "text:cond-style-name": "",
                    },
                )
                for token, value in line:
                    token_style_name = f"span__{self.theme.pygments_style}__{token}".replace(".", "_").lower()
                    if token_style_name not in self.theme.token_styles:
                        for tt in reversed(token.split()):
                            token_style_name = f"span__{self.theme.pygments_style}__{tt}".replace(".", "_").lower()
                            if token_style_name in self.theme.token_styles:
                                break

                    span = Tag(
                        "text:span",
                        self.namespaces,
                        {"text:style-name": token_style_name, "text:class-names": ""},
                    )
                    if value.isspace():
                        space_tag = Tag("text:s", self.namespaces, {"text:c": str(len(value))})
                        span.append(space_tag)
                    else:
                        span.text = value
                    p.append(span)
                new_slide.content_text_box.append(p)

            for line_no, line in enumerate(code.outputs, 1):
                output_p = Tag(
                    "text:p",
                    self.namespaces,
                    {
                        "text:style-name": CODE_PARAGRAPH_STYLE_NAME,
                    },
                )
                span = Tag(
                    "text:span",
                    self.namespaces,
                )
                span.text = line
                output_p.append(span)
                new_slide.output_text_box.append(output_p)

            output_p = Tag(
                "text:p",
                self.namespaces,
            )
            span = Tag(
                "text:span",
                self.namespaces,
            )
            span.text = code.title
            output_p.append(span)
            new_slide.title_text_box.append(output_p)

    def write(self, path: Path, prettify: bool = False):

        source = importlib.resources.files("presentpy") / "templates/odp/"

        exploded_presentation_path = path.parent / f"{path.stem}_odp"

        shutil.copytree(source, exploded_presentation_path, dirs_exist_ok=True)

        content_path = f"{exploded_presentation_path}/content.xml"
        content_xml = Content(content_path, self.namespaces, self.theme)

        styles_path = f"{exploded_presentation_path}/styles.xml"
        styles_xml = Styles(styles_path, self.namespaces, self.theme)

        for style in self.theme.styles:
            content_xml.automatic_styles.append(style.to_element())

        for slide in self.slides:
            content_xml.presentation.append(slide.to_element())

        content_xml.write(prettify=prettify)
        styles_xml.write(prettify=True)

        pptx_file = path.parent / f"{path.stem}.odp"

        with zipfile.ZipFile(pptx_file, "w") as zip_ref:
            for file in exploded_presentation_path.glob("**/*"):
                zip_ref.write(file, file.relative_to(exploded_presentation_path))


def get_raw_text(token):
    if isinstance(token, mistletoe.span_token.RawText):
        return token.content
    else:
        return get_raw_text(token.children[0])
