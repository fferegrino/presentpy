from pathlib import Path
import shutil

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
            for xml_file in output_folder.glob(pattern):
                with open(xml_file, "r") as f:
                    xml_string = f.read()
                    dom = xml.dom.minidom.parseString(xml_string)
                    pretty_xml_as_string = dom.toprettyxml()
                with open(xml_file, "w") as f:
                    f.write(pretty_xml_as_string)

        prettify_files("**/*.xml")
        prettify_files("**/*.rels")


@cli.command()
@click.argument("pptx-folder", type=click.Path(exists=True, file_okay=False))
@click.option("--delete-original", is_flag=True, default=False)
def dopptx(pptx_folder, delete_original):
    for pptx_exploded_folder in Path(pptx_folder).glob("*_pptx"):
        deck_name = pptx_exploded_folder.stem[:-5]
        pptx_file = Path(pptx_folder) / f"{deck_name}.pptx"

        with zipfile.ZipFile(pptx_file, "w") as zip_ref:
            for file in pptx_exploded_folder.glob("**/*"):
                zip_ref.write(file, file.relative_to(pptx_exploded_folder))

        if delete_original:
            shutil.rmtree(pptx_exploded_folder)


if __name__ == "__main__":
    cli()
