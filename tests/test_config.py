from presentpy.config.read_only_dot_dict import ReadOnlyDotDict


def test_read_only_dot_dict():
    test_dict = {
        "a": 1,
        "b": {
            "c": 2,
            "d": 3,
            "e": {
                "f": 4,
            },
        },
    }

    read_only_dot_dict = ReadOnlyDotDict(test_dict)

    assert read_only_dot_dict.a == 1
    assert read_only_dot_dict.b.c == 2
    assert read_only_dot_dict.b.d == 3
    assert read_only_dot_dict.b.e.f == 4
    assert read_only_dot_dict.b.e["f"] == 4
    assert read_only_dot_dict.b["e"].f == 4
    assert read_only_dot_dict.b["e"]["f"] == 4
    assert read_only_dot_dict.b.e.get("g") is None
    assert read_only_dot_dict.b.e.get("g", 5) == 5
