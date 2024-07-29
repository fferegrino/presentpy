import nbformat
import pytest
from pygments.token import Token

from presentpy.code_slide_source import (
    CodeSlideSource,
    get_parsed_lines,
    parse_highlights,
    parse_magic_config,
)


@pytest.fixture
def test_notebook(pytestconfig):
    file = pytestconfig.rootpath / "tests" / "files" / "test.ipynb"
    with open(file) as f:
        notebook = nbformat.read(f, as_version=4)
    return notebook


@pytest.fixture
def get_cell(test_notebook):

    def get_cell_index(idx):
        return test_notebook.cells[idx]

    return get_cell_index


def test_get_parsed_lines_default():
    source = "print('Hello, World!')\nprint('Goodbye, World!')"
    expected_output = [
        [
            (Token.Name.Builtin, "print"),
            (Token.Punctuation, "("),
            (Token.Literal.String.Single, "'"),
            (Token.Literal.String.Single, "Hello, World!"),
            (Token.Literal.String.Single, "'"),
            (Token.Punctuation, ")"),
        ],
        [
            (Token.Name.Builtin, "print"),
            (Token.Punctuation, "("),
            (Token.Literal.String.Single, "'"),
            (Token.Literal.String.Single, "Goodbye, World!"),
            (Token.Literal.String.Single, "'"),
            (Token.Punctuation, ")"),
        ],
    ]

    result = get_parsed_lines(source)

    assert result == expected_output


def test_full_parse(get_cell):
    cell = get_cell(0)

    real_source = "\n".join(cell.source.split("\n")[:-1])

    code_slide = CodeSlideSource.from_code_cell(cell)

    assert code_slide.code == cell.source
    assert code_slide.title == "Find the H.C.F of two numbers"
    assert code_slide.outputs == ["The H.C.F. is 100", "100"]
    assert code_slide.lines == get_parsed_lines(real_source)
    # fmt: off
    assert code_slide.highlights == [[-1,],[1,],[2,3,],[4,5,],[9,],]
    # fmt: on


@pytest.mark.parametrize(
    "source, expected_output",
    [
        # fmt: off
        ("1,2-3,4-5,9", [[1],[2,3],[4,5],[9]]),
        ("1", [[1]]),
        ("1-9", [[1, 2, 3, 4, 5, 6, 7, 8, 9]]),
        # fmt: on
    ],
)
def test_parse_highlights_single_range(source, expected_output):
    result = parse_highlights(source)
    assert result == expected_output


@pytest.mark.parametrize(
    ["config", "expected_config"],
    [
        # fmt: off
    (
        "#% title=\"Hello, World!\"",
        {"title": "Hello, World!"}
    ),
    (
        "#% highlights=1,2-3,4-5,9",
        {"highlights": "1,2-3,4-5,9"}
    ),
    (
        "#% title=\"Hello, World!\" highlights=1,2-3,4-5,9",
        {"title": "Hello, World!", "highlights": "1,2-3,4-5,9"}
    )
        # fmt: on
    ],
)
def test_parse_magic_config(config, expected_config):
    result = parse_magic_config(config)
    assert result == expected_config
