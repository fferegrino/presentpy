import pytest

from presentpy.writer.theme import convert_color


@pytest.mark.parametrize(
    "color, expected_output",
    [
        ("#fff", "#ffffff"),
        ("#000", "#000000"),
        ("#123", "#112233"),
        ("#abcabc", "#abcabc"),
    ],
)
def test_convert_color(color, expected_output):
    assert convert_color(color) == expected_output
