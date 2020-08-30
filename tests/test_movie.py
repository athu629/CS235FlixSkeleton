import pytest

from domainmodel.movie import Movie
from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director


def test_init():
    movie1 = Movie("Moana", 2016)
    assert repr(movie1) == "<Movie Moana, 2016>"
    movie2 = Movie("", 0)
    assert movie2.title is None
    assert movie2.movie_date is None
    director1 = Director("Harry Potter")
    movie1.director = director1
    assert repr(movie1.director) == "<Director Harry Potter>"
    movie1.runtime_minutes = 122
    assert repr(movie1.runtime_minutes) == "122"
    movie3 = Movie("Harry Potter", 1997)
    movie3.runtime_minutes = "h"
    assert movie3.runtime_minutes is None
    movie4 = Movie("H", "h")
    assert movie4.movie_date is None

    description1 = "This is a cool movie"
    movie1.description = description1
    assert movie1.description == "This is a cool movie"

    movie5 = Movie("Title", 2000)
    description2 = 45
    movie5.description = description2
    assert movie5.description is None

    movie6 = Movie("ABC", 2000)
    description3 = "This is a funny movie   "
    movie6.description = description3
    assert movie6.description == "This is a funny movie"

    director2 = Director("Ron Weasley")
    movie1.director = director2

    m2 = Movie("Hello", 70000000000)
    m2.director = [Director("Hugh"), Director("Dane")]
    assert m2.director is None





def test_repr():
    movie1 = Movie("Moana", 2016)
    assert movie1.__repr__() == "<Movie Moana, 2016>"

def test_eq():
    movie1 = Movie("ABC", 2016)
    movie2 = Movie("ABC", 2016)
    movie3 = Movie("EFG", 2016)
    movie4 = Movie("ABC", 2014)
    assert movie1.__eq__(movie2) is True
    assert movie1.__eq__(movie3) is False
    assert movie1.__eq__(movie4) is False

def test_lt():
    movie1 = Movie("ABC", 2016)
    movie2 = Movie("ABC", 2020)
    movie3 = Movie("EFG", 2020)
    movie4 = Movie("EFG", 2014)
    assert movie1.__lt__(movie2) is True
    assert movie2.__lt__(movie3) is True
    assert movie2.__lt__(movie4) is True

def test_hash():
    movie1 = Movie("Moana", 2016)
    string1 = movie1.title + str(movie1.movie_date)
    assert movie1.__hash__() == hash(string1)
    movie2 = Movie("Green", "h")
    string2 = movie2.title + str(movie2.movie_date)
    assert movie2.__hash__() == hash(string2)

def test_add_actor():
    movie1 = Movie("House Bunny", 2020)
    actor1 = Actor("Anna Faris")
    movie1.add_actor(actor1)
    assert repr(movie1.actors) == "[<Actor Anna Faris>]"
    actor2 = Actor("Kat Dennings")
    movie1.add_actor(actor2)
    assert repr(movie1.actors) == "[<Actor Anna Faris>, <Actor Kat Dennings>]"
    actor3 = Actor("Emma Stone")
    movie1.add_actor(actor3)
    assert repr(movie1.actors) == "[<Actor Anna Faris>, <Actor Kat Dennings>, <Actor Emma Stone>]"

def test_remove_actor():
    movie1 = Movie("House Bunny", 2020)
    actor1 = Actor("Anna Faris")
    actor2 = Actor("Kat Dennings")
    actor3 = Actor("Emma Stone")
    movie1.add_actor(actor1)
    movie1.add_actor(actor2)
    assert repr(movie1.actors) == "[<Actor Anna Faris>, <Actor Kat Dennings>]"
    movie1.remove_actor(actor1)
    assert repr(movie1.actors) == "[<Actor Kat Dennings>]"
    movie1.remove_actor(actor3)


def test_add_genre():
    movie1 = Movie("House Bunny", 2020)
    genre1 = Genre("Comedy")
    movie1.add_genre(genre1)
    assert repr(movie1.genres) == "[<Genre Comedy>]"
    genre2 = Genre("Romance")
    movie1.add_genre(genre2)
    assert repr(movie1.genres) == "[<Genre Comedy>, <Genre Romance>]"
    genre3 = Genre("Drama")
    movie1.add_genre(genre3)
    assert repr(movie1.genres) == "[<Genre Comedy>, <Genre Romance>, <Genre Drama>]"


def test_remove_genre():
    movie1 = Movie("House Bunny", 2020)
    genre1 = Genre("Comedy")
    genre2 = Genre("Romance")
    movie1.add_genre(genre1)
    movie1.add_genre(genre2)
    assert repr(movie1.genres) == "[<Genre Comedy>, <Genre Romance>]"
    movie1.remove_genre(genre1)
    assert repr(movie1.genres) == "[<Genre Romance>]"

def test_accessing_items_in_actors_list():
    movie1 = Movie("House Bunny", 2020)
    actor1 = Actor("Anna Faris")
    actor2 = Actor("Kat Dennings")
    actor3 = Actor("Emma Stone")
    movie1.add_actor(actor1)
    movie1.add_actor(actor2)
    movie1.add_actor(actor3)
    assert repr(movie1.actors[0]) == "<Actor Anna Faris>"

def random_tests():
    m1 = Movie("","")
    assert repr(m1.title) is None
    assert repr(m1.movie_date) is None

    m2 = Movie("Hello", 70000000000)
    m2.director = [Director("Hugh"), Director("Dane")]
    assert repr(m2.director) is None



