# region imports
from dotenv import load_dotenv, find_dotenv;
find_dotenv()
load_dotenv()  # import dot-env and load .env file
from flask import Flask, jsonify, render_template, session, redirect, request, url_for
from flask_cors import CORS
from flask_migrate import Migrate
from os import urandom
from shared.models import db, setup_db
from shared.auth import AuthError, get_permissions
from blueprints.movies import movies_blueprint
from blueprints.artists import artists_blueprint
from blueprints.roles import roles_blueprint
from shared.common import get_fail_response, get_success_response, DateJSONEncoder
# endregion imports

# region app startup


def create_app(test_config=None):
    # create and configure the app
    _app = Flask(__name__)
    _app.secret_key = urandom(32)
    _app.config.from_object(test_config)
    _app.register_blueprint(movies_blueprint, url_prefix="/movies")
    _app.register_blueprint(artists_blueprint, url_prefix="/artists")
    _app.register_blueprint(roles_blueprint, url_prefix="/roles")
    _app.json_encoder = DateJSONEncoder
    CORS(_app)

    return _app


app = create_app()
setup_db(app)
migrate = Migrate(app, db)
# endregion app startup



@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS')
    return response


@app.route('/')
def index():
    return get_success_response(None, "Alive and working")


# region error handling


@app.errorhandler(400)
def handle_400(err):
    return get_fail_response(400, err.description)


@app.errorhandler(403)
def handle_403(err):
    return get_fail_response(403, err.description)


@app.errorhandler(404)
def handle_404(err):
    return get_fail_response(404, err.description)


@app.errorhandler(500)
def handle_500(err):
    return get_fail_response(500, err.description)


@app.errorhandler(AuthError)
def handle_auth_error(error):
    return get_fail_response(403, error.error.get("description"))


# endregion error handling


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
