from datetime import date

import pytest

#from covid.authentication.services import AuthenticationException
from movies import services as movie_services
from domainmodel.movie import Movie
from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.review import Review
from domainmodel.user import User
#from covid.authentication import services as auth_services
from movies.services import NonExistentMovieException

def test_can_add_review(in_memory_repo):
    movie_id = "The Great Wall2016"
    review_text = "So Good!"
    user_name = "fmercury"
    rating = 8

    # Call the movie.service layer to add the review
    movie_services.add_review(movie_id, review_text, user_name, rating, in_memory_repo)

    # retrieve the reviews for the movie from the repo
    reviews_as_dict = movie_services.get_reviews_for_movie(movie_id, in_memory_repo)

    # Check that the reviews include a comment with the new text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None

def test_cannot_add_comment_for_non_existent_movie(in_memory_repo):
    movie_id = "Blah2016"
    review_text = "he is such a good actor!"
    rating = 3
    user_name = 'fmercury'

    # Call the service layer to attempt to add the review.
    with pytest.raises(movie_services.NonExistentMovieException):
        movie_services.add_review(movie_id, review_text, user_name, rating, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie = "The Great Wall2016"
    review_text = 'The cinematography is on point!'
    user_name = 'gmichael'
    rating = 6

    # Call the service layer to attempt to add the review.
    with pytest.raises(movie_services.UnknownUserException):
        movie_services.add_review(movie, review_text, user_name, rating, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie = "The Great Wall2016"

    movie_as_dict = movie_services.get_movie(movie, in_memory_repo)

    assert movie_as_dict['title'] == "The Great Wall"
    assert movie_as_dict['year'] == 2016
    assert movie_as_dict['genres'] == [Genre('Action'), Genre('Adventure'), Genre('Fantasy')]
    assert movie_as_dict['actors'] == [Actor('Matt Damon'), Actor('Tian Jing'), Actor('Willem Dafoe'), Actor('Andy Lau')]
    assert movie_as_dict['director'] == Director('Yimou Zhang')
    assert movie_as_dict['description'] == 'European mercenaries searching for black powder become embroiled in the defense of the Great Wall of China against a horde of monstrous creatures.'
    assert movie_as_dict['runtime'] == 103


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = "hello"

    # Call the service layer to attempt to retrieve the movie.
    with pytest.raises(movie_services.NonExistentMovieException):
        movie_services.get_movie(movie_id, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movie_services.get_first_movie(in_memory_repo)

    assert movie_as_dict['title'] == 'Guardians of the Galaxy'


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movie_services.get_last_movie(in_memory_repo)

    # not the last one in the csv file - the last one alphabetically
    assert movie_as_dict['title'] == "The Lost City of Z"

def test_get_movies_by_year_with_one_year(in_memory_repo):
    target_year = 2012

    # should return one movie and none for prev and next
    # movie_as_dict, prev_date, next_date = movie_services.get_list_of_movies_by_year(target_year, in_memory_repo)
    pass


def test_get_movies_by_year_with_multiple_years(in_memory_repo):
    target_year = 2016

    movies_as_dict, prev_date, next_date = movie_services.get_list_of_movies_by_year(target_year, in_memory_repo)

    # Check that there are 6 movies produced in 2016.
    assert len(movies_as_dict) == 6

    # Check that the article ids for the the articles returned are 3, 4 and 5.
    movie_title = [movie['title'] for movie in movies_as_dict]
    #assert set([3, 4, 5]).issubset(article_ids) get titls off all from 2016

    # Check that the dates of articles surrounding the target_date are 2020-02-29 and 2020-03-05.
    assert prev_date == 2015
    assert next_date == 2017


def test_get_movies_by_year_with_non_existent_year(in_memory_repo):
    target_year = 2021

    movies_as_dict, prev_date, next_date = movie_services.get_list_of_movies_by_year(target_year, in_memory_repo)

    # Check that there are no movies produced in 2021.
    assert len(movies_as_dict) == 0


def test_get_movies_by_id(in_memory_repo):
    target_movies_ids = ["The Great Wall2016", "Passengers2016"]
    movies_as_list = movie_services.get_movies_by_id(target_movies_ids, in_memory_repo)
    # Check that 2 movies were returned from the query.
    assert len(movies_as_list) == 2

    # Check that the movie ids returned were 5 and 6.
    #movie_ids = [article['id'] for article in articles_as_dict]
    #assert set([5, 6]).issubset(article_ids)


def test_get_comments_for_article(in_memory_repo):
    movie_id = "The Great Wall2016"
    review_text = "So Good!"
    user_name = "fmercury"
    rating = 8
    review_text2 = "Crappy"
    user_name2 = "thorke"
    rating2 = 2

    # Call the movie.service layer to add the review
    movie_services.add_review(movie_id, review_text, user_name, rating, in_memory_repo)
    movie_services.add_review(movie_id, review_text2, user_name2, rating2, in_memory_repo)

    reviews_as_dict = movie_services.get_reviews_for_movie(movie_id, in_memory_repo)

    # Check that 2 comments were returned for article with id 1.
    assert len(reviews_as_dict) == 2

    # Check that the reviews relate to the movie The Great Wall.
    movie_ids = [review['movie_title'] for review in reviews_as_dict]
    movie_ids = set(movie_ids)
    assert "The Great Wall" in movie_ids and len(movie_ids) == 1


def test_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        reviews_as_dict = movie_services.get_reviews_for_movie("Hello", in_memory_repo)


def test_get_reviews_for_movie_without_reviews(in_memory_repo):
    reviews_as_dict = movie_services.get_reviews_for_movie("The Great Wall2016", in_memory_repo)
    assert len(reviews_as_dict) == 0
