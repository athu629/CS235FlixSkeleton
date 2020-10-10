from bisect import insort_left, bisect_left
import csv
import os
from werkzeug.security import generate_password_hash

from adapters.repository import AbstractRepository, RepositoryException
from domainmodel.movie import Movie
from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.review import Review
from domainmodel.user import User
from domainmodel.watchlist import WatchList
from datafilereaders.movie_file_csv_reader import MovieFileCSVReader

class MemoryRepository(AbstractRepository):
    # Movies ordered by title, not date, combination of title and date is assumed unique.

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()
        self._users = list()
        self._reviews = list()
        # dict of movie object with list of review objects - rview object has movie;text;rating, user object has a list of reviews
        self._movie_review_list = dict()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        for user in self._users:
            if user.user_name == username:
                return user
        return None

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        key = str(movie.title) + str(movie.movie_date)
        self._movies_index[key] = movie

    def get_movie(self, movie_id: str) -> Movie:
        movie = None
        try:
            print("HEY",movie_id)
            movie = self._movies_index[movie_id]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def get_number_of_movies(self):
        return len(self._movies)

    def get_first_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_movies_by_id(self, id_list):
        existing_ids = []
        for id in id_list:
            if id in self._movies_index:
                existing_ids.append(id)
        movies = []
        for id2 in existing_ids:
            movies = self._movies_index[id2]

        # Return a list of Movie objects
        return movies

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        key = str(movie.title) + str(movie.movie_date)
        index = bisect_left(self._movies, key)
        if index != len(self._movies) and self._movies[index].title == movie.title:
            return index
        raise ValueError

    def get_previous_movie(self, movie: Movie):
        previous_movie = None

        try:
            for i in range(len(self._movies)):
                if movie == self._movies[i]:
                    if i > 0:
                        previous_movie = self._movies[i - 1]
                        break
                    elif i == 0:
                        previous_movie = self._movies[len(self._movies)-1]
                        break
        except ValueError:
            # No subsequent movies, so return None.
            pass

        return previous_movie

    def get_next_movie(self, movie: Movie):
        next_movie = None

        try:
            for i in range(len(self._movies)):
                if movie == self._movies[i]:
                    if i == len(self._movies) - 1:
                        next_movie = self._movies[0]
                        break
                    elif i < len(self._movies):
                        next_movie = self._movies[i + 1]
                        break
        except ValueError:
            # No subsequent movies, so return None.
            pass

        return next_movie

    def get_previous_year(self, movie: Movie):
        previous_movie_year = None

        try:
            previous_movie_year = movie.movie_date - 1
        except ValueError:
            # No subsequent movies, so return None.
            pass

        return previous_movie_year

    def get_next_year(self, movie: Movie):
        next_movie_year = None

        try:
            next_movie_year = movie.movie_date + 1
        except ValueError:
            # No subsequent movies, so return None.
            pass

        return next_movie_year

    def get_list_of_movies_by_title(self, title_list):
        list1 = []

        for movie in self._movies:
            if movie.title in title_list:
                list1.append(movie)
        return list1

    def get_list_of_movies_by_year(self, year):
        list2 = []

        for movie in self._movies:
            if movie.movie_date == year and movie not in list2:
                list2.append(movie)
        if len(list2) == 0:
            list2 = None
        return list2

    def get_list_of_movies_by_actor(self, actor: Actor):
        # returns a list of movies with chosen actor
        list3 = []

        for movie in self._movies:
            for a in movie.actors:
                if actor == a and movie not in list3:
                    list3.append(movie)

        return list3

    def get_list_of_movies_by_director(self, director: Director):
        # returns a list of movies with chosen director
        list4 = []

        for movie in self._movies:
            if movie.director == director and movie not in list4:
                    list4.append(movie)

        return list4

    def get_list_of_movies_by_genre(self, genre: Genre):
        # returns a list of movies with chosen genre
        list5 = []
        print(genre)
        for movie in self._movies:
            for g in movie.genres:
                if genre == g and movie not in list5:
                    list5.append(movie)

        return list5

    def add_review(self, user: User, review: Review):
        super().add_review(user, review)
        for u in self._users:
            if u == user:
                # link review and user - review and move already linked
                user.add_review(review)
                self._reviews.append(review)
                # add review to movie_review_list - link movies to users - dict of movies with list of users who have made reviews
                if review.movie not in self._movie_review_list:
                    self._movie_review_list[review.movie] = [user]
                else:
                    list1 = self._movie_review_list[review.movie]
                    list1.append(user)
                    self._movie_review_list[review.movie] = list1

    def get_reviews_by_movie(self, movie: Movie):
        # Returns list of Review obj movie: [Reviw(), ..., review()]
        review_list = []
        for k in self._movie_review_list:
            if k == movie:
                list_users = self._movie_review_list[k]
                for u in list_users:
                    for r in u.reviews:
                        if r.movie == movie:
                            review_list.append(r)
        return review_list

    def get_reviews_by_user(self, user):
        # Returns list of Review obj [Reviw(), ..., review()]
        # users have a list of review objects which have the movie
        return user.reviews

def read_other_csv_file(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row

def load_movies(data_path: str, repo: MemoryRepository):
    path = os.path.join(data_path, 'test_movies.csv')
    movie_file_reader = MovieFileCSVReader(path)
    movie_file_reader.read_csv_file()

    for movie in movie_file_reader.dataset_of_movies:
        repo.add_movie(movie)

def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_other_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users

def populate(data_path: str, repo: MemoryRepository):
    # Load articles and tags into the repository.
    load_movies(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)