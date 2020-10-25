import os
import pytest

from adapters.repository import RepositoryException
from cs235init import create_app
from adapters import memory_repository
from adapters.memory_repository import MemoryRepository, populate
from domainmodel.movie import Movie
from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.review import Review
from domainmodel.user import User
from domainmodel.watchlist import WatchList


TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'Alyssa', 'Documents', 'UOA', 'Uni 2020',
                        'CS235', 'CS235_A1', 'CS235FlixSkeleton', 'datafiles')

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='thorke', password='cLQ^C#oFXloS'):
        return self._client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
