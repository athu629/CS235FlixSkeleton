import csv

from domainmodel.movie import Movie
from domainmodel.actor import Actor
from domainmodel.genre import Genre
from domainmodel.director import Director


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self._dataset_of_movies = []
        self._dataset_of_actors = []
        self._dataset_of_directors = []
        self._dataset_of_genres = []

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as isfile:
            movie_file_reader = csv.DictReader(isfile)

            index = 0
            for row in movie_file_reader:
                # title = row['Title']
                # release_year = int(row['Year'])
                # print(f"Movie {index} with title: {title}, release year {release_year}")
                # print("HHH", row['Genre'], row['Director'], row['Actors'])

                t = row['Title']
                y = int(row['Year'])
                r = int(row['Runtime (Minutes)'])
                des = row['Description']
                movie = Movie(t, y)
                if movie not in self.dataset_of_movies:
                    movie.runtime_minutes = r
                    movie.description = des
                    self.dataset_of_movies.append(movie)

                actors = row['Actors'].split(",")
                for a in actors:
                    act = Actor(a)
                    movie.add_actor(act)
                    if act not in self.dataset_of_actors:
                        self.dataset_of_actors.append(act)

                director = Director(row['Director'])
                movie.director = director
                if director not in self.dataset_of_directors:
                    self.dataset_of_directors.append(director)

                genres = row['Genre'].split(",")
                for g in genres:
                    gen = Genre(g)
                    movie.add_genre(gen)
                    if gen not in self.dataset_of_genres:
                        self.dataset_of_genres.append(gen)

                index += 1
        """
        print("M", len(self.dataset_of_movies),self.dataset_of_movies)
        print("A", len(self.dataset_of_actors),self.dataset_of_actors)
        print("D", len(self.dataset_of_directors),self.dataset_of_directors)
        print("G", len(self.dataset_of_genres),self.dataset_of_genres)
        """

    @property
    def dataset_of_movies(self) -> list:
        return self._dataset_of_movies

    @property
    def dataset_of_actors(self) -> list:
        return self._dataset_of_actors

    @property
    def dataset_of_directors(self) -> list:
        return self._dataset_of_directors

    @property
    def dataset_of_genres(self) -> list:
        return self._dataset_of_genres
