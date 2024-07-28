import pytest

from presentpy.namespaces import Namespaces
from presentpy.writer.tag import Tag


@pytest.fixture
def nsmap():
    return {
        "test": "http://test.com",
        "custom": "http://custom.com",
    }


@pytest.fixture
def namespaces(nsmap):
    return Namespaces(nsmap)


@pytest.mark.parametrize(
    "element_name",
    [
        "test",
        "tag",
        "custom:page",
        "test:thing",
    ],
)
@pytest.mark.parametrize(
    "attributes",
    [None, {"id": "123"}, {"id": "123", "class": "test"}, {"test:abc": "123", "test:def": "456", "id": "789"}],
)
@pytest.mark.parametrize("text", [None, "Hello, World!"])
def test_to_element(namespaces, element_name, attributes, text):
    tag = Tag(element_name=element_name, namespaces=namespaces, attributes=attributes)

    if text is not None:
        tag.text = text

    element = tag.to_element()

    assert element.tag == namespaces(element_name)
    if attributes is not None:
        for attr, value in attributes.items():
            assert element.get(namespaces(attr)) == value

    if text is not None:
        assert element.text == text
