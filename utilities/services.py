from typing import Iterable
import random

from adapters.repository import AbstractRepository
from domainmodel.movie import Movie

"""
def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genre()
    genre_names = [genre.genre_name for genre in genres]

    return genre_names
"""

def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids/keys to generate if the repository has an insufficient number of movies.
        quantity = movie_count - 1

    # Pick distinct and random movie.
    random_ids = random.sample(range(1, movie_count), quantity)
    print("RAND", random_ids)
    movies = repo.get_movies_by_id(random_ids)

    return movies_to_dict(movies)

# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'title': movie.title,
        'year': movie.movie_date
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]