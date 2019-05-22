import pytest
from state_manager_factory import state_manager_factory, injector_factory


@pytest.fixture(autouse=True)
def setup_test():
    injector_factory.configure(True)  


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


def test_add_second_named_object():
    sm = state_manager_factory.create()
    assert(len(sm.names()) == 0)
    sm.add("hello", {"value": 10})
    sm.add("hello", {"value1": 20})
    sm.add("hello2", {"value9": 9})
    sm.add("hello2", {"value10": 100})
    assert(len(sm.names()) == 2)
    assert("value" in sm.get("hello"))
    assert(sm.get("hello")["value"] == 10)
    assert("value1" in sm.get("hello"))
    assert(sm.get("hello")["value1"] == 20)

    assert("value9" in sm.get("hello2"))
    assert(sm.get("hello2")["value9"] == 9)
    assert("value10" in sm.get("hello2"))
    assert(sm.get("hello2")["value10"] == 100)
