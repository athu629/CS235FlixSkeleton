from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director

class Movie:

    def __init__(self, title: str, movie_date: int):
        if type(title) is str and title.strip() != "":
            self.__title = title.strip()
        else:
            self.__title = None

        if (type(movie_date) is int) and movie_date >= 1900:
            self.__movie_date = movie_date
        else:
            self.__movie_date = None

        self._description: str = None
        self._director: Director = None
        self._actors: list = []
        self._genres: list = []
        self._runtime_minutes: int = None

    @property
    def title(self) -> str:
        return self.__title

    @property
    def movie_date(self) -> int:
        return self.__movie_date

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value):
        if type(value) is str:
            self._description = value.strip()
        else:
            self._description = None

    @property
    def director(self) -> Director:
        return self._director

    @director.setter
    def director(self, d):
        if type(d) is Director:
            self._director = d

    @property
    def actors(self) -> list:
        return self._actors

    @actors.setter
    def actors(self, value):
        if type(value) is list:
            for x in value:
                if type(x) is not Actor:
                    self._actors = []
                    return
            self._actors = value
        else:
            self._actors = []

    @property
    def genres(self) -> list:
        return self._genres

    @genres.setter
    def genres(self, value):
        if type(value) is list:
            for x in value:
                if type(x) is not Genre:
                    self._genres = []
                    return
            self._genres = value
        else:
            self._genres = []

    @property
    def runtime_minutes(self) -> int:
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, value):
        if type(value) is int:
            if value > 0:
                self._runtime_minutes = value
            else:
                raise ValueError

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__movie_date}>"

    def __eq__(self, other):
        string1 = self.__title + str(self.__movie_date)
        string2 = other.__title + str(other.__movie_date)
        return string1 == string2

    def __lt__(self, other):
        string1 = self.__title + str(self.__movie_date)
        string2 = other.__title + str(other.__movie_date)
        return string1 < string2

    def __hash__(self):
        string1 = self.__title + str(self.__movie_date)
        return hash(string1)

    def add_actor(self, actor):
        if type(actor) is Actor:
            self.actors.append(actor)

    def remove_actor(self, actor):
        if type(actor) is Actor and actor in self.actors:
            self.actors.remove(actor)

    def add_genre(self, genre):
        if type(genre) is Genre:
            self.genres.append(genre)

    def remove_genre(self, genre):
        if type(genre) is Genre and genre in self.genres:
            self.genres.remove(genre)
