import json

from flask import Blueprint, abort, request
from flask_cors import cross_origin
from sqlalchemy import exc

from shared.auth import requires_auth
from shared.common import *
from shared.models import Movie

movies_blueprint = Blueprint('movies', __name__)


# region movies


@movies_blueprint.route('/', methods=['GET'])
def get_movies_list():
    movies = [movie.format() for movie in Movie.query.order_by(Movie.name).all()]
    return get_success_response(movies) if movies else get_fail_response(404, 'no data found')


@movies_blueprint.route('/names', methods=['GET'])
def get_movies_names_list():
    movies = [{'id': movie.id, 'name': movie.name} for movie in Movie.query.order_by(Movie.name).all()]
    return get_success_response(movies) if movies else get_fail_response(404, 'no data found')


@movies_blueprint.route('/<int:movie_id>', methods=["GET"])
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    return get_success_response(movie.format()) if movie else get_fail_response(404, f"movie with id: {movie_id} not found")


@movies_blueprint.route('/<int:movie_id>', methods=['DELETE'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('delete:movies')
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404, f"movie with id: {movie_id} not found")
    movie.delete()
    return get_success_response(
        data=None,
        msg=f"movie with id: {movie_id} deleted successfully"
    )


@movies_blueprint.route('/new', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('add:movies')
def add_movie():
    try:
        movie = load_and_validate_movie_data('new')
        movie.insert()
        return get_success_response(movie.format(), 'Movie inserted successfully')
    except exc.SQLAlchemyError as err:
        abort(500, err)


@movies_blueprint.route('/edit/<int:movie_id>', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('modify:movies')
def edit_movie(movie_id):
    try:
        movie = load_and_validate_movie_data('edit', movie_id)
        movie.update()
        return get_success_response(movie.format(), 'Movie updated successfully')
    except exc.SQLAlchemyError as err:
        abort(500, err)


def load_and_validate_movie_data(mode='new', movie_id=None):
    data = json.loads(request.data) if request.data else abort(400, f'data not valid')
    if not data:
        abort(400, 'no data to update')
    movie = Movie.query.get(movie_id) if mode == 'edit' else Movie()
    if not movie and mode == 'edit':
        abort(404, f"artist with id: {movie_id} not found")
    movie.load(data)
    movie.id = movie_id if mode == 'edit' else None
    validation = movie.validate()
    if not validation.get('is_valid'):
        abort(400, f'data not valid {validation.get("errors")}')
    return movie

# endregion movies
