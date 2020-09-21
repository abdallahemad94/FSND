import json

from flask import Blueprint, abort, request
from flask_cors import cross_origin
from sqlalchemy import exc

from shared.auth import requires_auth as authorize
from shared.common import get_success_response, get_fail_response
from shared.models import Artist

artists_blueprint = Blueprint('artists', __name__)


# region artists


@artists_blueprint.route('/', methods=['GET'])
def get_all():
    artists = [artist.format()
               for artist in Artist.query.order_by(Artist.name).all()]
    return get_success_response(artists) if artists else\
        get_fail_response(404, 'no data found')


@artists_blueprint.route('/names', methods=['GET'])
def get_artists_names_list():
    artists = [{'id': artist.id, 'name': artist.name}
               for artist in Artist.query.order_by(Artist.name).all()]
    return get_success_response(artists) if artists else\
        get_fail_response(404, 'no data found')


@artists_blueprint.route('/<int:artist_id>', methods=["GET"])
def get_artist(artist_id):
    artist = Artist.query.get(artist_id)
    return get_success_response(artist.format()) if artist else\
        get_fail_response(404, f"artist with id: {artist_id} not found")


@artists_blueprint.route('/<int:artist_id>', methods=['DELETE'])
@cross_origin(headers=["Content-Type", "Authorization"])
@authorize('delete:artists')
def delete_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if not artist:
        abort(404, f"artist with id: {artist_id} not found")
    artist.delete()
    return get_success_response(
        data=None,
        msg=f"artist with id: {artist_id} deleted successfully"
    )


@artists_blueprint.route('/new', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@authorize('add:artists')
def add_artist():
    try:
        artist = load_and_validate_artist_data('new')
        artist.insert()
        return get_success_response(artist.format(), 'Artist inserted successfully')
    except exc.SQLAlchemyError as err:
        abort(500, err)


@artists_blueprint.route('/edit/<int:artist_id>', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@authorize('modify:artists')
def edit_artist(artist_id):
    try:
        artist = load_and_validate_artist_data('edit', artist_id)
        artist.update()
        return get_success_response(artist.format(), 'Artist updated successfully')
    except exc.SQLAlchemyError as err:
        abort(500, err)


def load_and_validate_artist_data(mode='new', artist_id=None):
    data = json.loads(request.data) if request.data else abort(400, f'data not valid')
    if not data:
        abort(400, 'no data to update')
    artist = Artist.query.get(artist_id) if mode == 'edit' else Artist()
    if not artist and mode == 'edit':
        abort(404, f"artist with id: {artist_id} not found")
    artist.load(data)
    artist.id = artist_id if mode == 'edit' else None
    validation = artist.validate()
    if not validation.get('is_valid'):
        abort(400, f'data not valid {validation.get("errors")}')
    return artist

# endregion artists
