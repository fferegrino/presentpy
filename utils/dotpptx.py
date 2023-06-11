from pathlib import Path

import zipfile

import click

import xml.dom.minidom


@click.group()
def cli():
    pass


@cli.command()
@click.argument("pptx-folder", type=click.Path(exists=True, file_okay=False))
def unpptx(pptx_folder):
    for pptx_file in Path(pptx_folder).glob("*.pptx"):
        if pptx_file.stem.startswith("~$"):
            continue

        output_folder = Path(pptx_folder) / f"{pptx_file.stem}_pptx"

        with zipfile.ZipFile(pptx_file, "r") as zip_ref:
            zip_ref.extractall(output_folder)

        def prettify_files(pattern):
            # Pretty print the XML files
            for xml_file in output_folder.glob(pattern):
                with open(xml_file, "r") as f:
                    xml_string = f.read()
                    dom = xml.dom.minidom.parseString(xml_string)
                    pretty_xml_as_string = dom.toprettyxml()
                with open(xml_file, "w") as f:
                    f.write(pretty_xml_as_string)

        prettify_files("**/*.xml")
        prettify_files("**/*.rels")


if __name__ == "__main__":
    cli()
