from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange, InputRequired

import adapters.repository as repo
import utilities.utilities as utilities
import movies.services as services

# Configure Blueprint.
from authentication.authentication import login_required

movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/retrieve_movie', methods=['GET'])
def retrieve_movie():
    # Read query parameters.
    target_id = request.args.get('target_id')
    movie_to_show_reviews = request.args.get('view_review_for')

    # Fetch the first and last movies in the series - dict.
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_id is None:
        # No title query parameter, so return first movie.
        target_id = first_movie['movie_id']

    # need to fetch previous and next
    next_movie = services.get_next_movie(target_id, repo.repo_instance)
    previous_movie = services.get_previous_movie(target_id, repo.repo_instance)

    # Retrieve a movie object that named with target_title ==> should just be one movie
    movie = [services.get_movie(target_id, repo.repo_instance)]

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if previous_movie is not None:
        # There are articles on a previous date, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.retrieve_movie', target_id=previous_movie['movie_id'])
        first_movie_url = url_for('movies_bp.retrieve_movie', target_id=first_movie['movie_id'])

        # There are articles on a subsequent date, so generate URLs for the 'next' and 'last' navigation buttons.
    if next_movie is not None:
        next_movie_url = url_for('movies_bp.retrieve_movie', target_id=next_movie['movie_id'])
        last_movie_url = url_for('movies_bp.retrieve_movie', target_id=last_movie['movie_id'])

    # construct urls for viewing movie comments
    movie[0]['view_review_url'] = url_for('movies_bp.retrieve_movie', target_id=target_id, view_reviews_for=target_id)
    movie[0]['add_review_url'] = url_for('movies_bp.movie_review', target_id=target_id)

    # Generate the webpage to display the movies.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies=movie,
        genre_urls=utilities.get_genre_urls(),
        director_url=utilities.get_director_urls(),
        actor_urls=utilities.get_actor_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        next_movie_url=next_movie_url,
        prev_movie_url=prev_movie_url,
        show_reviews_for_movie=movie_to_show_reviews
    )


@movies_blueprint.route('/movies_by_year', methods=['GET'])
def movies_by_year():
    pass


@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    movies_per_page = 3

    # read query parameters
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')

    if genre_name is None:
        genre_name = 'Action'

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    # retrieve a list of movie_ids with chosen genre
    target_ids = services.get_movie_ids_by_genre(genre_name, repo.repo_instance)

    # retrieve batch of movie objects to display on the web page - 3 at a time
    movies = services.get_movies_by_id(target_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    # generate urls for next/prev/etc
    if cursor > 0:
        prev_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name)

    if cursor + movies_per_page < len(target_ids):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(target_ids) / movies_per_page)
        if len(target_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=last_cursor)



    # Generate the webpage to display the movies.
    # display Genre at the top and then a list of movies and movie details  - title,year,descri,acto,directors,runtime
    # have to add what needs to be on nav bar
    # have to add next and prev buttons
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Movies by Genre: ' + genre_name,
        movies=movies,
        genre_urls=utilities.get_genre_urls(),
        director_url=utilities.get_director_urls(),
        actor_urls=utilities.get_actor_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
    )


@movies_blueprint.route('/movies_by_director', methods=['GET'])
def movies_by_director():
    # read query parameters
    director_name = request.args.get('director')

    # retrieve first, last.
    first_director = services.get_first_director(repo.repo_instance)
    print("FIRST", first_director)
    last_director = services.get_last_director(repo.repo_instance)

    if director_name is None:
        director_name = first_director

    # retrieve a list of movie_ids with chosen director
    target_ids = services.get_movie_ids_by_director(director_name, repo.repo_instance)
    print('target', target_ids)

    # retrieve batch of movie objects to display on the web page - all by same director
    movies = services.get_movies_by_id(target_ids, repo.repo_instance)


    prev_director = services.get_prev_director(director_name, repo.repo_instance)
    next_director = services.get_next_director(director_name, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None


    if len(movies) > 0:
        if prev_director is not None:
            prev_movie_url = url_for('movies_bp.movies_by_director', director=prev_director)
            first_movie_url = url_for('movies_bp.movies_by_director', director=first_director)

        if next_director is not None:
            next_movie_url = url_for('movies_bp.movies_by_director', director=next_director)
            last_movie_url = url_for('movies_bp.movies_by_director', director=last_director)

        # Generate the webpage to display the movies.
        return render_template(
            'movies/movies.html',
            title='Movies',
            movies_title='Movies by Director: ' + director_name,
            movies=movies,
            genre_urls=utilities.get_genre_urls(),
            director_url=utilities.get_director_urls(),
            actor_urls=utilities.get_actor_urls(),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url
        )

    # No articles to show, so return the homepage.
    return redirect(url_for('home_bp.home'))


@movies_blueprint.route('/movies_by_actor', methods=['GET'])
def movies_by_actor():
    # read query parameters
    actor_name = request.args.get('actor')

    # retrieve first, last.
    first_actor = services.get_first_actor(repo.repo_instance)
    last_actor = services.get_last_actor(repo.repo_instance)

    if actor_name is None:
        actor_name = first_actor

    # retrieve a list of movie_ids with chosen director
    target_ids = services.get_movie_ids_by_actor(actor_name, repo.repo_instance)

    # retrieve batch of movie objects to display on the web page - all by same director
    movies = services.get_movies_by_id(target_ids, repo.repo_instance)

    prev_actor = services.get_prev_actor(actor_name, repo.repo_instance)
    next_actor = services.get_next_actor(actor_name, repo.repo_instance)
    print("prev", prev_actor, 'next', next_actor)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies) > 0:
        if prev_actor is not None:
            prev_movie_url = url_for('movies_bp.movies_by_actor', actor=prev_actor)
            first_movie_url = url_for('movies_bp.movies_by_actor', actor=first_actor)

        if next_actor is not None:
            next_movie_url = url_for('movies_bp.movies_by_actor', actor=next_actor)
            last_movie_url = url_for('movies_bp.movies_by_actor', actor=last_actor)

        # Generate the webpage to display the movies.
        return render_template(
            'movies/movies.html',
            title='Movies',
            movies_title='Movies by Actor: ' + actor_name,
            movies=movies,
            genre_urls=utilities.get_genre_urls(),
            director_url=utilities.get_director_urls(),
            actor_urls=utilities.get_actor_urls(),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url
        )

    # No articles to show, so return the homepage.
    return redirect(url_for('home_bp.home'))


@movies_blueprint.route('/movies_by_rating', methods=['GET'])
def movies_by_rating():
    pass


@movies_blueprint.route('/movies_in_watchlist', methods=['GET'])
def movies_in_watchlist():
    pass


@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def movie_review():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        movie_id = form.movie_id.data
        rating = form.rating.data

        # Use the service layer to store the new comment.
        services.add_review(movie_id, form.review.data, username, rating, repo.repo_instance)

        # Retrieve the article in dict form.
        movie = services.get_movie(movie_id, repo.repo_instance)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('movie_bp.retrieve_movie', target_id=movie['movie_id'], view_comments_for=movie_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        movie_id = request.args.get('movie')

        # Store the article id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        movie_id = form.movie_id.data

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    movie = services.get_movie(movie_id, repo.repo_instance)
    return render_template(
        'news/comment_on_article.html',
        title='Edit article',
        movie=movie,
        form=form,
        handler_url=url_for('movie_bp.movie_review'),
        genre_urls=utilities.get_genre_urls(),
        director_url=utilities.get_director_urls(),
        actor_urls=utilities.get_actor_urls(),
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    rating = IntegerField('Rating', [InputRequired("Please enter a rating from 0 to 10"),
                                     NumberRange(min=1, max=10)
                                     ])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')
