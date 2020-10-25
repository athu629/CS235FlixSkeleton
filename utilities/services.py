from typing import Iterable
import random

from adapters.repository import AbstractRepository
from domainmodel.movie import Movie


def get_first_movie(repo: AbstractRepository):
    movie = [repo.get_first_movie()]
    return movies_to_dict(movie)


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_unique_genre_list()
    genre_names = [genre.genre_name for genre in genres]
    return genre_names


def get_director_names(repo: AbstractRepository):
    directors = repo.get_unique_director_list()
    director_names = [director.director_full_name for director in directors]
    return director_names


def get_actor_names(repo: AbstractRepository):
    actors = repo.get_unique_actor_list()
    actor_names = [actor.actor_full_name for actor in actors]
    return actor_names


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids/keys to generate if the repository has an insufficient number of movies.
        quantity = movie_count - 1

    if quantity == 1:
        movies = [repo.get_first_movie()]
    else:
        # Pick distinct and random movie.
        random_ids = random.sample(range(1, movie_count), quantity)
        movies = repo.get_movies_by_id(random_ids)

    return movies_to_dict(movies)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'title': movie.title,
        'year': movie.movie_date,
        'description': movie.description,
        'actors': movie.actors,
        'director': movie.director,
        'genres': movie.genres,
        'runtime': movie.runtime_minutes
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
