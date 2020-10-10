import pytest

from domainmodel.watchlist import WatchList
from domainmodel.movie import Movie

def test_init():
    w1 = WatchList()
    assert len(w1.watch_list) == 0

def test_add_movie():
    w1 = WatchList()
    w1.add_movie(Movie("Moana", 2016))
    assert len(w1.watch_list) == 1

def test_remove_movie():
    w1 = WatchList()
    w1.add_movie(Movie("Moana", 2016))
    w1.add_movie(Movie("Ice Age", 2002))
    assert len(w1.watch_list) == 2
    w1.remove_movie(Movie("Moana", 2016))
    assert repr(w1.watch_list) == "[<Movie Ice Age, 2002>]"

def test_repr():
    w1 = WatchList()
    assert w1.__repr__() == "You have no movies saved in your watchlist."
    w1.add_movie(Movie("Moana", 2016))
    w1.add_movie(Movie("Ice Age", 2002))
    assert w1.__repr__() == "Watchlist:\n"\
                            "1 : <Movie Moana, 2016>\n"\
                            "2 : <Movie Ice Age, 2002>"

def test_eq():
    w1 = WatchList()
    w1.add_movie(Movie("Moana", 2016))
    w1.add_movie(Movie("Ice Age", 2002))
    w2 = WatchList()
    w2.add_movie(Movie("Ice Age", 2002))
    w2.add_movie(Movie("Moana", 2016))
    assert w1.__eq__(w2) is True
    w3 = WatchList()
    w3.add_movie(Movie("House Bunny", 2002))
    assert w1.__eq__(w3) is False

def test_select_movie_to_watch():
    pass

def test_size():
    w1 = WatchList()
    assert w1.size() == 0
    w1.add_movie(Movie("Moana", 2016))
    w1.add_movie(Movie("Ice Age", 2002))
    assert w1.size() == 2

def test_first_movie_in_watchlist():
    w1 = WatchList()
    assert w1.first_movie_in_watchlist() is None
    w1.add_movie(Movie("Moana", 2016))
    assert repr(w1.first_movie_in_watchlist()) == "<Movie Moana, 2016>"

def test_iter_and_next():
    w1 = WatchList()
    w1.add_movie(Movie("Moana", 2016))
    w1.add_movie(Movie("Ice Age", 2002))
    iter_lst = w1.__iter__()
    with pytest.raises(StopIteration):
        while True:
            iter_lst.__next__()


