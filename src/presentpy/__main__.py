from typing import Any, List, Tuple

import click
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import Token

from presentpy.code_slide_source import CodeSlideSource
from presentpy.namespaces import Namespaces
from presentpy.writer.presentation import Presentation
from presentpy.writer.slides import dopptx
from presentpy.writer.theme import Theme


def get_parsed_lines(source: str, language: str = "python") -> List[List[Tuple[Any, str]]]:
    lines = []
    line = []
    lexer = get_lexer_by_name(language)
    for token, value in lex(source, lexer):
        if token is Token.Text.Whitespace and value == "\n":
            lines.append(line)
            line = []
        else:
            line.append((token, value))

    lines.append(line)

    return lines


code = """
from typing import Iterator

# This is an example
class Math:
    @staticmethod
    def fib(n: int) -> Iterator[int]:
        \"\"\"Fibonacci series up to n.\"\"\"
        a, b = 0, 1
        while a < n:
            yield a
            a, b = b, a + b

result = sum(Math.fib(42))
print(f"The answer is {result}")
#% title="Find the H.C.F of two numbers" highlights=1,2-3,4-5,9
"""


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
# @click.argument("notebook", type=click.Path(exists=True))
@click.option("--theme", default="default")
def process(theme):
    namespaces = Namespaces(odf_namespaces)
    theme = Theme(theme, namespaces)
    presentation = Presentation(theme, namespaces)

    # slide = presentation.new_slide("slide1")

    slode = CodeSlideSource.from_source_code(code)
    # slide.add_source_code(slode)

    presentation.add_source_code(slode)

    presentation.write("result")

    import platform
    import subprocess

    if platform.system() == "Darwin":  # macOS
        subprocess.call(("open", "result.odp"))
