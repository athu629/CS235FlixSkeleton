from flask import Blueprint, render_template

import utilities.utilities as utilities

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        "home/home.html",
        genre_urls=utilities.get_genre_urls(),
        director_url=utilities.get_director_urls(),
        actor_urls=utilities.get_actor_urls()
    )
    # alphabet_urls=utilities.get_movies_by_title(),
    # director_url=utilities.get_movie_by_director(),
    # actor_url=utilities.get_movie_by_actor(),

# we want the home page to show a title screen - welcoem to movies blah blaj have a collapsable nav bar nav bar - has
# home button, buttons for all genres, and couple of buttons ith alphbets on them, director button, actor button,
# realsie date, runtime minutes

# home blueprint should have the following in render templete
# 1. utilities.get_movie_by_title - alphabet - kinda like get articles by date from COVID web app
# 2. utilities.get_movie by genre
# 3. utilities.get_movie_by director - director button takes to first movie with all movies with director starting with A
# 4.
