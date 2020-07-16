import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS, cross_origin

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
def drinks_get():
    try:
        drinks = [drink.short() for drink in Drink.query.all()]
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except exc.SQLAlchemyError:
        abort(500, ','.join(e.orig.args))


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks-detail", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth("get:drinks-detail")
def drinks_detail_get(payload):
    try:
        drinks = [drink.long() for drink in Drink.query.all()]
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except exc.SQLAlchemyError as e:
        abort(500, ','.join(e.orig.args))


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks", methods=["POST"])
@cross_origin(header=["Content-Type", "Authorization"])
@requires_auth("post:drinks")
def drinks_insert(payload):
    try:
        data = json.loads(request.data)
        drink = Drink()
        if data.get('title', '') is None or data.get('title', '') == '':
            abort(400, "title must be submitted")
        drink.title = data.get('title', '')
        if data.get('recipe', []) is None or data.get('recipe', []) == []:
            abort(400, "recipe must be submitted")
        drink.recipe = str(data.get('recipe'))
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except exc.SQLAlchemyError as e:
        abort(500, ','.join(e.orig.args))


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<int:drink_id>", methods=["PATCH"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth("patch:drinks")
def drinks_update(payload, drink_id):
    if drink_id is None or drink_id <= 0:
        abort(400, "drink id is not submitted")
    drink = None
    try:
        drink = Drink.query.get(drink_id)
    except exc.SQLAlchemyError as e:
        abort(500, ','.join(e.orig.args))
    if drink is None:
        abort(404, 'drink not found')
    data = json.loads(request.data)
    if data.get('title', '') is None or data.get('title', '') == '':
        abort(400, "title must be submitted")
    drink.title = data.get('title', '')
    if data.get('recipe', None) is not None and data.get('recipe', None) != []:
        drink.recipe = jsonify(data.get('recipe'))
    try:
        drink.update()
    except exc.SQLAlchemyError as e:
        abort(500, ','.join(e.orig.args))
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth("delete:drinks")
def drinks_delete(payload, drink_id):
    if drink_id is None or drink_id <= 0:
        abort(400, "drink id is not submitted")
    drink = None
    try:
        drink = Drink.query.get(drink_id)
    except exc.SQLAlchemyError as e:
        abort(500, ','.join(e.orig.args))
    if drink is None:
        abort(404, 'drink not found')
    try:
        drink.delete()
    except exc.SQLAlchemyError as e:
        abort(500, ','.join(e.orig.args))
    return jsonify({
        'success': True,
        'delete': drink_id
    }), 200


## Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(500)
def handle_500(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": error.description
    }), 500


@app.errorhandler(400)
def handle_400(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description
    }), 400


'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


@app.errorhandler(404)
def handle_404(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''


@app.errorhandler(AuthError)
def handle_AuthError(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error.get('description')
    }), error.status_code


if __name__ == '__main__':
    app.run()
