from pygments.styles import get_all_styles, get_style_by_name
from pygments.token import Comment, Literal, String, Token

from presentpy.constants import *
from presentpy.namespaces import Namespaces
from presentpy.writer.tag import Tag


def convert_color(color: str):
    if len(color) == 4:
        color = f"#{color[1] * 2}{color[2] * 2}{color[3] * 2}"
    return color


class Theme:

    def __init__(self, pygments_style: str, namespaces: Namespaces, height=7.5, width=13.33, font_size_ratio=0.5 / 36):
        self.styles = []
        self.namespaces = namespaces
        self.pygments_style = pygments_style
        self.width = width
        self.height = height
        self.token_styles = set()
        self.font_size_ratio = font_size_ratio

        self.style = get_style_by_name(self.pygments_style)

        for token, str_style in self.style.styles.items():
            style_parts = set(str_style.split())

            if not style_parts:
                continue

            color = None
            for part in style_parts:
                if part.startswith("#"):
                    color = convert_color(part)
                    break

            token_normalised_name = str(token).replace(".", "_")
            inner_style_name = f"span__{self.pygments_style}__{token_normalised_name}".lower()
            text_style = Tag(
                "style:style",
                self.namespaces,
                {
                    "style:family": "text",
                    "style:name": inner_style_name,
                },
            )

            style_attributes = {}

            if color:
                style_attributes["fo:color"] = color

            if "bold" in style_parts:
                style_attributes["fo:font-weight"] = "bold"

            if "italic" in style_parts:
                style_attributes["fo:font-style"] = "italic"

            if "underline" in style_parts:
                style_attributes["style:text-underline-style"] = "solid"

            text_properties = Tag(
                "style:text-properties",
                self.namespaces,
                style_attributes,
            )

            text_style.append(text_properties)
            self.token_styles.add(inner_style_name)
            self.styles.append(text_style)

    @property
    def background_color(self):
        return convert_color(self.style.background_color)

    @property
    def title_color(self):
        selected_token_style = self._find_style_for_token(String, Literal)
        style_parts = set(selected_token_style.split())
        for part in style_parts:
            if part.startswith("#"):
                return convert_color(part)
        return "#ffffff"

    @property
    def highlight_color(self):
        return convert_color(self.style.highlight_color)

    @property
    def content_color(self):
        selected_token_style = self._find_style_for_token(Comment, String, Literal)
        style_parts = set(selected_token_style.split())
        for part in style_parts:
            if part.startswith("#"):
                return convert_color(part)
        return "#ffffff"

    def _find_style_for_token(self, *token):
        for t in token:
            if t in self.style.styles:
                return self.style.styles[t]
        else:
            return self.style.styles[Token]

    def font_size(self, pts):
        return f"{pts}pt"

    @property
    def content_font_size(self):
        return self.font_size(28)

    @property
    def title_font_size(self):
        return self.font_size(44)
