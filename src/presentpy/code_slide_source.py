import shlex
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CodeSlideSource:
    code: str
    highlights: List[List[int]] = field(default_factory=list)
    title: Optional[str] = None

    @classmethod
    def from_source_code(cls, source_code: str):
        source_lines = source_code.strip().split("\n")

        config = {}
        last_line = source_lines[-1]
        if last_line.startswith("#%"):
            config = {
                key: value for key, _, value in
                [conf.partition("=") for conf in shlex.split(last_line[2:].strip())]
            }

            source_code = "\n".join(source_lines[:-1])

        dataclass_atrributes = {"title": config.get("title")}

        if highlights := config.get("highlights"):
            lines_to_highlights = highlights.split(",")
            highlight_ints = []
            for highlighted_lines in lines_to_highlights:
                start, _, end = highlighted_lines.partition("-")
                if end:
                    highlight_ints.append(list(range(int(start), int(end) + 1)))
                else:
                    highlight_ints.append([int(start)])

            dataclass_atrributes["highlights"] = highlight_ints

        return cls(code=source_code,**dataclass_atrributes)