import pytest

from movies.models import Movie


# Follows the 'Factory as Fixture' pattern, which is used to pass a function as fixture.
# This function can be used multiple times in a test to generate data,
# as well as having benefits of a normal fixture such as yield, teardown, combining other fixtures etc.
@pytest.fixture(scope="function")
def add_movie():
    def _add_movie(title, genre, year):
        movie = Movie.objects.create(title=title, genre=genre, year=year)
        return movie

    return _add_movie
