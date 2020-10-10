from datetime import date

import pytest

#from covid.authentication.services import AuthenticationException
from movies import services as movie_services
#from covid.authentication import services as auth_services
from movies.services import NonExistentMovieException

def test_can_add_comment(in_memory_repo):
    movie_id = "The Great Wall2016"
    review_text = "So Good!"
    user_name = "fmercury"
    rating = 8

    # Call the movie.service layer to add the review
    movie_services.add_review(movie_id, review_text, user_name, rating)

    # retrieve the review for the movie from the repo
    reviews_as_dict = movie_services.get_reviews_for_movie(movie_id)