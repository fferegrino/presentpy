from pathlib import Path

import nbformat

from presentpy.code_slide_source import CodeSlideSource


class NotebookProcessor:
    def __init__(self, notebook_path: Path, writer):
        self.notebook_path = notebook_path
        self.notebook = nbformat.read(self.notebook_path, as_version=4)
        self.writer = writer

    def process(self):
        for cell in self.notebook.cells:
            if cell.cell_type == "code":
                code_slide_source = CodeSlideSource.from_source_code(cell.source)
                self.writer.write(code_slide_source)
