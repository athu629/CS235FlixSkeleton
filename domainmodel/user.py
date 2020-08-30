from domainmodel.movie import Movie
from domainmodel.review import Review

class User:

    def __init__(self, user_name: str, password: str):
        if type(user_name) is str:
            self._user_name = user_name.strip().lower()
        else: self._user_name = None
        if type(password) is str:
            self._password = password
        else:
            self._password = None
        self._watched_movies = []
        self._reviews = []
        self._time_spent_watching_movies_minutes: int = 0

    def __repr__(self):
        return f"<User {self._user_name}>"

    def __eq__(self, other):
        return self._user_name == other._user_name

    def __lt__(self, other):
        return self._user_name < other._user_name

    def __hash__(self):
        return hash(self._user_name)

    def watch_movie(self, movie):
        if type(movie) is Movie and movie not in self._watched_movies:
            self._watched_movies.append(movie)
            self._time_spent_watching_movies_minutes = self._time_spent_watching_movies_minutes + movie.runtime_minutes

    def add_review(self, review):
        if type(review) is Review and review not in self._reviews:
            self._reviews.append(review)

    @property
    def user_name(self):
        return self._user_name

    @property
    def password(self):
        return self._password

    @property
    def watched_movies(self):
        return self._watched_movies

    @property
    def reviews(self):
        return self._reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self._time_spent_watching_movies_minutes