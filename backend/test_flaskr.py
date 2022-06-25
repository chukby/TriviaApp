import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("student",
        "student", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'id': 40,
            'question' : "What sea does the Jordan River empty into?",
            'answer' : "Dead Sea",
            'category' : 3,
            'dificulty' : 3
        }

        self.new_category = {
            'id' : "6",
            'type' : "Sports",
        }


        # binds the app to the current context
        with self.app.app_context():
             self.db = SQLAlchemy()
             self.db.init_app(self.app)
             #create all tables
             self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        """tests that the get_categories endpoint gets the 
           categories
        """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
    
    def test_get_categories_error(self):
        """tests the get_categories endpoint for error 
           when using a get request with a category ID   
        """
        res = self.client().get('/categories/10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_questions(self):
        """ tests that the get_questions endpoint gets the 
            questions 
        """
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
    
    def test_404_sent_requesting_beyond_valid_page(self):
        """ tests that the get_questions endpoint pagination 
            gets only valid pages and throws 404 error for invalid pages 
        """
        res = self.client().get('/questions?page=10', json={'category' : '2'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_questions_error(self):
        """tests the get_questions endpoint for error 
           when using a get request with a question ID  
        """
        res = self.client().get('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')
    
    def test_get_questions_by_category(self):
        """ tests that the get_questions_by_category endpoint
            gets the questions by category 
        """
        res = self.client().get('/categories/5/questions') 
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['current_category'], 'Entertainment')

    
    def test_404_sent_requesting_get_questions_by_category_for_invalid_category(self):
        """ tests that the get_questions_by_category endpoint  
            gets only valid categories and throws 404 error for 
            invalid category get request
        """
        res = self.client().get('/categories/10/question')
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
    
    # def test_add_question(self):
    #     """ tests that the add_questions endpoint creates a new 
    #         question
    #     """
    #     res = self.client().post('/questions/', json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
    #     self.assertTrue(data['questions'])
    

    def test_405_if_add_question_not_allowed(self):
        """ tests the add_questions endpoint for error 
           when using a post request with a question ID  
        """
        res = self.client().post('/questions/50', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')



    def test_search_questions(self):
        """tests the search_question endpoint returns results
           for existing search term
        """
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'title'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_search_question_error(self):
        """Test _____________ """
        res = self.client().get('/questions/search')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)


    # def test_delete_questions(self):
    #     """ tests the delete_questions endpoint """
    #     res = self.client().delete('/questions/15')
    #     data = json.loads(res.data)
    
    #     question = Question.query.filter(Question.id == 15).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'], 15)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertEqual(question, None)
    
    def test_422_if_question_does_not_exist(self):
        """ tests the delete_questions endpoint for 422 error
            when non existent book is deleted
        """
        res = self.client().delete('/questions/1500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()