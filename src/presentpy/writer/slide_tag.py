from presentpy.constants import *
from presentpy.namespaces import Namespaces
from presentpy.writer.tag import Tag
from presentpy.writer.theme import Theme


class SlideTag(Tag):
    def __init__(self, name, namespaces: Namespaces, theme: Theme):
        super().__init__(
            "draw:page",
            namespaces,
            {"draw:name": name, "draw:style-name": DRAWING_PAGE_STYLE_NAME, "draw:id": name},
        )
        self.name = name
        self.theme = theme

    def add_text_box(self, container_style, x, y, w, h, text_box_style=None):
        frame = Tag(
            "draw:frame",
            self.namespaces,
            {
                "draw:style-name": container_style,
                "svg:x": f"{x:.2}in",
                "svg:y": f"{y:.2}in",
                "svg:width": f"{w:.2f}in",
                "svg:height": f"{h:.2f}in",
            },
        )

        text_box_style_def = {}
        if text_box_style:
            text_box_style_def = {"draw:style-name": text_box_style}
        text_box = Tag("draw:text-box", self.namespaces, text_box_style_def)

        frame.append(text_box)
        self.append(frame)

        return text_box


class TitleSlide(SlideTag):
    def __init__(self, name, namespaces: Namespaces, theme: Theme):
        super().__init__(
            name,
            namespaces,
            theme,
        )
        self.name = name
        self.theme = theme

        x = 0.9
        title_y = 0.4
        w = self.theme.width - (2 * x)
        title_h = 1

        self.title_text_box = super().add_text_box("masterTitle", x, title_y, w, title_h)

        content_y = title_y + title_h + 0.2
        content_h = self.theme.height - content_y - 0.4

        self.content_text_box = super().add_text_box(CODE_FRAME_STYLE_NAME, x, content_y, w, content_h)


class TitleContentAndOutputSlide(SlideTag):
    def __init__(self, name, namespaces: Namespaces, theme: Theme):
        super().__init__(
            name,
            namespaces,
            theme,
        )
        self.name = name
        self.theme = theme

        x = 0.9
        title_y = 0.4
        w = self.theme.width - (2 * x)
        title_h = 1

        self.title_text_box = super().add_text_box(MASTER_TITLE_STYLE_NAME, x, title_y, w, title_h)

        content_y = title_y + title_h + 0.2
        content_h = self.theme.height - content_y - 0.4
        content_h = content_h / 2 - 0.2

        self.content_text_box = super().add_text_box(CODE_FRAME_STYLE_NAME, x, content_y, w, content_h)
        self.output_text_box = super().add_text_box(CODE_FRAME_STYLE_NAME, x, content_y + content_h + 0.2, w, content_h)
