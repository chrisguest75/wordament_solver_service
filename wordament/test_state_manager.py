import pytest
from state_manager import state_manager_factory

def test_singleton():
    sm1 = state_manager_factory.create()
    sm2 = state_manager_factory.create()
    assert(id(sm1) == id(sm2))

def test_empty():
    sm = state_manager_factory.create()
    assert(len(sm.names()) == 0)

def test_add_named_object():
    sm = state_manager_factory.create()
    sm.add("hello", {})
    assert(len(sm.names()) == 1)
    assert(sm.exists("hello"))

def test_added_named_object_exists():
    sm = state_manager_factory.create()
    assert(len(sm.names()) == 0)
    sm.add("hello", {})
    assert(len(sm.names()) == 1)
    assert(sm.names()[0] == "hello")

def test_get_named_object():
    sm = state_manager_factory.create()
    assert(len(sm.names()) == 0)
    sm.add("hello", {"value": 10})
    assert(len(sm.names()) == 1)
    assert("value" in sm.get("hello"))
    assert(sm.get("hello")["value"] == 10)
