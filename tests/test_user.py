from domainmodel.user import User
from domainmodel.movie import Movie
from domainmodel.review import Review


def test_init():
    user1 = User('Martin', 'pw12345')
    # user2 = User('Ian', 'pw67890')
    # user3 = User('Daniel', 'pw87465')
    assert repr(user1) == "<User martin>"
    movie = Movie("Moana", 2016)
    movie.runtime_minutes = 150
    review_text = "This movie was very enjoyable."
    rating = 8
    review = Review(movie, review_text, rating)
    user1.watch_movie(movie)
    assert repr(user1.watched_movies) == "[<Movie Moana, 2016>]"
    user1.add_review(review)
    assert repr(user1.reviews) == "[<Moana, Rating: 8, Review: This movie was very enjoyable.>]"
    assert user1.time_spent_watching_movies_minutes == 150
