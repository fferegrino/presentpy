from pathlib import Path

import click
import mistletoe
import nbformat

from presentpy.code_slide_source import CodeSlideSource
from presentpy.namespaces import Namespaces
from presentpy.writer.presentation import Presentation
from presentpy.writer.theme import Theme

odf_namespaces = {
    "dom": "http://www.w3.org/2001/xml-events",
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    "fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
    "loext": "urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0",
    "manifest": "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0",
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "presentation": "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
    "script": "urn:oasis:names:tc:opendocument:xmlns:script:1.0",
    "smil": "urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0",
    "style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
    "svg": "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "xlink": "http://www.w3.org/1999/xlink",
}


@click.command()
@click.argument("notebook", type=click.Path(exists=True))
@click.option(
    "--output",
    default=".",
    help="Directory or file path where the output ODP file will be saved. Defaults to the current directory.",
)
@click.option(
    "--theme",
    default="default",
    help=(
        "Pygments style to be applied to the presentation."
        "Defaults to 'default'. See https://pygments.org/docs/styles/ for available styles."
    ),
)
@click.option(
    "--prettify",
    is_flag=True,
    default=False,
    help="Prettify the output ODP file. NOT RECOMMENDED unless you are debugging the output files.",
    hidden=True,
)
@click.option(
    "--keep-intermediate",
    is_flag=True,
    default=False,
    help="Keep the intermediate files. NOT RECOMMENDED unless you are debugging the output files.",
    hidden=True,
)
@click.option(
    "--outputs",
    is_flag=True,
    default=False,
    help="Include code cell outputs in the presentation.",
)
def process(notebook, output, theme, prettify, keep_intermediate, outputs):
    """
    A CLI tool to convert Jupyter Notebooks to slides.
    """
    namespaces = Namespaces(odf_namespaces)
    theme = Theme(theme, namespaces)
    presentation = Presentation(theme, namespaces)
    notebook = Path(notebook)
    output = Path(output) / f"{notebook.stem}.odp" if Path(output).is_dir() else Path(output)

    if notebook.suffix == ".ipynb":
        with open(notebook) as f:
            nb = nbformat.read(f, as_version=4)

        for cell in nb.cells:
            if cell.cell_type == "code":
                code_slide = CodeSlideSource.from_code_cell(cell)
                presentation.add_source_code(code_slide, with_output=outputs)
            elif cell.cell_type == "markdown":
                document = mistletoe.Document(cell.source)
                presentation.add_content(document)

    elif notebook.suffix == ".py":
        with open(notebook) as f:
            source = f.read()
            code_slide = CodeSlideSource.from_source_code(source)
            presentation.add_source_code(code_slide)

    presentation.write(output, prettify=prettify, keep_intermediate=keep_intermediate)
