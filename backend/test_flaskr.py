import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, TEST_DB_NAME


class TriviaTestCase(unittest.TestCase):

    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}:{}/{}".format(
            DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, _DB_NAME
        )
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "What sea does the Jordan River empty into?",
            "answer": "Dead Sea",
            "category": 3,
            "dificulty": 3,
        }

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
    Write at least one test for each test for successful
    operation and for expected errors.
    """

    def test_get_categories(self):
        """tests that the get_categories endpoint gets the
        categories
        """
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_categories_error(self):
        """tests the get_categories endpoint for error
        when using a get request with a category ID
        """
        res = self.client().get("/categories/10")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_questions(self):
        """tests that the get_questions endpoint gets the
        questions
        """
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["questions"])

    def test_404_sent_requesting_beyond_valid_page(self):
        """tests that the get_questions endpoint pagination
        gets only valid pages and throws 404 error for invalid pages
        """
        res = self.client().get("/questions?page=10", json={"category": "2"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_questions_error(self):
        """Tests the get_questions endpoint for error
        when using a get request with a question ID
        """
        res = self.client().get("/questions/2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_questions_by_category(self):
        """Tests that the get_questions_by_category endpoint
        gets the questions by category
        """
        res = self.client().get("/categories/5/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["questions"])
        self.assertEqual(data["current_category"], "Entertainment")

    def test_404_sent_requesting_for_invalid_category(self):
        """Tests that the get_questions_by_category endpoint
        gets only valid categories and throws 404 error for
        invalid category get request
        """
        res = self.client().get("/categories/10/question")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_add_question(self):
        """Tests that the add_questions endpoint creates a new
        question
        """
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        #self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["questions"])

    def test_405_if_add_question_not_allowed(self):
        """Tests the add_questions endpoint for error
        when using a post request with a question ID
        """
        res = self.client().post("/questions/50", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_search_questions(self):
        """Tests the search_question endpoint returns results
        for existing search term
        """
        url = "/questions/search"
        res = self.client().post(url, json={"searchTerm": "title"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_404_on_get_request_search_question(self):
        """Tests that the search question endpoint returns
        404 error on get request
        """
        res = self.client().get("/questions/search")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_delete_questions(self):
        """Tests the delete_questions endpoint"""
        res = self.client().delete("/questions/19")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 19).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"], 19)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        """Tests the delete_questions endpoint for 422 error
        when non existent book is deleted
        """
        res = self.client().delete("/questions/1500")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_play_quizzes(self):
        """Tests play_quizzes works with quiz data"""
        quiz_data = {
            "previous_questions": [10, 11],
            "quiz_category": {"type": "Sports", "id": 6},
        }
        response = self.client().post("/quizzes", json=quiz_data)
        data = json.loads(response.data)
        print(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_quizzes(self):
        """Tests play-quizzes endpoint sends 422 error
            without quiz data being sent
        """
        response = self.client().post("/quizzes", json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
