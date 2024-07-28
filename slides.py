#

import argparse
import shutil
import xml.dom.minidom
import zipfile
from pathlib import Path


def unpptx(pptx_folder):
    for pptx_file in Path(pptx_folder).glob("*.odp"):
        if pptx_file.stem.startswith("~$"):
            continue

        output_folder = Path(pptx_folder) / f"{pptx_file.stem}_odp"

        with zipfile.ZipFile(pptx_file, "r") as zip_ref:
            zip_ref.extractall(output_folder)

        def prettify_files(pattern):
            for xml_file in output_folder.glob(pattern):
                with open(xml_file, "r") as f:
                    xml_string = f.read()
                    dom = xml.dom.minidom.parseString(xml_string)
                    pretty_xml_as_string = dom.toprettyxml()
                    pretty_xml_as_string = "\n".join(
                        [line for line in pretty_xml_as_string.split("\n") if line.strip()]
                    )

                with open(xml_file, "w") as f:
                    f.write(pretty_xml_as_string)
                    f.write("\n")

        prettify_files("**/*.xml")
        prettify_files("**/*.rels")


def dopptx(pptx_folder, delete_original):
    for pptx_exploded_folder in Path(pptx_folder).glob("*_odp"):
        deck_name = pptx_exploded_folder.stem[:-4]
        pptx_file = Path(pptx_folder) / f"{deck_name}.odp"

        with zipfile.ZipFile(pptx_file, "w") as zip_ref:
            for file in pptx_exploded_folder.glob("**/*"):
                zip_ref.write(file, file.relative_to(pptx_exploded_folder))

        if delete_original:
            shutil.rmtree(pptx_exploded_folder)


def main():
    parser = argparse.ArgumentParser(description="Process PPTX files.")
    subparsers = parser.add_subparsers(dest="command")

    # Create parser for the "unpptx" command
    parser_unpptx = subparsers.add_parser("unpptx")
    parser_unpptx.add_argument("pptx_folder", type=str, help="Folder containing PPTX files")

    # Create parser for the "dopptx" command
    parser_dopptx = subparsers.add_parser("dopptx")
    parser_dopptx.add_argument("pptx_folder", type=str, help="Folder containing PPTX files")
    parser_dopptx.add_argument(
        "--delete-original", action="store_true", help="Delete the original files after processing"
    )

    args = parser.parse_args()

    if args.command == "unpptx":
        unpptx(args.pptx_folder)
    elif args.command == "dopptx":
        dopptx(args.pptx_folder, args.delete_original)


if __name__ == "__main__":
    main()
