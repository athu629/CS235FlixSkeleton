import unittest
from datetime import date, datetime
from typing import List

import os
import pytest

from adapters.repository import RepositoryException
from adapters import memory_repository
from adapters.memory_repository import MemoryRepository, populate
from domainmodel.movie import Movie
from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.review import Review
from domainmodel.user import User
from domainmodel.watchlist import WatchList




# user tests - add watched movies, total watch time, reviews relative to user
def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user('dave') is user

def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None

# movie tests
def test_repository_can_add_movie(in_memory_repo):
    movie = Movie("Hello", 2000)
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie("Hello2000") is movie

def test_repository_can_retrieve_a_movie_by_title_and_year(in_memory_repo):
    movie = in_memory_repo.get_movie("The Great Wall2016")
    assert movie == Movie("The Great Wall", 2016)

def test_repository_can_retrieve_movies_by_title(in_memory_repo):
    movie_list = in_memory_repo.get_list_of_movies_by_title(["The Great Wall", "Guardians of the Galaxy", "Passengers"])
    assert len(movie_list) == 3

def test_repository_can_retrieve_a_movies_by_year(in_memory_repo):
    date_list = in_memory_repo.get_list_of_movies_by_year(2016)
    assert len(date_list) == 6

def test_repository_can_retrieve_movie_count(in_memory_repo):
    count = in_memory_repo.get_number_of_movies()
    assert count == 10

def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie("Burlesque2000")
    assert movie is None

def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie == Movie("Guardians of the Galaxy", 2014)

def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie == Movie("The Lost City of Z", 2016)

# hoping repo should be in alphabetical order
def test_repository_can_get_next_movie(in_memory_repo):
    movie1 = in_memory_repo.get_first_movie()
    movie2 = in_memory_repo.get_next_movie(movie1)
    assert movie2 == Movie("La La Land", 2016)

def test_repository_can_get_previous_movie(in_memory_repo):
    movie1 = in_memory_repo.get_last_movie()
    movie2 = in_memory_repo.get_previous_movie(movie1)
    assert movie2 == Movie("The Great Wall", 2016)

def test_repository_can_get_next_movie_year(in_memory_repo):
    movie1 = in_memory_repo.get_last_movie()
    next_date = in_memory_repo.get_next_year(movie1)
    assert next_date == 2017

def test_repository_can_get_previous_movie_year(in_memory_repo):
    movie1 = in_memory_repo.get_last_movie()
    prev_date = in_memory_repo.get_previous_year(movie1)
    assert prev_date == 2015

def test_repository_does_not_retrieve_date_for_non_existent_date(in_memory_repo):
    pass

# previous and next method loop round
def test_repository_can_retrieve_next_first_movie_when_at_the_end_of_the_list(in_memory_repo):
    movie1 = in_memory_repo.get_last_movie()
    movie2 = in_memory_repo.get_next_movie(movie1)
    assert movie2 == Movie("Guardians of the Galaxy", 2014)

def test_repository_can_retrieve_the_previous_last_movie_when_at_the_start_of_the_list(in_memory_repo):
    movie1 = in_memory_repo.get_first_movie()
    movie2 = in_memory_repo.get_previous_movie(movie1)
    assert movie2 == Movie("The Lost City of Z", 2016)

def test_repository_does_not_retrieve_movie_for_non_exisitent_title(in_memory_repo):
    movie1 = in_memory_repo.get_movie("WASSUP2000")
    assert movie1 is None

def test_repository_does_not_retrieve_movie_for_non_exisitent_year(in_memory_repo):
    date_list = in_memory_repo.get_list_of_movies_by_year([1600])
    assert date_list is None

def test_repository_can_retrieve_users_watched_movies(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    movie1 = in_memory_repo.get_first_movie()
    user.watch_movie(movie1)
    assert user.watched_movies[0] == Movie("Guardians of the Galaxy", 2014)

def test_repository_can_retrieve_users_total_time_spent_watching_movies(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    movie1 = in_memory_repo.get_first_movie()
    user.watch_movie(movie1)
    assert user.time_spent_watching_movies_minutes == 121

def test_repository_can_retrieve_reviews_the_user_has_written(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    movie1 = in_memory_repo.get_first_movie()
    review_text = "Really good movie"
    rating = 8
    rev = Review(movie1,review_text,rating)
    user.add_review(rev)
    assert user.reviews[0] == Review(Movie("Guardians of the Galaxy", 2014), "Really good movie", 8)

# test other factors of the movie - actor, director, genre, runtime
def test_repository_can_retrieve_actors_by_movie(in_memory_repo):
    movie1 = in_memory_repo.get_movie("Guardians of the Galaxy2014")
    actors1 = movie1.actors
    assert actors1 == [Actor("Chris Pratt"), Actor("Vin Diesel"), Actor("Bradley Cooper"), Actor("Zoe Saldana")]

def test_repository_can_retrieve_movies_with_chosen_actor(in_memory_repo):
    actor = Actor("Chris Pratt")
    movies1 = in_memory_repo.get_list_of_movies_by_actor(actor)
    assert movies1 == [Movie("Guardians of the Galaxy", 2014), Movie("Passengers", 2016)]

def test_repository_can_retrieve_movie_by_director(in_memory_repo):
    director = Director("Sean Foley")
    movies1 = in_memory_repo.get_list_of_movies_by_director(director)
    assert movies1 == [Movie("Mindhorn", 2016)]

def test_repository_can_retrieve_movie_by_genre(in_memory_repo):
    genre = Genre("Fantasy")
    movies = in_memory_repo.get_list_of_movies_by_genre(genre)
    assert movies == [Movie("Suicide Squad", 2016), Movie("The Great Wall", 2016)]

def test_repository_can_retrieve_movie_runtime(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.runtime_minutes == 121

# test review
def test_repository_can_add_a_review(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    user = in_memory_repo.get_user('fmercury')
    review = Review(movie, "I like, great!", 7)
    in_memory_repo.add_review(user, review)
    assert movie in in_memory_repo._movie_review_list
    assert in_memory_repo._movie_review_list[movie][0] == User('fmercury', '8734gfe2058v')

def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    review = Review(movie, "I like it!", 7)
    user = in_memory_repo.get_user('prince')
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(user, review)

def test_repository_does_not_add_a_review_without_an_movie_properly_attached(in_memory_repo):
    movie = None
    review = Review(movie, "Sucked", 2)
    user = in_memory_repo.get_user('fmercury')
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(user, review)

def test_repository_can_retrieve_reviews(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    review1 = Review(movie, "Sucked", 2)
    user1 = in_memory_repo.get_user('fmercury')
    in_memory_repo.add_review(user1, review1)
    review2 = Review(movie, "Fantastic", 8)
    user2 = in_memory_repo.get_user('thorke')
    in_memory_repo.add_review(user2, review2)
    assert len(in_memory_repo._reviews) == 2


def test_repository_can_retrieve_reviews_by_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    review1 = Review(movie, "Sucked", 2)
    user1 = in_memory_repo.get_user('fmercury')
    in_memory_repo.add_review(user1, review1)
    review2 = Review(movie, "Fantastic", 8)
    user2 = in_memory_repo.get_user('thorke')
    in_memory_repo.add_review(user2, review2)
    list1 = in_memory_repo.get_reviews_by_movie(movie)
    assert list1 == [review1, review2]

def test_repository_can_retrieve_reviews_by_user(in_memory_repo):
    movie1 = in_memory_repo.get_first_movie()
    movie2 = in_memory_repo.get_last_movie()
    review1 = Review(movie1, "Sucked", 2)
    review2 = Review(movie1, "Fantastic", 8)
    user1 = in_memory_repo.get_user('fmercury')
    in_memory_repo.add_review(user1, review1)
    in_memory_repo.add_review(user1, review2)
    list1 = in_memory_repo.get_reviews_by_user(user1)
    assert list1 == [review1, review2]