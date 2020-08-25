import pytest

from domainmodel.director import Director

def test_init():
    director1 = Director("Taika Waititi")
    assert repr(director1) == "<Director Taika Waititi>"
    director2 = Director("")
    assert director2.director_full_name is None
    director3 = Director(42)
    assert director3.director_full_name is None

def test_repr(self):
    pass

def test_eq(self):
    pass

def test_lt():
    director1 = Director("Taika Waititi")
    director2 = Director("ZAika Waititi")
    #director3 = Director("ZAika Waititi")
    assert director1.__lt__(director2) is True
    #assert director3.__lt__(director2) is True

def test_hash():
    director1 = Director("Alyssa")
    assert director1.__hash__() == hash(director1)

