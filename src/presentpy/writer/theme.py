from pygments.styles import get_all_styles, get_style_by_name
from pygments.token import Comment, Literal, String, Token

from presentpy.namespaces import Namespaces
from presentpy.writer.tag import Tag


def convert_color(color: str):
    if len(color) == 4:
        color = f"#{color[1] * 2}{color[2] * 2}{color[3] * 2}"
    return color


class Theme:
    DRAWING_PAGE_STYLE_NAME = "dp1"
    CODE_PARAGRAPH_STYLE_NAME = "c20"
    CODE_HIGHLIGHT_PARAGRAPH_STYLE_NAME = "hl20"
    CODE_FRAME_STYLE_NAME = "f30"

    def __init__(self, pygments_style: str, namespaces: Namespaces, height=7.5, width=13.33, font_size_ratio=0.5 / 36):
        self.styles = []
        self.namespaces = namespaces
        self.pygments_style = pygments_style
        self.width = width
        self.height = height
        self.token_styles = set()
        self.font_size_ratio = font_size_ratio

        self.style = get_style_by_name(self.pygments_style)

        drawing_page_style = self.create_drawing_page_style(self.style)
        self.styles.append(drawing_page_style)

        paragraph_style = self.create_paragraph_style()
        self.styles.append(paragraph_style)

        paragraph_highlight_style = self.create_paragraph_style(highlight=True)
        self.styles.append(paragraph_highlight_style)

        graphic_style = self.create_graphic_frame_style()
        self.styles.append(graphic_style)

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
        return f"{pts * self.font_size_ratio:.2f}in"

    def create_drawing_page_style(self, style):
        drawing_page_style = Tag(
            "style:style",
            self.namespaces,
            {
                "style:family": "drawing-page",
                "style:name": Theme.DRAWING_PAGE_STYLE_NAME,
            },
        )
        drawing_page_properties = Tag(
            "style:drawing-page-properties",
            self.namespaces,
            {
                "draw:fill": "solid",
                "draw:fill-color": convert_color(style.background_color),
                "draw:opacity": "100%",
                "presentation:visibility": "visible",
                "draw:background-size": "border",
                "presentation:background-objects-visible": "true",
                "presentation:background-visible": "false",
                "presentation:display-header": "false",
                "presentation:display-footer": "false",
                "presentation:display-page-number": "false",
                "presentation:display-date-time": "false",
            },
        )
        drawing_page_style.append(drawing_page_properties)
        return drawing_page_style

    def create_graphic_frame_style(self):
        frame_style = Tag(
            "style:style",
            self.namespaces,
            {
                "style:family": "graphic",
                "style:name": Theme.CODE_FRAME_STYLE_NAME,
            },
        )

        paragraph_properties = Tag(
            "style:paragraph-properties",
            self.namespaces,
            {"style:font-independent-line-spacing": "true", "style:writing-mode": "lr-tb"},
        )

        frame_style.append(paragraph_properties)
        return frame_style

    def create_paragraph_style(self, highlight=False):
        paragraph_style = Tag(
            "style:style",
            self.namespaces,
            {
                "style:family": "paragraph",
                "style:name": (
                    Theme.CODE_PARAGRAPH_STYLE_NAME if not highlight else Theme.CODE_HIGHLIGHT_PARAGRAPH_STYLE_NAME
                ),
            },
        )
        paragraph_properties = Tag(
            "style:paragraph-properties",
            self.namespaces,
            {
                "fo:line-height": "100%",
                "fo:text-align": "left",
                "style:tab-stop-distance": "1in",
                "fo:margin-left": "0in",
                "fo:margin-right": "0in",
                "fo:text-indent": "0in",
                "fo:margin-top": "0in",
                "fo:margin-bottom": "0in",
                "style:punctuation-wrap": "hanging",
                "style:vertical-align": "auto",
                "style:writing-mode": "lr-tb",
            },
        )
        tab_stops = Tag("style:tab-stops", self.namespaces)
        paragraph_properties.append(tab_stops)

        text_properties_attributes = {
            "fo:font-variant": "normal",
            "fo:text-transform": "none",
            "fo:color": "#000000",
            "style:text-line-through-type": "none",
            "style:text-line-through-style": "none",
            "style:text-line-through-width": "auto",
            "style:text-line-through-color": "font-color",
            "style:text-position": "0% 100%",
            "fo:font-size": "0.25in",
            "style:font-size-asian": "0.25in",
            "style:font-size-complex": "0.25in",
            "fo:letter-spacing": "0in",
            "fo:font-style": "normal",
            "style:font-style-asian": "normal",
            "style:font-style-complex": "normal",
            "style:text-underline-type": "none",
            "style:text-underline-style": "none",
            "style:text-underline-width": "auto",
            "style:text-underline-color": "font-color",
            "fo:font-weight": "normal",
            "style:font-weight-asian": "normal",
            "style:font-weight-complex": "normal",
            "style:text-underline-mode": "continuous",
            "style:letter-kerning": "false",
            "fo:font-family": "Courier New",
            "style:font-family-complex": "Courier New",
        }

        if highlight:
            text_properties_attributes["fo:background-color"] = self.highlight_color
            text_properties_attributes["fo:font-weight"] = "bold"

        text_properties = Tag("style:text-properties", self.namespaces, text_properties_attributes)
        paragraph_style.append(paragraph_properties)
        paragraph_style.append(text_properties)
        return paragraph_style
