"""Initialize Flask app."""

import os

from flask import Flask

import adapters.repository as repo
from adapters.memory_repository import MemoryRepository, populate


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = os.path.join('C:', os.sep, 'Users', 'Alyssa', 'Documents', 'UOA', 'Uni 2020',
                        'CS235', 'CS235_A1', 'CS235FlixSkeleton', 'datafiles')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from home.home import home_blueprint
        app.register_blueprint(home_blueprint)

        from movies.movies import movies_blueprint
        app.register_blueprint(movies_blueprint)

        from utilities.utilities import utilities_blueprint
        app.register_blueprint(utilities_blueprint)

    return app
