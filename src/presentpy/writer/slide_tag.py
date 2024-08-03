from presentpy.constants import *
from presentpy.namespaces import Namespaces
from presentpy.writer.tag import Tag
from presentpy.writer.theme import Theme


class SlideTag(Tag):

    def __init__(self, name, namespaces: Namespaces, theme: Theme):
        super().__init__(
            "draw:page",
            namespaces,
            {
                "draw:name": name,
                "draw:style-name": DRAWING_PAGE_STYLE_NAME,
                "draw:id": name,
                "draw:master-page-name": "Master1-Master",
            },
        )
        self.name = name
        self.theme = theme

        self.text_boxes = {}
        self.master_page_items = []

    def add_text_box(self, identifier, container_style, x, y, w, h, text_box_style=None, presentation_class=None):
        frame_attributes = {
            "draw:style-name": container_style,
            "svg:x": f"{x:.2}in",
            "svg:y": f"{y:.2}in",
            "svg:width": f"{w:.2f}in",
            "svg:height": f"{h:.2f}in",
        }

        if presentation_class:
            frame_attributes["presentation:class"] = presentation_class

        frame = Tag("draw:frame", self.namespaces, frame_attributes)

        text_box_style_def = {}
        if text_box_style:
            text_box_style_def = {"draw:style-name": text_box_style}
        text_box = Tag("draw:text-box", self.namespaces, text_box_style_def)

        frame.append(text_box)
        self.append(frame)

        self.text_boxes[identifier] = text_box

        return text_box

    def __getattr__(self, item):
        if item in self.text_boxes:
            return self.text_boxes[item]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def to_master_page(self, prefix, layout, style):
        master_page = Tag(
            "style:master-page",
            self.namespaces,
            {
                "style:name": f"{prefix}-{self.__class__.__name__}",
                "style:page-layout-name": layout,
                "draw:style-name": style,
            },
        )

        for child in self.children:
            master_page.append(child)

        return master_page


class BlankSlide(SlideTag):
    """
    ┌────────────────────────────────────────────────┐
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    └────────────────────────────────────────────────┘
    """

    def __init__(self, name, namespaces: Namespaces, theme: Theme):
        super().__init__(
            name,
            namespaces,
            theme,
        )
        self.name = name
        self.theme = theme


class TitleSlide(SlideTag):
    """
    ┌────────────────────────────────────────────────┐
    │ ┌────────────────────────────────────────────┐ │
    │ │ Title                                      │ │
    │ └────────────────────────────────────────────┘ │
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    │                                                │
    └────────────────────────────────────────────────┘
    """

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

        super().add_text_box(
            "title_text_box", MASTER_TITLE_STYLE_NAME, x, title_y, w, title_h, presentation_class="title"
        )


class TitleAndContentSlide(SlideTag):
    """
    ┌────────────────────────────────────────────────┐
    │ ┌────────────────────────────────────────────┐ │
    │ │ Title                                      │ │
    │ └────────────────────────────────────────────┘ │
    │ ┌────────────────────────────────────────────┐ │
    │ │ Content                                    │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ └────────────────────────────────────────────┘ │
    └────────────────────────────────────────────────┘
    """

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

        super().add_text_box(
            "title_text_box", MASTER_TITLE_STYLE_NAME, x, title_y, w, title_h, presentation_class="title"
        )

        content_y = title_y + title_h + 0.2
        content_h = self.theme.height - content_y - 0.4

        super().add_text_box(
            "content_text_box", MASTER_CONTENT_STYLE_NAME, x, content_y, w, content_h, presentation_class="object"
        )


class TitleAndCodeSlide(SlideTag):
    """
    ┌────────────────────────────────────────────────┐
    │ ┌────────────────────────────────────────────┐ │
    │ │ Title                                      │ │
    │ └────────────────────────────────────────────┘ │
    │ ┌────────────────────────────────────────────┐ │
    │ │ Code                                       │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ └────────────────────────────────────────────┘ │
    └────────────────────────────────────────────────┘
    """

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

        super().add_text_box(
            "title_text_box", MASTER_TITLE_STYLE_NAME, x, title_y, w, title_h, presentation_class="title"
        )

        content_y = title_y + title_h + 0.2
        content_h = self.theme.height - content_y - 0.4

        super().add_text_box(
            "content_text_box", CODE_FRAME_STYLE_NAME, x, content_y, w, content_h, presentation_class="object"
        )


class TitleCodeAndOutputSlide(SlideTag):
    """
    ┌────────────────────────────────────────────────┐
    │ ┌────────────────────────────────────────────┐ │
    │ │ Title                                      │ │
    │ └────────────────────────────────────────────┘ │
    │ ┌────────────────────────────────────────────┐ │
    │ │ Content                                    │ │
    │ │                                            │ │
    │ └────────────────────────────────────────────┘ │
    │ ┌────────────────────────────────────────────┐ │
    │ │ Outputs                                    │ │
    │ │                                            │ │
    │ └────────────────────────────────────────────┘ │
    └────────────────────────────────────────────────┘
    """

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

        super().add_text_box(
            "title_text_box", MASTER_TITLE_STYLE_NAME, x, title_y, w, title_h, presentation_class="title"
        )

        content_y = title_y + title_h + 0.2
        content_h = self.theme.height - content_y - 0.4
        content_h = content_h / 2 - 0.2

        super().add_text_box(
            "content_text_box", CODE_FRAME_STYLE_NAME, x, content_y, w, content_h, presentation_class="object"
        )
        super().add_text_box(
            "output_text_box",
            OUTPUT_FRAME_STYLE_NAME,
            x,
            content_y + content_h + 0.2,
            w,
            content_h,
            presentation_class="object",
        )
