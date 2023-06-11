from pathlib import Path

import click
import nbformat

from presentpy.code_slide_source import CodeSlideSource


class NotebookProcessor:
    def __init__(self, notebook_path: Path, output_device):
        self.notebook_path = notebook_path
        self.notebook = nbformat.read(self.notebook_path, as_version=4)
        self.output_device = output_device

    def process(self):
        for cell in self.notebook.cells:
            if cell.cell_type == "code":
                code_slide_source = CodeSlideSource.from_source_code(cell.source)
                self.output_device.write(code_slide_source)


@click.command()
@click.argument('notebook', type=click.Path(exists=True))
def run_presentpy(notebook):

    class PrintOutputDevice:
        def write(self, code_slide_source: CodeSlideSource):
            print(code_slide_source)

    notebook_path = Path(notebook)
    notebook_processor = NotebookProcessor(notebook_path, PrintOutputDevice())
    notebook_processor.process()


    print(f'Running {notebook_path}...')

if __name__ == '__main__':
    run_presentpy()
