import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}@{}/{}".format('postgres', 'localhost:5432',
                                                             self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertIsNotNone(data["categories"])
        self.assertTrue(len(data["categories"]) > 0)

    def test_get_all_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertIsNotNone(data["questions"])
        self.assertIsNotNone(data["total_questions"])
        self.assertIsNotNone(data["categories"])
        self.assertIsNotNone(data["current_category"])
        self.assertTrue(len(data["questions"]) > 0)
        self.assertTrue(len(data["categories"]) > 0)
        self.assertTrue(data["total_questions"] > 0)

    def test_add_questions(self):
        res = self.client().post("/questions", json={
            "question": "",
            "answer": "answer",
            "category": 1,
            "difficulty": 1,
        })
        data = json.loads(res.data)
        self.assertEqual(data['status_code'], 400)

        res = self.client().post("/questions", json={
            "question": "question",
            "answer": "",
            "category": 1,
            "difficulty": 1,
        })
        data = json.loads(res.data)
        self.assertEqual(data['status_code'], 400)

        res = self.client().post("/questions", json={
            "question": "question",
            "answer": "question",
            "category": 1,
            "difficulty": 1,
        })
        data = json.loads(res.data)
        self.assertEqual(data['status_code'], 201)
        self.assertTrue(data['question']['id'] > 0)

    def test_delete_questions(self):
        res = self.client().delete("/questions/0")
        data = json.loads(res.data)
        self.assertEqual(data["status_code"], 404)
        self.assertTrue(data["success"] is False)

        res = self.client().post("/questions", json={
            "question": "question",
            "answer": "question",
            "category": 1,
            "difficulty": 1,
        })
        data = json.loads(res.data)
        res = self.client().delete(f"/questions/{data['question']['id']}")
        data = json.loads(res.data)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(data['success'] is True)

    def test_search_questions(self):
        res = self.client().post("/questions/search", json={"searchTerm": "abcdefghijklmnopqrstuvxyz"})
        data = json.loads(res.data)
        self.assertEqual(data['status_code'], 404)
        self.assertTrue(data['success'] is False)

        res = self.client().post("/questions/search", json={"searchTerm": ""})
        data = json.loads(res.data)
        self.assertTrue(data['total_questions'] > 0)
        self.assertTrue(data['current_category'] is not None)


    def test_questions_by_category(self):
        res = self.client().get("/categories/0/questions")
        data = json.loads(res.data)

        self.assertTrue(data["success"] is False)
        self.assertEqual(data["status_code"], 404)

        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertTrue(data["total_questions"] > 0)
        self.assertTrue(data["current_category"] is not None)

    def test_quizzes(self):
        res = self.client().post("/quizzes", json={"quiz_category": {"id": 999999}, "previous_questions": []})
        data = json.loads(res.data)
        self.assertTrue(data["success"] is False)
        self.assertEqual(data["status_code"], 404)

        res = self.client().post("/quizzes", json={"quiz_category": {"id": 0}, "previous_questions": []})
        data = json.loads(res.data)
        self.assertTrue(data["question"] is not None)

        res = self.client().post("/quizzes", json={"quiz_category": {"id": 0}, "previous_questions": [i for i in range(1000)]})
        data = json.loads(res.data)
        self.assertTrue(data["question"] is None)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
