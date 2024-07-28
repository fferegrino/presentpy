from typing import Any, List, Tuple

from presentpy.code_slide_source import CodeSlideSource
from presentpy.namespaces import Namespaces
from presentpy.writer.tag import Tag
from presentpy.writer.theme import Theme


class SlideTag(Tag):
    def __init__(self, name, namespaces: Namespaces, theme: Theme):
        super().__init__(
            "draw:page",
            namespaces,
            {"draw:name": name, "draw:style-name": Theme.DRAWING_PAGE_STYLE_NAME, "draw:id": name},
        )
        self.name = name
        self.theme = theme

        x = 1.0
        y = 1.0
        w = self.theme.width - 2
        h = self.theme.height - 2

        frame = Tag(
            "draw:frame",
            self.namespaces,
            {
                "draw:style-name": Theme.CODE_FRAME_STYLE_NAME,
                "svg:x": f"{x:.2}in",
                "svg:y": f"{y:.2}in",
                "svg:width": f"{w:.2f}in",
                "svg:height": f"{h:.2f}in",
            },
        )
        self.text_box = Tag("draw:text-box", self.namespaces, {})

        frame.append(self.text_box)
        self.append(frame)

    def add_source_code(self, code: CodeSlideSource):

        for highlight in code.highlights:
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
                self.text_box.append(p)
