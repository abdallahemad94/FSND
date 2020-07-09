# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
API and Endpoints documentation updated for submission
Endpoints
GET '/categories', '/questions', '/categories/<int:category_id>/questions'
POST '/questions', '/questions/search','/quizzes'
DELETE '/questions/<int:question_id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- usage: get all questions
- Returns: a dictionary with all questions, number of questions, dictionary od categories, current category
- Request query params: page_no
- Returns: An object with four keys
    1) questions: a list that contains the questions,
    2) total_questions: number of question
    3) categories: a dictionary of categories key is the id and value is the category_string
    4) current_category: dictionary  that contains selected category
{"questions": [],
    "total_questions": 0,
    "categories": {0: "", 1: "", 2: ""},
    "current_category": {0: ""}}

GET /categories/<int:category_id>/questions'
- usage: filter question by specific category
- Returns: a list of all questions in a specific category
- Request argument: category_id
- Returns: An object with three keys
    1) questions: a list that contains the questions filterd by selected category,
    2) total_questions: number of questions returnd
    4) current_category: dictionary that contains selected category
{"questions": [],
    "total_questions": 0,
    "current_category": {0: ""}}

POST '/questions'
- usage: used to insert a new question
- returns: a dictinary with status code and success flag and the inserted question  
- Request argument: new question data as json 
{question="",
    answer="",
    category=0,    # category_id
    difficulty=0}
- Returns: 
{"success": true,
    "status_code": 201,
    "question": question.format()}

POST '/questions/search'
- usage: search question by specific search term and returns all that contains the search term
- Request argument: new question data as json 
{"searchTerm": ""}
- Returns: 
{"questions": [search results],
    "total_questions": 0,
    "current_category": {category_id: category_string}}

POST '/quizzes'
- usage: gets a random question from a specific category if previous_questions is supplied will not repeat the question again
- Request argument: dictionary with the category id and list of ids of preveious questions
{"quiz_category": {id: category_string},
"previous_questions": [question_id]}
- Returns: 
{"question": {id: 0, question: "", answer: "", category:"", deficulty: ""}}


DELETE '/questions/<int:question_id>'
- usage: delete a question 
- Request argument: question id
{"quiz_category": {id: category_string},
"previous_questions": [question_id]}
- Returns: 
{"question": {id: 0, question: "", answer: "", category:"", deficulty: ""}}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```