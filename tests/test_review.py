import pytest

from domainmodel.movie import Movie
from domainmodel.review import Review


def test_init():
    movie = Movie("Moana", 2016)
    review_text = "This movie was very enjoyable."
    rating = 14
    review = Review(movie, review_text, rating)
    assert repr(review.movie) == "<Movie Moana, 2016>"
    assert review.rating == None
    assert review.review_text == "This movie was very enjoyable."


def test_repr():
    movie1 = Movie("ABC", 2016)
    review_text = "This movie was very enjoyable."
    rating = 8
    review = Review(movie1, review_text, rating)
    assert repr(review) == "<ABC, Rating: 8, Review: This movie was very enjoyable.>"

def test_eq():
    movie1 = Movie("ABC", 2016)
    movie2 = Movie("EFG", 2020)
    movie3 = movie2
    review_text1 = "This movie was very enjoyable."
    rating1 = 8
    review_text2 = "Meh."
    rating2 = 4
    review1 = Review(movie1, review_text1, rating1)
    review2 = Review(movie2, review_text2, rating2)
    review3 = Review(movie3, review_text2, rating2)
    assert review1.__eq__(review2) is False
    assert review2.__eq__(review3) is True
