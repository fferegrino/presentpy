from pathlib import Path

import click

from presentpy.notebook_processor import NotebookProcessor
from presentpy.writers.pptx_writer import PptxWriter

CARRIAGE_RETURN = "\x0A"


@click.command()
@click.argument("notebook", type=click.Path(exists=True))
@click.option("--theme", default="light")
def run_presentpy(notebook, theme):
    notebook_path = Path(notebook)
    output_file_name = Path(notebook_path.stem + ".pptx")

    pptx_writer = PptxWriter(theme=theme)
    notebook_processor = NotebookProcessor(notebook_path, pptx_writer)
    notebook_processor.process()

    pptx_writer.save(output_file_name)

    print(f"Running {notebook_path}...")


if __name__ == "__main__":
    run_presentpy()
