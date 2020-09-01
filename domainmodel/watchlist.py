from domainmodel.movie import Movie

class WatchList:

    def __init__(self):
        self._watch_list = []
        self._ptr = 0

    def add_movie(self, movie: Movie):
        if type(movie) is Movie and movie not in self._watch_list:
            self._watch_list.append(movie)

    def remove_movie(self, movie: Movie):
        if type(movie) is Movie and movie in self._watch_list:
            self._watch_list.remove(movie)

    def __repr__(self):
        if len(self._watch_list) == 0:
            return f"You have no movies saved in your watchlist."
        else:
            string = "Watchlist:\n"
            for x in range(len(self._watch_list)):
                if x == len(self._watch_list) - 1:
                    y = str(x + 1) + " : " + str(self._watch_list[x])
                else:
                    y = str(x+1) + " : " + str(self._watch_list[x]) + "\n"
                string = string + y
            return f"{string}"

    def __eq__(self, other):
        l1 = self._watch_list
        l1.sort()
        l2 = other._watch_list
        l2.sort()
        return l1 == l2

    def select_movie_to_watch(self, index):
        if type(index) is int and 0 <= index < len(self._watch_list):
            return self._watch_list[index]
        elif index < 0 or index >= len(self._watch_list):
            return None

    def size(self):
        return len(self._watch_list)

    def first_movie_in_watchlist(self):
        if len(self._watch_list) > 0:
            return self._watch_list[0]
        elif len(self._watch_list) == 0:
            return None

    def __iter__(self):
        self._ptr = 0
        return self

    def __next__(self):
        if self._ptr == len(self._watch_list):
            raise StopIteration
        s = self._watch_list[self._ptr]
        self._ptr += 1
        return s

    @property
    def watch_list(self):
        return self._watch_list