import pytest

from domainmodel.genre import Genre

def test_init():
    genre1 = Genre("Comedy,Horror")
    assert repr(genre1) == "<Genre Comedy,Horror>"
    genre2 = Genre("")
    assert genre2.genre_name is None
    genre3 = Genre(42)
    assert genre3.genre_name is None

def test_repr():
    genre1 = Genre("Comedy, Horror")
    assert genre1.__repr__() == "<Genre Comedy, Horror>"

def test_eq():
    genre1 = Genre("Drama")
    genre2 = Genre("Mystery")
    genre3 = Genre("Drama")
    genre4 = Genre("Drama,Romance")
    genre5 = Genre("Romance,Drama")
    assert genre1.__eq__(genre2) is False
    assert genre1.__eq__(genre3) is True
    assert genre3.__eq__(genre4) is False
    #assert genre4.__eq__(genre5) is True

def test_lt():
    genre1 = Genre("Drama")
    genre2 = Genre("Mystery")
    assert genre1.__lt__(genre2) is True
    #assert director3.__lt__(director2) is True

def test_hash():
    genre1 = Genre("Drama, Horror")
    assert genre1.__hash__() == hash(genre1)
