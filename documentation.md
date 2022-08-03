# Trivia_API APP
 This project is a simple view for some questions and their answers , there are some categories for these questions , every question has a difficulty level from one to five. You can add new question or delete exsisting questions, also you can search for specific question.Additionally there is a simple quiz game that select random questions and you answer to them and get a score finally based on your answers.
 
 The backend code is adapted to follow PEP8 style guidelines

 # Getting started

  Pre-requisities and local development:
   
   Backend:

    Install dependencies by navigating to the `/backend` directory and running:

      In bash shell or on a mac terminal
      ```
        pip install -r requirements.txt
      ```
    With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
    
      In bash shell or on a mac terminal
      ```
        psql trivia < trivia.psql
        
      ```
    To run the server, execute:
        In bash shell or on a mac terminal

        ```
        export FLASK_APP=flaskr
        export FLASK_ENV=development
        flask run
        ```
        This will run locally on http://127.0.0.1:5000 and is a proxy in the frontend cofiguration
     
    Frontend:
        In bash shell or on a mac terminal
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
  
    Errors are returned as JSON objects in the following format:
  
  ### Sample Output
  ```
     {
        'success':False,
        'error':404,
        'message':'resource not found'
     }
  ```

    The API will return response for these error types when requests fail:

     404: Resource not found
     405: Method not allowed
     422: Unprocessable Entity
     500: Internal Server Error
    

  # Endpoints:

  # GET /categories
    General:
    Returns list of categories of questions
    Sample request: curl http://127.0.0.1:5000/categories
  
  ### Output
  ```
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
       "answer": "Blood", 
       "category": 1, 
       "difficulty": 4, 
       "id": 22, 
       "question": "Hematology is a branch of medicine involving the study of what?"
      }, 
      {
       "answer": "Alexander Fleming", 
       "category": 1, 
       "difficulty": 3, 
       "id": 21, 
       "question": "Who discovered penicillin?"
      }, 
      {
       "answer": "The Liver", 
       "category": 1, 
       "difficulty": 4, 
       "id": 20, 
       "question": "What is the heaviest organ in the human body?"
      }
      ], 
     "success": true, 
     "total_questions": 20
  }
  ```        

  # DELETE /questions/{question_id}
    General:
    Deletes the question that has {question_id} from the database
    
    Sample request: curl -X DELETE http://127.0.0.1:5000/questions/19

  ### Output
  ```
  { 
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
  ```

  # POST /questions/
    General:
    Create a new question in the database
    
    Sample request: curl -X POST -H "Content-Type: application/json" -d '{"question":"Which country has the fewest people per square mile?", "answer":"Namibia", "category":"3", "difficulty": 3}' http://127.0.0.1:5000/questions
  
  ### Output
  ```
        {
  "created": 52,
  "question": "Which country has the fewest people per square mile?",
  "success": true,
  "total_questions": 43
}
```

  # POST /questions/search
    General:
    searches the database and returns questions that {search_term} is part of the question
    Sample request: curl --header "Content-Type: application/json" -X POST -d "{\"searchTerm\":\"title\"}" http://127.0.0.1:5000/questions/search
  
  ### Output
  ```
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
  ```

  # GET /categories/{category_id}/questions
    General:
    Returns list of questions in a specific category
    Sample request: curl http://127.0.0.1:5000/categories/6/questions

  ### Output
  ```
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
    }
  ], 
  "success": true, 
  "total_questions": 2
}
  ```

  # POST /quiz
    General:
    Returns a random question every time from selected category by the user
    The random question shoud not be repeated again in the same quiz
    Sample request: curl --header "Content-Type: application/json" --request POST --data "{\"quiz_category\":{\"id\":6},\"previous_questions\":[45,29]}" http://127.0.0.1:5000/quizzes

### Output
  ```
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
```
