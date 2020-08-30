from datetime import datetime

from domainmodel.movie import Movie

class Review:

    def __init__(self, movie: Movie, review_text: str, rating: int):
        if type(movie) is Movie:
            self._movie = movie
        else:
            self._movie = None
        if type(review_text) is str:
            self._review_text = review_text
        else:
            self._review_text = None
        if type(rating) is int and 1 <= rating <= 10:
            self._rating = rating
        else:
            self._rating = None
        self._timestamp = datetime.now()
        #print("TIME", self._timestamp)

    def __repr__(self):
        return f"<{self._movie.title}, Rating: {self._rating}, Review: {self._review_text}>"

    def __eq__(self, other):
        return self._movie == other._movie \
               and self._review_text == other._review_text \
               and self._rating == other._rating

    @property
    def movie(self) -> Movie:
        return self._movie

    @property
    def review_text(self) -> str:
        return self._review_text

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, value):
        if type(value) is int and 1 <= value <= 10:
            self._rating = value

    @property
    def timestamp(self):
        return self._timestamp

