from pathlib import Path

from presentpy.constants import *
from presentpy.namespaces import Namespaces
from presentpy.templates.xml_file import XMLFile
from presentpy.writer.tag import Tag


class Manifest(XMLFile):

    def __init__(self, path: Path, namespaces: Namespaces):
        super().__init__(path, namespaces)

        self.manifest = self.xpath("manifest:manifest")

    def add_file_entry(self, path: Path, media_type: str):

        manifest_file_entry = Tag(
            "manifest:file-entry",
            self.namespaces,
            {
                "manifest:media-type": media_type,
                "manifest:full-path": str(path),
            },
        )

        self.manifest.append(manifest_file_entry.to_element())
