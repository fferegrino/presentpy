import pytest

from presentpy.namespaces import Namespaces


def test_call_with_namespace():
    ns = Namespaces({"ns": "http://example.com/ns"})
    resolved_tag = ns("ns:tag")
    assert resolved_tag == "{http://example.com/ns}tag"


def test_call_without_namespace():
    ns = Namespaces({"ns": "http://example.com/ns"})
    resolved_tag = ns("tag")
    assert resolved_tag == "tag"


def test_resolve_with_namespace():
    ns = Namespaces({"ns": "http://example.com/ns"})
    resolved_tag = ns.resolve("ns:tag")
    assert resolved_tag == "{http://example.com/ns}tag"


def test_resolve_without_namespace():
    ns = Namespaces({"ns": "http://example.com/ns"})
    resolved_tag = ns.resolve("tag")
    assert resolved_tag == "tag"


def test_raises_if_namespace_not_found():
    ns = Namespaces({"ns": "http://example.com/ns"})
    with pytest.raises(KeyError):
        ns.resolve("other:tag")
