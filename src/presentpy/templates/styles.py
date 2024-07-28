from pathlib import Path

from presentpy.namespaces import Namespaces
from presentpy.templates.xml_file import XMLFile
from presentpy.writer.theme import Theme


class Styles(XMLFile):

    def __init__(self, path: Path, namespaces: Namespaces, theme: Theme):
        super().__init__(path, namespaces)
        self.theme = theme

        page_layout_properties = self.xpath(
            "office:document-styles",
            "office:automatic-styles",
            "style:page-layout[@style:name='pageLayout1']",
            "style:page-layout-properties",
        )
        page_layout_properties.set(namespaces("fo:page-width"), f"{self.theme.width:.2f}in")
        page_layout_properties.set(namespaces("fo:page-height"), f"{self.theme.height:.2f}in")

        drawing_page_properties = self.xpath(
            "office:document-styles",
            "office:automatic-styles",
            "style:style[@style:name='masterStyle']",
            "style:drawing-page-properties",
        )
        drawing_page_properties.set(namespaces("draw:fill-color"), self.theme.background_color)

        master_title_style = self.xpath(
            "office:document-styles",
            "office:automatic-styles",
            "style:style[@style:name='masterTitle']",
        )
        text_properties = master_title_style.xpath("style:text-properties", namespaces=namespaces.data)[0]
        text_properties.set(namespaces("fo:color"), self.theme.title_color)
        text_properties.set(namespaces("fo:font-size"), self.theme.font_size(48))
        text_properties.set(namespaces("style:font-size-asian"), self.theme.font_size(48))
        text_properties.set(namespaces("style:font-size-complex"), self.theme.font_size(48))

        master_content_style = self.xpath(
            "office:document-styles",
            "office:automatic-styles",
            "style:style[@style:name='masterContent']",
        )
        text_properties = master_content_style.xpath("style:text-properties", namespaces=namespaces.data)[0]
        text_properties.set(namespaces("fo:color"), self.theme.content_color)
        text_properties.set(namespaces("fo:font-size"), self.theme.font_size(18))
        text_properties.set(namespaces("style:font-size-asian"), self.theme.font_size(18))
        text_properties.set(namespaces("style:font-size-complex"), self.theme.font_size(18))
