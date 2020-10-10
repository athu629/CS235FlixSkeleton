from typing import List, Iterable

from adapters.repository import AbstractRepository
# from adapters.memory_repository import
from domainmodel.movie import Movie
from domainmodel.genre import Genre
from domainmodel.review import Review
from utilities.services import movie_to_dict


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_id: str, review_text: str, user_name: str, rating: int, repo: AbstractRepository):
    # Check that the article exists.
    movie1 = repo.get_movie(movie_id)
    if movie1 is None:
        raise NonExistentMovieException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create review and add to user's list of reviews
    review = Review(movie1, review_text, rating)
    user.add_review(review)

    # Movie has a dict of reviews, key = movie and value is a list of users who have written a review
    # Update the repository.
    repo.add_review(user, review)


def get_movie(movie_id: str, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):

    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):

    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_list_of_movies_by_year(year, repo: AbstractRepository):
    # Returns movies for the target date (empty if no matches),
    # the date of the previous movie (might be null),
    # the date of the next movie (might be null)

    movies = repo.get_list_of_movies_by_year(year)

    movies_dto = list()
    prev_year = next_year = None

    if len(movies) > 0:
        prev_year = repo.get_previous_year(movies[0])
        next_year = repo.get_next_year(movies[0])

        # Convert Movies to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_year, next_year


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert Movies to dictionary form.
    #movies_as_dict = movies_to_dict(movies)

    return movies


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    # Have to retrieve user list of reviews and then see what reviews match with the movie title.
    movie = repo.get_reviews_by_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.review)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'title': movie.title,
        'year': movie.movie_date,
        'genres': movie.genres,
        'actors': movie.actors,
        'director': movie.director,
        'description' : movie.description,
        'runtime': movie.runtime_minutes,
        #'image_hyperlink': movie.image_hyperlink,
        'review': reviews_to_dict(movie.review)
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'username': review.user.user_name,
        'article_id': review.movie.id,
        'comment_text': review.comment,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]

"""
def tag_to_dict(tag: Tag):
    tag_dict = {
        'name': tag.tag_name,
        'tagged_articles': [article.id for article in tag.tagged_articles]
    }
    return tag_dict


def tags_to_dict(tags: Iterable[Tag]):
    return [tag_to_dict(tag) for tag in tags]

"""
# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(dict):
    movie = Movie(dict.title, dict.year)
    movie.genres = dict.genres
    movie.actors = dict.actors
    movie.director = dict.director
    movie.description = dict.description
    movie.runtime_minutes = dict.runtime
    # Note there's no comments or tags.
    return movie