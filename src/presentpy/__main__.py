from pathlib import Path

import click

from presentpy.config import get_configuration
from presentpy.processors import NotebookProcessor, ScriptProcessor
from presentpy.writers.pptx_writer import PptxWriter

CARRIAGE_RETURN = "\x0A"


@click.group()
def cli():
    pass


@cli.command("nb")
@click.argument("notebook", type=click.Path(exists=True))
@click.option("--theme", default="light")
def process_notebook(notebook, theme):
    notebook_path = Path(notebook)
    output_file_name = Path(notebook_path.stem + ".pptx")

    pptx_writer = PptxWriter(configuration=get_configuration(), theme=theme)
    notebook_processor = NotebookProcessor(notebook_path, pptx_writer)
    notebook_processor.process()

    pptx_writer.save(output_file_name)

    print(f"Running {notebook_path}...")


@cli.command("py")
@click.argument("script", type=click.Path(exists=True))
@click.option("--theme", default="light")
def process_script(script, theme):
    script_path = Path(script)
    output_file_name = Path(script_path.stem + ".pptx")

    pptx_writer = PptxWriter(configuration=get_configuration(), theme=theme)
    script_processor = ScriptProcessor(script_path, pptx_writer)
    script_processor.process()

    pptx_writer.save(output_file_name)

    print(f"Running {script_path}...")


if __name__ == "__main__":
    cli()
