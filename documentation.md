# Trivia_API APP
 This project is a simple view for some questions and their answers , there are some categories for these questions , every question has a difficulty level from one to five. You can add new question or delete exsisting questions, also you can search for specific question.Additionally there is a simple quiz game that select random questions and you answer to them and get a score finally based on your answers.
 
 The backend code is adapted to follow PEP8 style guidelines

 # Getting started
  pre-requisities and local development:
   
   Backend:

    install dependencies by naviging to the `/backend` directory and running:

        ```bash
        pip install -r requirements.txt
        ```
        With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
        ```bash
        psql trivia < trivia.psql
        ```
        To run the server, execute:
        ```bash
        export FLASK_APP=flaskr
        export FLASK_ENV=development
        flask run
        ```
        This will run locally on http://127.0.0.1:5000 and is a proxy in the frontend cofiguration
     
     Frontend:

        ```bash
        npm start
        ```
        This will start http://localhost:3000 to view the frontend react app
  
  # Tests
   To run tests excute:
    ```
    dropdb trivia_test
    createdb trivia_test
    psql trivia_test < trivia.psql
    python test_flaskr.py
    ```


 # API Reference
  # Getting Started
    Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at http://127.0.0.1:5000/ which is set as a proxy in the frontend configuration.
    
    Authentication: This version of the app does not require authentication or API keys

  # Error Handling
    errors are returned as JSON objects in the following format:
    {
        'success':False,
        'error':404,
        'message':'resource not found'
    }
    The API will return these error types:
    404: resource not found
    422: Unprocessable Entity
    500: Internal Server Error
    
  # Endpoints:
   # GET /categories
    General:
    Returns list of categories of questions
    Sample request: curl http://127.0.0.1:5000/categories
       {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
    #######################################################################################################
   # GET /questions
    General:
    Returns list of questions which are paginated as every page has 10 questions
    Returns total num. of questions
    Sample request : curl http://127.0.0.1:5000/questions
        {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "History",
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "4",
      "category": 1,
      "difficulty": 3,
      "id": 43,
      "question": "The Brain Is Divided Into How Many Lobes?"
    }, {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }
  ],
  "success": true,
  "total_questions": 42
  }
        #######################################################################################################
   # DELETE /questions/{question_id}
    General:
    Deletes the question that has {question_id} from the database
    
    Sample request: curl -X DELETE http://127.0.0.1:5000/questions/19
        {
        "deleted": 19,
        
  "deleted": 19,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 42
  }
        #######################################################################################################
   # POST /questions/
    General:
    Create a new question in the database
    
    Sample request: curl -X POST -H "Content-Type: application/json" -d '{"question":"Which country has the fewest people per square mile?", "answer":"Namibia", "category":"3", "difficulty": 3}' http://127.0.0.1:5000/questions
        {
  "created": 52,
  "question": "Which country has the fewest people per square mile?",
  "success": true,
  "total_questions": 43
}
    #######################################################################################################
   # POST /questions/search
    General:
    searches the database and returns questions that {search_term} is part of the question
    Sample request: curl --header "Content-Type: application/json" -X POST -d "{\"searchTerm\":\"title\"}" http://127.0.0.1:5000/questions/search
        {
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
    #######################################################################################################
   # GET /categories/{category_id}/questions
    General:
    Returns list of questions in specific category
    Sample request: curl http://127.0.0.1:5000/categories/6/questions
        {
        "current_category": "Sports",
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "Nigeria",
      "category": 6,
      "difficulty": 2,
      "id": 28,
      "question": "Which country won the AFCON 2013?"
    },
    {
      "answer": "Patrice Motsepe",
      "category": 6,
      "difficulty": 3,
      "id": 29,
      "question": "Who is the current president of CAF?"
    }
  ],
  "success": true,
  "total_questions": 4
}
    #######################################################################################################
   # POST /quiz
    General:
    Returns a random question every time from selected category by the user
    The random question shoud not be repeated again in the same quiz
    Sample request: curl --header "Content-Type: application/json" --request POST --data "{\"quiz_category\":{\"id\":6},\"previous_questions\":[45,29]}" http://127.0.0.1:5000/quizzes
        {
  "question": {
    "answer": "Brown",
    "category": 6,
    "difficulty": 2,
    "id": 44,
    "question": " What color was the original basketball?"
  },
  "success": true
}
#####################################################################################################

# Error handling

The API will return three error types when requests fail:

405: Method not allowed
404: Resource Not Found
422: Not Processable



 # Author
  Joseph Emefieh

 # Acknowledgements
  My session lead Gift Chimponda and Udacity instructors