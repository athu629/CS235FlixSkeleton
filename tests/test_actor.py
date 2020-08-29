import pytest

from domainmodel.actor import Actor

def test_init():
    actor1 = Actor("Emma Stone")
    assert repr(actor1) == "<Actor Emma Stone>"
    actor2 = Actor("")
    assert actor2.actor_full_name is None
    actor3 = Actor(42)
    assert actor3.actor_full_name is None

def test_repr():
    actor1 = Actor("Emma Stone")
    assert actor1.__repr__() == "<Actor Emma Stone>"

def test_eq():
    pass
    """
    genre1 = Genre("Drama")
    genre2 = Genre("Mystery")
    genre3 = Genre("Drama")
    genre4 = Genre("Drama,Romance")
    genre5 = Genre("Romance,Drama")
    assert genre1.__eq__(genre2) is False
    assert genre1.__eq__(genre3) is True
    assert genre3.__eq__(genre4) is False
    #assert genre4.__eq__(genre5) is True
    """

def test_lt():
    actor1 = Actor("Julia Roberts")
    actor2 = Actor("Henry Cavill")
    assert actor2.__lt__(actor1) is True
    #assert director3.__lt__(director2) is True

def test_hash():
    actor1 = Actor("Johnny Depp")
    assert actor1.__hash__() == hash(actor1)

def test_add_actor_colleague():
    actor1 = Actor("Emma Stone")
    actor2 = Actor("Henry Cavill")
    actor1.add_actor_colleague(actor2)
    assert actor1.actor_colleague_list == ["Henry Cavill"]

def test_check_if_this_actor_worked_with():
    actor1 = Actor("Emma Stone")
    actor2 = Actor("Henry Cavill")
    actor1.add_actor_colleague(actor2)
    assert actor1.check_if_this_actor_worked_with(actor2) == True
