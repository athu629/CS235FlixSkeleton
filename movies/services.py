from typing import List, Iterable

from adapters.repository import AbstractRepository
# from adapters.memory_repository import
from domainmodel.movie import Movie
from domainmodel.genre import Genre
from domainmodel.review import Review
from domainmodel.director import Director
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

    # Movie has a dict of reviews, key = movie and value is a list of users who have written a review, also a list of review objects in repo
    # Update the repository.
    repo.add_review(user, review)


def get_movie(movie_id: str, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_movies_by_genre(genre, repo: AbstractRepository):
    # retrieve list of movies with matching genre
    movies = repo.get_list_of_movies_by_genre(genre)
    return movies_to_dict(movies)


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_first_movie()
    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):
    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_next_movie(movie: str, repo: AbstractRepository):
    m = repo.get_movie(movie)  # turns into a movie object
    next_movie = repo.get_next_movie(m)  # get the enxt movie object
    return movie_to_dict(next_movie)  # converts to dict


def get_previous_movie(movie: str, repo: AbstractRepository):
    m = repo.get_movie(movie)
    prev_movie = repo.get_previous_movie(m)
    return movie_to_dict(prev_movie)


def get_list_of_movies_by_year(year, repo: AbstractRepository):
    # Returns movies for the target date (empty if no matches),
    # the date of the previous movie (might be null),
    # the date of the next movie (might be null)

    movies = repo.get_list_of_movies_by_year(year)

    movies_dto = list()
    prev_year = next_year = None

    if movies is not None and len(movies) > 0 and 1800 < year < 2021:
        prev_year = repo.get_previous_year(movies[0])
        next_year = repo.get_next_year(movies[0])

        # Convert Movies to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_year, next_year


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert Movies to dictionary form.
    # movies_as_dict = movies_to_dict(movies)
    # returns a list
    return movies_to_dict(movies)


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    # Have to retrieve user list of reviews and then see what reviews match with the movie title.
    movie = repo.get_movie(movie_id)

    # ist of review objects for movie
    reviews_for_movie = repo.get_reviews_by_movie(movie)

    if movie is None:
        raise NonExistentMovieException

    if len(reviews_for_movie) > 0:
        return reviews_to_dict(reviews_for_movie)
    else:
        return []


def get_genre_index(genre_name, repo: AbstractRepository):
    g = Genre(genre_name)
    g_list = repo.get_unique_genre_list()
    index = g_list.index(g)
    return index


def get_genre_by_index(index: int, repo: AbstractRepository):
    # returns genre object
    g_list = repo.get_unique_genre_list()
    return g_list[index]


def get_unique_genre_list(repo: AbstractRepository):
    return repo.get_unique_genre_list()


def get_movie_ids_by_genre(genre_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_by_genre(genre_name)
    return movie_ids


def get_movie_ids_by_director(director_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_by_director(director_name)
    return movie_ids


def get_movie_ids_by_actor(actor_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_by_actor(actor_name)
    return movie_ids


def get_first_director(repo: AbstractRepository):
    d = repo.get_unique_director_list()[0]
    return d.director_full_name


def get_last_director(repo: AbstractRepository):
    d = repo.get_unique_director_list()[-1]
    return d.director_full_name


def get_next_director(director_name: str, repo: AbstractRepository):
    d_list = repo.get_unique_director_list()
    for i in range(len(d_list)):
        if d_list[i].director_full_name == director_name and i != len(d_list) - 1:
            return d_list[i + 1].director_full_name


def get_prev_director(director_name: str, repo: AbstractRepository):
    d_list = repo.get_unique_director_list()
    for i in range(len(d_list)):
        if d_list[i].director_full_name == director_name and i != 0:
            return d_list[i - 1].director_full_name


def get_first_actor(repo: AbstractRepository):
    a = repo.get_unique_actor_list()[0]
    return a.actor_full_name


def get_last_actor(repo: AbstractRepository):
    a = repo.get_unique_actor_list()[-1]
    return a.actor_full_name


def get_next_actor(actor_name: str, repo: AbstractRepository):
    a_list = repo.get_unique_actor_list()
    for i in range(len(a_list)):
        if a_list[i].actor_full_name == actor_name and i != len(a_list) - 1:
            return a_list[i + 1].actor_full_name


def get_prev_actor(actor_name: str, repo: AbstractRepository):
    a_list = repo.get_unique_actor_list()
    for i in range(len(a_list)):
        if a_list[i].actor_full_name == actor_name and i != 0:
            return a_list[i - 1].actor_full_name


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'movie_id': str(movie.title) + str(movie.movie_date),
        'title': movie.title,
        'year': movie.movie_date,
        'genres': movie.genres,
        'actors': movie.actors,
        'director': movie.director,
        'description': movie.description,
        'runtime': movie.runtime_minutes
        #'review': get_reviews_for_movie()
        # 'image_hyperlink': movie.image_hyperlink,
    }

    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'movie_title': review.movie.title,
        'movie_year': review.movie.movie_date,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    list1 = []
    for r in reviews:
        list1 = list1 + [review_to_dict(r)]
    return list1


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
