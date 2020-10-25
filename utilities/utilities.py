from flask import Blueprint, request, render_template, redirect, url_for, session

import adapters.repository as repo
import utilities.services as services

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_movies_by_title():
    # returns url to movie title starting with a digit or letter A
    pass


def get_genre_urls():
    # returns urls for all genres to display on navigation dropdown
    genre_names = services.get_genre_names(repo.repo_instance)
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('movies_bp.movies_by_genre', genre=genre_name)

    return genre_urls


def get_director_urls():
    # return url to movie with director at the start of the alphabet
    director_names = services.get_director_names(repo.repo_instance)
    director_urls = dict()
    for director_name in director_names:
        director_urls[director_name] = url_for('movies_bp.movies_by_director', director=director_name)

    return director_urls


def get_actor_urls():
    # return url to movie with actor at the stat of the alphabet
    actor_names = services.get_actor_names(repo.repo_instance)
    actor_urls = dict()
    for actor_name in actor_names:
        actor_urls[actor_name] = url_for('movies_bp.movies_by_actor', actor=actor_name)

    return actor_urls

# get selected movies by title?year?actor?genre?
