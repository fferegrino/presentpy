from pathlib import Path
from typing import Any, List, Tuple

import click
import nbformat

from presentpy.code_slide_source import CodeSlideSource
from presentpy.namespaces import Namespaces
from presentpy.writer.presentation import Presentation
from presentpy.writer.theme import Theme


@click.group()
def cli():
    pass


odf_namespaces = {
    "dom": "http://www.w3.org/2001/xml-events",
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    "fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
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


@cli.command("nb")
@click.argument("notebook", type=click.Path(exists=True))
@click.option("--output", default=".")
@click.option("--theme", default="default")
def process(notebook, output, theme):
    namespaces = Namespaces(odf_namespaces)
    theme = Theme(theme, namespaces)
    presentation = Presentation(theme, namespaces)
    output = Path(output) / Path(notebook).stem if Path(output).is_dir() else Path(output)

    with open(notebook) as f:
        nb = nbformat.read(f, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == "code":
            slode = CodeSlideSource.from_code_cell(cell)
            presentation.add_source_code(slode)

    presentation.write(output)
