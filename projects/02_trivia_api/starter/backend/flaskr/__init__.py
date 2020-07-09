import os, sys
from flask import Flask, request, abort, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

sys.path.append(os.getcwd())
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r'/api/*': {"origins": "*"}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories', methods=["GET"])
    def categories_all():
        categories = {category.id: category.type for category in Category.query.all()}
        if len(categories) <= 0:
            abort(404, "No categories found")
        return jsonify({"categories": categories})

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route("/questions", methods=['GET'])
    def questions_all():
        page = request.args.get("page", 1, int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        if len(questions) <= 0:
            abort(404, "No questions found")
        return jsonify({
            "questions": [question.format() for question in questions[start:end]],
            "total_questions": len(questions),
            "categories": {category.id: category.type for category in Category.query.all()},
            "current_category": Category.query.all()[0].format()
        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def question_delete(question_id):
        question: Question = Question.query.get(question_id)
        if question is None:
            abort(404, f"question with Id:{question_id} dose not exist")
        try:
            question.delete()
        except:
            abort(500)
        return jsonify({
            "success": True,
            "status_code": 200,
            "deleted_question_id": question_id
        })

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route("/questions", methods=["POST"])
    @cross_origin()
    def questions_add():
        data = json.loads(request.data)
        question = Question(
            question=data.get("question", ''),
            answer=data.get("answer", ''),
            category=data.get("category", 0),
            difficulty=data.get("difficulty", 0),
        )
        if question.question is None or question.question == '':
            abort(400, "question cannot be null")
        if question.answer is None or question.answer == '':
            abort(400, "answer cannot be null")
        try:
            question.insert()
        except:
            abort(500)
        return jsonify({
            "success": True,
            "status_code": 201,
            "question": question.format()
        })

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route("/questions/search", methods=["POST"])
    @cross_origin()
    def questions_search():
        search_term = json.loads(request.data).get("searchTerm", "")
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        category = Category.query.first()
        if len(questions) <= 0:
            abort(404)
        return jsonify({
            "questions": [question.format() for question in questions],
            "total_questions": len(questions),
            "current_category": {category.id: category.type}
        })

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route("/categories/<int:category_id>/questions", methods=['GET'])
    def questions_by_category(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        category = Category.query.get(category_id)
        if len(questions) <= 0:
            abort(404)
        return jsonify({
            "questions": [question.format() for question in questions],
            "total_questions": len(questions),
            "current_category": {category.id: category.type}
        })

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route("/quizzes", methods=['POST'])
    def quizzes():
        category_id = int(json.loads(request.data).get("quiz_category", {}).get('id', 0))
        previous_questions = json.loads(request.data).get("previous_questions", [])
        questions = []
        if category_id > 0:
            if Category.query.get(category_id) is None:
                abort(404)
            questions = Question.query.filter(Question.category == category_id).all()
        else:
            questions = Question.query.all()
        if len(previous_questions) <= 0:
            random_question = questions[random.randint(0, len(questions) - 1)]
            return jsonify({
                "question": random_question.format(),
            })
        else:
            filtered_questions = list(filter(lambda x: x.id not in previous_questions, questions))
            if len(filtered_questions) > 0:
                random_question = filtered_questions[random.randint(0, len(filtered_questions) - 1)]
                return jsonify({
                    "question": random_question.format(),
                })
            else:
                return jsonify({
                    "question": None,
                })

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(400)
    def handle_400(error):
        return jsonify({
            "status_code": 400,
            "success": False,
            "message": "Bad request"
        })

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "status_code": 404,
            "success": False,
            "message": "Not found"
        })

    @app.errorhandler(422)
    def handle_422(error):
        return jsonify({
            "status_code": 422,
            "success": False,
            "message": "Unprocessable"
        })

    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({
            "status_code": 500,
            "success": False,
            "message": "Internal server error"
        })

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
