import json

from flask import Blueprint, abort, request
from flask_cors import cross_origin
from sqlalchemy import exc

from shared.auth import requires_auth
from shared.common import get_success_response, get_fail_response
from shared.models import Role

roles_blueprint = Blueprint('roles', __name__)


# region roles

@roles_blueprint.route('/', methods=['GET'])
def get_roles_list():
    roles = [role.format() for role in Role.query.all()]
    return get_success_response(roles) if roles else get_fail_response("no roles found")

@roles_blueprint.route('/<int:role_id>', methods=['GET'])
def get_role(role_id):
    if not role_id:
        abort(400, 'id must not be null or less than 1')
    role = Role.query.get(role_id)
    if not role:
        abort(404, f"role with id: {role_id} not found")
    return get_success_response(role.format())


@roles_blueprint.route('/<int:role_id>', methods=['DELETE'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('delete:roles')
def delete_role(role_id):
    if not role_id:
        abort(400, 'id must not be null or less than 1')
    role = Role.query.get(role_id)
    if not role:
        abort(404, f"role with id: {role_id} not found")
    role.delete()
    return get_success_response(None, f'role with id: {role_id} deleted successfully')


@roles_blueprint.route('/new', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth('add:roles')
def add_roles():
    try:
        data = json.loads(request.data)
        role = Role()
        if not data:
            abort(400, 'cannot insert empty data')
        role.load(data)
        validation = role.validate()
        if not validation.get('is_valid'):
            abort(400, f'data not valid {validation.get("errors")}')
        role.id = None
        role.insert()
        return get_success_response(role.format(), 'Role added successfully')
    except exc.SQLAlchemyError as err:
        abort(500, err)

# endregion roles
