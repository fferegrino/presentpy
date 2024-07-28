import shlex
from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple

from nbformat import NotebookNode
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import Token


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

    if line:
        lines.append(line)

    return lines



def parse_highlights(highlights: str) -> List[List[int]]:
    highlight_ints = []
    lines_to_highlights = highlights.split(",")
    for highlighted_lines in lines_to_highlights:
        start, _, end = highlighted_lines.partition("-")
        if end:
            highlight_ints.append(list(range(int(start), int(end) + 1)))
        else:
            highlight_ints.append([int(start)])
    return highlight_ints


@dataclass
class CodeSlideSource:
    code: str
    lines: List[List[Tuple[Any, str]]]
    highlights: List[List[int]] = field(default_factory=list)
    outputs: Optional[List[str]] = None
    title: Optional[str] = None

    @classmethod
    def from_code_cell(cls, cell: NotebookNode):
        source_lines = cell.source.strip().split("\n")
        source_code = cell.source

        config = {}
        last_line = source_lines[-1]
        if last_line.startswith("#%"):
            config = {
                key: value for key, _, value in [conf.partition("=") for conf in shlex.split(last_line[2:].strip())]
            }

            source_code = "\n".join(source_lines[:-1])

        dataclass_attributes = {"title": config.get("title")}

        dataclass_attributes["highlights"] = [[-1]]
        if highlights := config.get("highlights"):
            dataclass_attributes["highlights"].extend(parse_highlights(highlights))

        dataclass_attributes["outputs"] = []

        stream = [output for output in cell.outputs if output.output_type == "stream"]
        execute_result = [output for output in cell.outputs if output.output_type == "execute_result"]

        if stream:
            dataclass_attributes["outputs"].extend(stream[0].text.strip().split("\n"))
        if execute_result:
            dataclass_attributes["outputs"].extend(execute_result[0].data["text/plain"].strip().split("\n"))

        return cls(
            code=cell.source,
            lines=get_parsed_lines(source_code),
            **dataclass_attributes,
        )
