from colour import Color
from pygments.styles import get_style_by_name
from pygments.token import Comment, Literal, String, Token

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

        self._table_row_odd_background_color = Color(self.style.background_color)
        max_luminance = min(self._table_row_odd_background_color.luminance + 0.05, 1)
        self._table_row_odd_background_color.set_luminance(max_luminance)

        self._table_row_even_background_color = Color(self.style.background_color)
        min_luminance = max(self._table_row_even_background_color.luminance - 0.05, 0)
        self._table_row_even_background_color.set_luminance(min_luminance)

        fallback_color = Color(self.style.background_color)
        fallback_color_luma = 0.2126 * fallback_color.red + 0.7152 * fallback_color.green + 0.0722 * fallback_color.blue
        if fallback_color_luma > 128:
            self._fallback_color = Color(self.style.background_color)
            self._fallback_color.set_luminance(max(fallback_color.get_luminance() - 0.5, 0))
        else:
            self._fallback_color = Color(self.style.background_color)
            self._fallback_color.set_luminance(min(fallback_color.get_luminance() + 0.5, 1))

    @property
    def table_row_odd_background_color(self):
        return convert_color(self._table_row_odd_background_color.hex)

    @property
    def table_row_even_background_color(self):
        return convert_color(self._table_row_even_background_color.hex)

    @property
    def background_color(self):
        return convert_color(self.style.background_color)

    @property
    def title_color(self):
        selected_token_style = self._find_style_for_token(String, Literal, Comment)
        style_parts = set(selected_token_style.split())
        for part in style_parts:
            if part.startswith("#"):
                return convert_color(part)
        return str(self._fallback_color)

    @property
    def highlight_color(self):
        return convert_color(self.style.highlight_color)

    @property
    def table_border_width(self):
        return f"{0.03}in"

    @property
    def content_color(self):
        selected_token_style = self._find_style_for_token(Comment, String, Literal)
        style_parts = set(selected_token_style.split())
        for part in style_parts:
            if part.startswith("#"):
                return convert_color(part)
        return str(self._fallback_color)

    @property
    def content_color_alt(self):
        selected_token_style = self._find_style_for_token()
        style_parts = set(selected_token_style.split())
        for part in style_parts:
            if part.startswith("#"):
                return convert_color(part)
        return str(self._fallback_color)

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
