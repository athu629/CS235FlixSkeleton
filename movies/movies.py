from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import adapters.repository as repo
import utilities.utilities as utilities
import movies.services as services


# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/movies_by_title', methods=['GET'])
def movies_by_title():
    # Read query parameters.
    target_title = request.args.get('title')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    # Fetch the first and last movies in the series.
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_title is None:
        # No date query parameter, so return articles from day 1 of the series.
        target_title = first_movie['title']


    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    # Fetch movie(s) for the target year. This call also returns the previous and next year for movies immediately
    # before and after the target year.
    movies, previous_year, next_year = services.get_movies_by_title(target_title, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies) > 0:
        # There's at least one article for the target date.
        if previous_year is not None:
            # There are articles on a previous date, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_movie_url = url_for('movies_bp.movies_by_year')
            first_movie_url = url_for('movies_bp.movies_by_year')

        # There are articles on a subsequent date, so generate URLs for the 'next' and 'last' navigation buttons.
        if next_year is not None:
            next_movie_url = url_for('movies_bp.movies_by_year')
            last_movie_url = url_for('movies_bp.movies_by_year')

        # Construct urls for viewing movie reviews and adding reviews.
        for movie in movies:
            movie['view_review_url'] = url_for('movies_bp.movies_by_year', view_reviews_for=movie['title'])
            movie['add_review_url'] = url_for('movies_bp.movie_review', movie=movie['title'])

        # Generate the webpage to display the movies.
        return render_template(
            'movies/movies.html',
            title='Movies',
            movies_title=target_title,
            movies=movies,
            selected_movies=utilities.get_selected_movies(len(movies) * 2),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url,
            show_reviews_for_movie=movie_to_show_reviews
        )

    # No articles to show, so return the homepage.
    return redirect(url_for('home_bp.home'))