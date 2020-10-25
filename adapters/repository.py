import abc
from typing import List
from datetime import date

from domainmodel.movie import Movie
from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.review import Review
from domainmodel.user import User
from domainmodel.watchlist import WatchList

repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):


    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds an Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, movie_id: str) -> Movie:
        """ Returns Movie with title and release date from the repository.

        If there is no Movie with the given title and release date, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self) -> Genre:
        """ Adds genre to the unique genre_list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_unique_genre_list(self) -> List:
        """ Returns list of genres in the repo
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns movie count in repo
                """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns first movie in the repo
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns last movie in the repo
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, movie_list: list) -> Movie:
        """ Returns list of movies """
        raise NotImplementedError

    @abc.abstractmethod
    def get_previous_year(self, movie: Movie):
        """ Returns the year before a movie date"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_year(self, movie: Movie):
        """ Returns the year after a movie date"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_list_of_movies_by_title(self, title: str):
        """ Returns list of movies with matching year"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_list_of_movies_by_year(self, year: int):
        """ Returns list of movies with matching year"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_list_of_movies_by_actor(self, actor: Actor):
        """ Returns list of movies with matching actor"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_list_of_movies_by_director(self, director: Director):
        """ Returns list of movies with matching actor"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_list_of_movies_by_genre(self, genre: Genre):
        """ Returns list of movies with matching actor"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, user: User, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with an Movie and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if user is None:
            raise RepositoryException('User is None')
        if review.movie is None:
            raise RepositoryException('Review not correctly attached to a Movie')

    @abc.abstractmethod
    def get_reviews_by_movie(self, movie: Movie):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_by_user(self, user: User):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_movie(self, movie: Movie):
        """ Returns the next movie repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_previous_movie(self, movie: Movie):
        """ Returns the previous movie repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_by_genre(self, genre_name: object) -> object:
        """ Returns a list of movie_ids """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_by_director(self, director_name: object) -> object:
        """ Returns a list of movie_ids """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_by_actor(self, actor_name: object) -> object:
        """ Returns a list of movie_ids """
        raise NotImplementedError

    @abc.abstractmethod
    def get_unique_director_list(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_unique_actor_list(self):
        raise NotImplementedError




