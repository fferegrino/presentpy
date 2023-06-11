from presentpy.code_slide_source import CodeSlideSource


def test_from_source_code_single():
    source_code = """print("Hello World")"""
    expected_code_slide = CodeSlideSource(
        code=source_code,
        highlights=[],
        title=None
    )

    assert CodeSlideSource.from_source_code(source_code) == expected_code_slide

def test_from_source_multiple():
    source_code = """print("Hello World")
print("Hello World")"""
    expected_code_slide = CodeSlideSource(
        code=source_code,
        highlights=[],
        title=None
    )

    assert CodeSlideSource.from_source_code(source_code) == expected_code_slide


def test_from_source_multiple_with_config():
    source_code = """print("Hello World")
print("Hello World")
#% title=\"Hello World\""""
    expected_code_slide = CodeSlideSource(
        code="""print("Hello World")
print("Hello World")""",
        highlights=[],
        title="Hello World"
    )

    assert CodeSlideSource.from_source_code(source_code) == expected_code_slide

def test_from_source_multiple_with_highlights():
    source_code = """print("Hello World")
print("Hello World")
#% title=\"Hello World\" highlights=\"1-5,3-4\""""
    expected_code_slide = CodeSlideSource(
        code="""print("Hello World")
print("Hello World")""",
        highlights=[[1, 2, 3, 4, 5], [3, 4]],
        title="Hello World"
    )

    assert CodeSlideSource.from_source_code(source_code) == expected_code_slide

def test_from_source_multiple_with_highlights_no_quotes():
    source_code = """print("Hello World")
print("Hello World")
#% title=\"Hello World\" highlights=1-5,3-4"""
    expected_code_slide = CodeSlideSource(
        code="""print("Hello World")
print("Hello World")""",
        highlights=[[1, 2, 3, 4, 5], [3, 4]],
        title="Hello World"
    )

    assert CodeSlideSource.from_source_code(source_code) == expected_code_slide

def test_from_source_no_code():
    source_code = ""
    expected_code_slide = CodeSlideSource(
        code="",
        highlights=[],
        title=None
    )

    assert CodeSlideSource.from_source_code(source_code) == expected_code_slide
