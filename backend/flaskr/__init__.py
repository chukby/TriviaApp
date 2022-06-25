import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    # GET all question categories
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
           categories = Category.query.order_by(Category.type).all()
           categories_formatted_to_dict = {category.id: category.type for category in categories}

           return jsonify({
            "success": True,
            "categories": categories_formatted_to_dict
           })
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    # pagination function
    def paginate_questions(request, question_list):
        page =request.args.get('page',1, type=int)
        start =(page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions =[question.format() for question in question_list]
        current_page_questions = questions[start:end]
        return current_page_questions

    # GET Question all questions pagination
    @app.route('/questions', methods=['GET'])
    def get_questions():
        question_list = Question.query.order_by(Question.category).all()
        current_page_questions = paginate_questions(request, question_list)
        question_categories = Category.query.order_by(Category.id).all()
        categories_formatted = {category.id : category.type for category in question_categories}

        if len(current_page_questions) == 0:
            abort(404)
        return  jsonify({
            'success': True,
            'questions': current_page_questions,
            'total_questions': len(question_list),
            'current_category': 'History',
            'categories': categories_formatted
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(question_id == Question.id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            question_list = Question.query.order_by(Question.id).all()
            current_page_questions = paginate_questions(request, question_list)

            return jsonify({
                'success' : True,
                'deleted' : question_id,
                'questions' : current_page_questions,
                'total_questions': len(question_list)
            })
        except:
            abort(422)



    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        question_details = request.get_json()

        question = question_details.get('question')
        answer = question_details.get('answer')
        category = question_details.get('category')
        difficulty = question_details.get('difficulty')

        try:
            new_question = Question(question=question,answer=answer,category=category,difficulty=difficulty)
            new_question.insert()

            question_list = Question.query.order_by(Question.id).all()
            current_page_questions = paginate_questions(request, question_list)

            return jsonify({
                'success': True,
                'created': new_question.id,
                'question': new_question.question,
                'total_questions': len(question_list)
            })

        except:
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_details = request.get_json()
        print(search_details)
        search_term = search_details.get("searchTerm", None)
        try:
            question_search_result = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
            current_page_questions = paginate_questions(request, question_search_result)

            return jsonify({
                "success": True,
                "questions": current_page_questions,
                "total_questions": len(question_search_result),
            })

        except:
                abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        categories_selection = Category.query.filter(
            Category.id == category_id).all()
        if len(categories_selection) == 0:
            abort(404)

        questions_by_category_selection = Question.query.join(Category, Question.category == Category.id ).filter(Category.id == category_id).all()
        category = Category.query.get(category_id)
        print(category)

        return jsonify({
            "success": True,
            "questions": paginate_questions(request, questions_by_category_selection),
            "total_questions": len(questions_by_category_selection),
            "current_category": category.type
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quizzes():
        if request.method == "POST":
            try:
                quiz_details = request.get_json()
                prev_questions = quiz_details.get('previous_questions', None)
                category = quiz_details.get('quiz_category', None)

                category_id = category['id']
                next_question = None
                
                if category_id is not None:
                    quiz_questions = Question.query.filter_by(category=category_id).filter(Question.id.notin_((prev_questions))).all()    
                else:
                    quiz_questions = Question.query.filter(Question.id.notin_((prev_questions))).all()
                
                if len(quiz_questions) > 0:
                    next_question = random.choice(quiz_questions).format()
                
                return jsonify({
                    'question': next_question,
                    'success': True,
                })
            except:
                abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
           "success": False, 
           "error": 404,
           "message": "Resource not found"
        }), 404
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
           "success": False, 
           "error": 405,
           "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable"
        }), 422
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Internal jserver error"
        }), 500

    return app

