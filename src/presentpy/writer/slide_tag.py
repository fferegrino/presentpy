from presentpy.constants import (
    CODE_FRAME_STYLE_NAME,
    DRAWING_PAGE_STYLE_NAME,
    MASTER_CONTENT_STYLE_NAME,
    MASTER_SLIDE_PREFIX,
    MASTER_TITLE_FRAME_STYLE_NAME,
    OUTPUT_FRAME_STYLE_NAME,
)
from presentpy.namespaces import Namespaces
from presentpy.writer.tag import Tag
from presentpy.writer.theme import Theme


class SlideTag(Tag):

    __prefix__ = MASTER_SLIDE_PREFIX
    __layout__ = ""
    __infix__ = "presentpy"

    def __init__(self, name, namespaces: Namespaces, theme: Theme):
        super().__init__(
            "draw:page",
            namespaces,
            {
                "draw:name": name,
                "draw:style-name": DRAWING_PAGE_STYLE_NAME,
                "draw:id": name,
                "draw:master-page-name": self.get_master_page_style_name(),
            },
        )
        self.name = name
        self.theme = theme

        self.frames = {}
        self.text_boxes = {}
        self.master_page_items = []

    def get_dimensions(self, frame_name):
        frame = self.frames[frame_name]
        x = frame["svg:x"]
        y = frame["svg:y"]
        w = frame["svg:width"]
        h = frame["svg:height"]

        return [float(measure[:-2]) for measure in [x, y, w, h]]

    def add_frame(self, identifier, x, y, w, h, frame_style=None, presentation_class=None):
        frame_attributes = {}

        if frame_style:
            frame_attributes["draw:style-name"] = frame_style

        frame_attributes["svg:x"] = f"{x:.2}in"
        frame_attributes["svg:y"] = f"{y:.2}in"
        frame_attributes["svg:width"] = f"{w:.2f}in"
        frame_attributes["svg:height"] = f"{h:.2f}in"

        if presentation_class:
            frame_attributes["presentation:class"] = presentation_class

        frame = Tag("draw:frame", self.namespaces, frame_attributes)
        self.frames[identifier] = frame
        self.append(frame)

        return frame

    def add_text_box(
        self, identifier, x, y, w, h, container_style_name=None, text_box_style=None, presentation_class=None
    ):

        frame = self.add_frame(
            f"{identifier}_frame", x, y, w, h, frame_style=container_style_name, presentation_class=presentation_class
        )

        text_box_style_def = {}
        if text_box_style:
            text_box_style_def = {"draw:style-name": text_box_style}
        text_box = Tag("draw:text-box", self.namespaces, text_box_style_def)

        frame.append(text_box)

        self.text_boxes[identifier] = text_box

        return text_box

    def __getattr__(self, item):
        if item in self.text_boxes:
            return self.text_boxes[item]
        if item in self.frames:
            return self.frames[item]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def get_master_page_style_name(self):
        return f"{self.__prefix__}-{self.__layout__}-{self.__infix__}-{self.__class__.__name__}"

    def to_master_page(self, layout, style):
        master_page = Tag(
            "style:master-page",
            self.namespaces,
            {
                "style:name": self.get_master_page_style_name(),
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

    __layout__ = "Layout1"

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

    __layout__ = "Layout2"

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
            "title_text_box",
            x,
            title_y,
            w,
            title_h,
            container_style_name=MASTER_TITLE_FRAME_STYLE_NAME,
            presentation_class="title",
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

    __layout__ = "Layout3"

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
            "title_text_box",
            x,
            title_y,
            w,
            title_h,
            container_style_name=MASTER_TITLE_FRAME_STYLE_NAME,
            presentation_class="title",
        )

        content_y = title_y + title_h + 0.2
        content_h = self.theme.height - content_y - 0.4

        super().add_text_box(
            "content_text_box",
            x,
            content_y,
            w,
            content_h,
            container_style_name=MASTER_CONTENT_STYLE_NAME,
            presentation_class="object",
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

    __layout__ = "Layout4"

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
            "title_text_box",
            x,
            title_y,
            w,
            title_h,
            container_style_name=MASTER_TITLE_FRAME_STYLE_NAME,
            presentation_class="title",
        )

        content_y = title_y + title_h + 0.2
        content_h = self.theme.height - content_y - 0.4

        super().add_text_box(
            "content_text_box",
            x,
            content_y,
            w,
            content_h,
            container_style_name=CODE_FRAME_STYLE_NAME,
            presentation_class="object",
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

    __layout__ = "Layout5"

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
            "title_text_box",
            x,
            title_y,
            w,
            title_h,
            container_style_name=MASTER_TITLE_FRAME_STYLE_NAME,
            presentation_class="title",
        )

        content_y = title_y + title_h + 0.2
        content_h = self.theme.height - content_y - 0.4
        content_h = content_h / 2 - 0.2

        super().add_text_box(
            "content_text_box",
            x,
            content_y,
            w,
            content_h,
            container_style_name=CODE_FRAME_STYLE_NAME,
            presentation_class="object",
        )
        super().add_text_box(
            "output_text_box",
            x,
            content_y + content_h + 0.2,
            w,
            content_h,
            container_style_name=OUTPUT_FRAME_STYLE_NAME,
            presentation_class="object",
        )


class TitleAndImageSlide(SlideTag):
    """
    ┌────────────────────────────────────────────────┐
    │ ┌────────────────────────────────────────────┐ │
    │ │ Title                                      │ │
    │ └────────────────────────────────────────────┘ │
    │ ┌────────────────────────────────────────────┐ │
    │ │ Image                                      │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ └────────────────────────────────────────────┘ │
    └────────────────────────────────────────────────┘
    """

    __layout__ = "Layout6"

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
            "title_text_box",
            x,
            title_y,
            w,
            title_h,
            container_style_name=MASTER_TITLE_FRAME_STYLE_NAME,
            presentation_class="title",
        )

        content_y = title_y + title_h + 0.2
        content_h = self.theme.height - content_y - 0.4

        self.content_location = (x, content_y, w, content_h)

    def add_image(self, image_path, image_width, image_height):
        x, y, w, h = self.content_location
        mid_point = (x + w / 2, y + h / 2)

        image_x = mid_point[0] - image_width / 2
        image_y = mid_point[1] - image_height / 2

        image_frame = super().add_frame(
            "object_frame",
            image_x,
            image_y,
            image_width,
            image_height,
            frame_style="image",
            presentation_class="object",
        )

        image_frame.append(
            Tag(
                "draw:image",
                self.namespaces,
                {
                    "xlink:href": image_path,
                    "xlink:type": "simple",
                    "xlink:show": "embed",
                    "xlink:actuate": "onLoad",
                },
            )
        )


class ImageSlide(SlideTag):
    """
    ┌────────────────────────────────────────────────┐
    │ ┌────────────────────────────────────────────┐ │
    │ │ Image                                      │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ └────────────────────────────────────────────┘ │
    └────────────────────────────────────────────────┘
    """

    __layout__ = "Layout7"

    def __init__(self, name, namespaces: Namespaces, theme: Theme):
        super().__init__(
            name,
            namespaces,
            theme,
        )
        self.name = name
        self.theme = theme

        x = 0.9
        y = 0.4
        w = self.theme.width - (2 * x)
        h = self.theme.height - (2 * y)

        self.content_location = (x, y, w, h)

    def add_image(self, image_path, image_width, image_height):
        x, y, w, h = self.content_location
        mid_point = (x + w / 2, y + h / 2)

        image_x = mid_point[0] - image_width / 2
        image_y = mid_point[1] - image_height / 2

        image_frame = super().add_frame(
            "object_frame",
            image_x,
            image_y,
            image_width,
            image_height,
            frame_style="image",
            presentation_class="object",
        )

        image_frame.append(
            Tag(
                "draw:image",
                self.namespaces,
                {
                    "xlink:href": image_path,
                    "xlink:type": "simple",
                    "xlink:show": "embed",
                    "xlink:actuate": "onLoad",
                },
            )
        )


class TitleAndObjectSlide(SlideTag):
    """
    ┌────────────────────────────────────────────────┐
    │ ┌────────────────────────────────────────────┐ │
    │ │ Title                                      │ │
    │ └────────────────────────────────────────────┘ │
    │ ┌────────────────────────────────────────────┐ │
    │ │ Object                                     │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ │                                            │ │
    │ └────────────────────────────────────────────┘ │
    └────────────────────────────────────────────────┘
    """

    __layout__ = "Layout8"

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
            "title_text_box",
            x,
            title_y,
            w,
            title_h,
            container_style_name=MASTER_TITLE_FRAME_STYLE_NAME,
            presentation_class="title",
        )

        content_y = title_y + title_h + 0.2
        content_h = self.theme.height - content_y - 0.4

        self.content_location = (x, content_y, w, content_h)

        self.add_frame("object_frame", x, content_y, w, content_h, frame_style="object", presentation_class="object")
