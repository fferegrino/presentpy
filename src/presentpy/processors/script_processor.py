from pathlib import Path

from presentpy.code_slide_source import CodeSlideSource


class ScriptProcessor:
    def __init__(self, script_path: Path, writer):
        self.script_path = script_path
        self.writer = writer

    def process(self):
        with open(self.script_path, "r") as f:
            source_code = f.read()

        code_slide_source = CodeSlideSource.from_source_code(source_code)
        self.writer.write(code_slide_source)
