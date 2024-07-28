import importlib.resources
import shutil
import zipfile
from pathlib import Path
from typing import List

from lxml import etree

from presentpy.code_slide_source import CodeSlideSource
from presentpy.namespaces import Namespaces
from presentpy.templates import Content, Styles
from presentpy.writer.slide_tag import SlideTag
from presentpy.writer.tag import Tag
from presentpy.writer.theme import Theme


class Presentation:
    def __init__(self, theme: Theme, namespaces: Namespaces):
        self.theme = theme
        self.namespaces = namespaces
        self.styles: List[Tag] = []
        self.slides: List[SlideTag] = []

    def new_slide(self, name):
        slide_tag = SlideTag(name, self.namespaces, self.theme)
        self.slides.append(slide_tag)
        return slide_tag

    def add_source_code(self, code: CodeSlideSource):
        for idx, highlight in enumerate(code.highlights):
            new_slide = self.new_slide(f"code{idx}")
            for line_no, line in enumerate(code.lines, 1):
                p = Tag(
                    "text:p",
                    self.namespaces,
                    {
                        "text:style-name": (
                            Theme.CODE_PARAGRAPH_STYLE_NAME
                            if line_no not in highlight
                            else Theme.CODE_HIGHLIGHT_PARAGRAPH_STYLE_NAME
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
                new_slide.text_box.append(p)

    def write(self, path: str, prettify: bool = False):
        path = Path(path)
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

        pptx_file = f"{path}.odp"

        with zipfile.ZipFile(pptx_file, "w") as zip_ref:
            for file in exploded_presentation_path.glob("**/*"):
                zip_ref.write(file, file.relative_to(exploded_presentation_path))
