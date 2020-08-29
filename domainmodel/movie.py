from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director

class Movie:

    def __init__(self, title: str, movie_date: int):
        if title == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()
        if movie_date < 1900 or movie_date == "":
            self.__movie_date = None
        else:
            self.__movie_date = movie_date.strip()
        self.__description = None
        self.__director = None
        self.actors = None
        self.genres = None
        self.runtime_minutes = None
        self.actor_list = []
        self.genre_list = []

    @property
    def title(self) -> str:
        return self.title

    def movie_date(self) -> int:
        return self.movie_date

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__movie_date}>"

    def __eq__(self, other):
        return self.__title == other.__title and self.__movie_date == other.__movie_date

    def __lt__(self, other):
        return self.__title < other.__title and self.__movie_date < other.__movie_date

    def __hash__(self):
        return hash(self.__title, self.__movie_date)

    def add_actor(self, actor):
        self.actor_list.append(actor)

    def remove_actor(self, actor):
        if actor in self.actor_list:
            self.actor_list.remove(actor)
        else:
            pass

    def add_genre(self, genre):
        self.genre_list.append(genre)

    def remove_genre(self, genre):
        if genre in self.genre_list:
            self.genre_list.remove(genre)
        else:
            pass