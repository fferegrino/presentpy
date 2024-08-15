import base64
import importlib.resources
import os
import shutil
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path
from typing import List

import mistletoe
from bs4 import BeautifulSoup
from PIL import Image

from presentpy.code_slide_source import CodeSlideSource
from presentpy.constants import *
from presentpy.namespaces import Namespaces
from presentpy.templates import Content, Styles
from presentpy.templates.manifest import Manifest
from presentpy.writer.slide_tag import (
    BlankSlide,
    ImageSlide,
    SlideTag,
    TitleAndCodeSlide,
    TitleAndContentSlide,
    TitleAndImageSlide,
    TitleAndObjectSlide,
    TitleCodeAndOutputSlide,
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
        self.current_image_count = 0
        self.current_table_count = 0
        self._temp_dir = tempfile.mkdtemp()
        self.file_entries = []
        os.makedirs(f"{self._temp_dir}/media", exist_ok=True)

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

    def _add_title(self, title: str, slide: SlideTag):
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

    def add_source_code(self, code: CodeSlideSource, slide_name: str = None, with_output=False):
        if code.output.image_png:
            self.current_image_count += 1
            media_path = f"media/image{self.current_image_count}.png"
            image_path = f"{self._temp_dir}/{media_path}"
            self.file_entries.append((media_path, "image/png"))
            image_object = Image.open(BytesIO(base64.decodebytes(bytes(code.output.image_png, "utf-8"))))
            image_object.save(image_path)

            width, height = image_object.size
            dpi_x, dpi_y = image_object.info["dpi"]

            width_in_inches = width / dpi_x
            height_in_inches = height / dpi_y

            new_slide = self.new_slide(slide_name, slide_type=ImageSlide if not code.title else TitleAndImageSlide)
            new_slide.add_image(media_path, width_in_inches, height_in_inches)

            if code.title:
                self._add_title(code.title, new_slide)

        elif code.output.text_html:

            new_slide = self.new_slide(slide_name, slide_type=TitleAndObjectSlide)
            soup = BeautifulSoup(code.output.text_html, "lxml")

            table_attrs = {
                "table:use-banding-columns-styles": "false",
                "table:use-banding-rows-styles": "true",
                "table:use-first-column-styles": "false",
                "table:use-first-row-styles": "true",
                "table:use-last-column-styles": "false",
                "table:use-last-row-styles": "false",
            }
            table_table = soup.find("table", class_="dataframe")
            rows = table_table.find_all("tr")
            column_count = len(rows[0].find_all("th")) + len(rows[0].find_all("td"))

            self.current_table_count += 1

            table_name = f"table{self.current_table_count}"

            [*_, content_width, content_height] = new_slide.get_dimensions("object_frame")

            cell_width = content_width / column_count
            cell_height = content_height / len(rows)

            template_name = f"{table_name}-template"
            table_attrs["table:template-name"] = template_name

            table_template = Tag("table:table-template", self.namespaces, {"table:name": template_name})
            table_template.append(
                Tag("table:first-row", self.namespaces, {"table:style-name": f"{table_name}-first-row"})
            )
            self.styles.append(table_template)

            odd_row_style_name = f"{table_name}-odd-row"
            odd_row_style = Tag(
                "style:style", self.namespaces, {"style:family": "table-cell", "style:name": odd_row_style_name}
            )
            odd_row_style.append(
                Tag(
                    "style:table-cell-properties",
                    self.namespaces,
                    {
                        "fo:background-color": f"{self.theme.table_row_odd_background_color}",
                        "fo:border-bottom": f"{self.theme.table_border_width} solid {self.theme.content_color_alt}",
                        "fo:border-top": f"{self.theme.table_border_width} solid {self.theme.content_color_alt}",
                        "fo:border-left": f"{self.theme.table_border_width} solid {self.theme.content_color_alt}",
                        "fo:border-right": f"{self.theme.table_border_width} solid {self.theme.content_color_alt}",
                        "fo:border": f"{self.theme.table_border_width} solid {self.theme.content_color_alt}",
                    },
                )
            )
            odd_row_style.append(
                Tag(
                    "loext:graphic-properties",
                    self.namespaces,
                    {"draw:fill": "solid", "draw:fill-color": self.theme.table_row_odd_background_color},
                )
            )
            odd_row_style.append(
                Tag(
                    "style:paragraph-properties",
                    self.namespaces,
                    {"fo:border": f"{self.theme.table_border_width} solid {self.theme.content_color_alt}"},
                )
            )

            self.styles.append(odd_row_style)

            text_style_name = f"{table_name}-text"
            text_style = Tag("style:style", self.namespaces, {"style:family": "text", "style:name": text_style_name})
            text_style.append(
                Tag("style:text-properties", self.namespaces, {"fo:color": f"{self.theme.content_color_alt}"})
            )
            self.styles.append(text_style)

            text_heading_style_name = f"{table_name}-text-heading"
            text_heading_style = Tag(
                "style:style", self.namespaces, {"style:family": "text", "style:name": text_heading_style_name}
            )
            text_heading_style.append(
                Tag(
                    "style:text-properties",
                    self.namespaces,
                    {"fo:color": f"{self.theme.content_color_alt}", "fo:font-weight": "bold"},
                )
            )
            self.styles.append(text_heading_style)

            even_row_style_name = f"{table_name}-even-row"
            even_row_style = Tag(
                "style:style", self.namespaces, {"style:family": "table-cell", "style:name": even_row_style_name}
            )
            even_row_style.append(
                Tag(
                    "style:table-cell-properties",
                    self.namespaces,
                    {
                        "fo:background-color": f"{self.theme.table_row_even_background_color}",
                        "fo:border-bottom": f"{self.theme.table_border_width} solid {self.theme.content_color_alt}",
                        "fo:border-top": f"{self.theme.table_border_width} solid {self.theme.content_color_alt}",
                        "fo:border-left": f"{self.theme.table_border_width} solid {self.theme.content_color_alt}",
                        "fo:border-right": f"{self.theme.table_border_width} solid {self.theme.content_color_alt}",
                        "fo:border": f"{self.theme.table_border_width} solid {self.theme.content_color_alt}",
                    },
                )
            )
            even_row_style.append(
                Tag(
                    "loext:graphic-properties",
                    self.namespaces,
                    {"draw:fill": "solid", "draw:fill-color": self.theme.table_row_even_background_color},
                )
            )
            even_row_style.append(
                Tag(
                    "style:paragraph-properties",
                    self.namespaces,
                    {"fo:border": f"{self.theme.table_border_width} solid {self.theme.content_color_alt}"},
                )
            )
            self.styles.append(even_row_style)

            column_style = Tag(
                "style:style", self.namespaces, {"style:family": "table-column", "style:name": f"{table_name}-column"}
            )
            column_style.append(
                Tag("style:table-column-properties", self.namespaces, {"style:column-width": f"{cell_width}in"})
            )
            self.styles.append(column_style)

            table = Tag("table:table", self.namespaces, table_attrs)
            for _ in range(column_count):
                table.append(Tag("table:table-column", self.namespaces, {"table:style-name": f"{table_name}-column"}))
            for row_no, row in enumerate(rows):
                row_style_name = f"{table_name}-even-row" if row_no % 2 == 0 else f"{table_name}-odd-row"
                if row_no == 0:
                    text_style = text_heading_style_name
                else:
                    text_style = text_style_name
                table_row = Tag("table:table-row", self.namespaces, {"table:default-cell-style-name": row_style_name})
                for cell in row.find_all("th"):
                    cell_tag = self._table_create_cell(text_style, cell)
                    table_row.append(cell_tag)
                for cell in row.find_all("td"):
                    cell_tag = self._table_create_cell(text_style, cell)
                    table_row.append(cell_tag)
                table.append(table_row)
            new_slide.object_frame.append(table)

            if code.title:
                self._add_title(code.title, new_slide)

        else:
            self._add_code_slide(code, slide_name, with_output)

    def _table_create_cell(self, text_style, cell):
        cell_tag = Tag(
            "table:table-cell",
            self.namespaces,
        )
        text_p = Tag("text:p", self.namespaces)
        span = Tag("text:span", self.namespaces, {"text:style-name": text_style})
        span.text = cell.text
        text_p.append(span)
        cell_tag.append(text_p)
        return cell_tag

    def _add_code_slide(self, code, slide_name, with_output):
        for highlight in code.highlights:
            new_slide = self.new_slide(
                slide_name, slide_type=TitleCodeAndOutputSlide if with_output else TitleAndCodeSlide
            )

            if code.title:
                self._add_title(code.title, new_slide)

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

            if with_output:
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

    def write(self, path: Path, keep_intermediate: bool = False, prettify: bool = False):

        source = importlib.resources.files("presentpy") / "templates/odp/"

        exploded_presentation_path = path.parent / f"{path.stem}_odp"

        shutil.copytree(source, exploded_presentation_path, dirs_exist_ok=True)
        shutil.copytree(self._temp_dir, exploded_presentation_path, dirs_exist_ok=True)

        content_path = f"{exploded_presentation_path}/content.xml"
        content_xml = Content(content_path, self.namespaces, self.theme)

        styles_path = f"{exploded_presentation_path}/styles.xml"
        styles_xml = Styles(styles_path, self.namespaces, self.theme)

        manifest_path = f"{exploded_presentation_path}/META-INF/manifest.xml"
        manifest_xml = Manifest(manifest_path, self.namespaces)

        for file_path, media_type in self.file_entries:
            manifest_xml.add_file_entry(file_path, media_type)

        for style in self.theme.styles:
            content_xml.automatic_styles.append(style.to_element())

        for style in self.styles:
            content_xml.automatic_styles.append(style.to_element())

        for slide in self.slides:
            content_xml.presentation.append(slide.to_element())

        manifest_xml.write(prettify=prettify)
        content_xml.write(prettify=True)
        styles_xml.write(prettify=True)

        pptx_file = path.parent / f"{path.stem}.odp"

        with zipfile.ZipFile(pptx_file, "w") as zip_ref:
            for file in exploded_presentation_path.glob("**/*"):
                zip_ref.write(file, file.relative_to(exploded_presentation_path))

        if not keep_intermediate:
            shutil.rmtree(exploded_presentation_path)


def get_raw_text(token):
    if isinstance(token, mistletoe.span_token.RawText):
        return token.content
    else:
        return get_raw_text(token.children[0])
