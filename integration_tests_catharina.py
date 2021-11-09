# Done by
# Catharina Anggono (email: catharinaa.2019@scis.smu.edu.sg)

import unittest
import flask_testing
import json
from course_and_class import app, db, User, Course, CourseClass, Section, Quiz, Question, QuestionAnswer, FinalQuiz, FinalQuizQuestion, FinalQuizQuestionAnswer
from datetime import datetime

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    app.config.update({
    'SQLALCHEMY_POOL_SIZE': None,
    'SQLALCHEMY_POOL_TIMEOUT': None
})

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        user_1 = User(1, 'Brenda', 'Senior Engineer')
        course_1 = Course(1, 'Test Course 1', 'Test Course 1 Description', 'Test Course 1 Badge')
        class_1 = CourseClass(1, datetime.strptime('31-12-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('30-06-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('01-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('31-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        class_1.ClassID = 1
        section_1 = Section(1, 1, "Test Section 1")
        db.session.add(user_1)
        db.session.add(course_1)
        db.session.add(class_1)
        db.session.add(section_1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestCreateUngradedQuiz(TestApp):    
    def test_create_quiz(self):
        request_body = {
            "CourseID": 1,
            "ClassID": 1,
            "SectionID": 1,
            "QuizTitle": "Test Quiz 1",
            "QuizTimer" : 60
        }

        response = self.client.post("/create_quiz",
                            data=json.dumps(request_body),
                            content_type='application/json')

        self.assertEqual(response.json,{
            "code": 201,
            "message": "Quiz is successfully created",
            "data": {
                "QuizID": 1,
            }
        })

    def test_create_question(self):
        request_body = {
            "CourseID": 1,
            "ClassID": 1,
            "SectionID": 1,
            "QuizID": 1,
            "QuestionContent" : "Test Question 1"
        }

        response = self.client.post("/create_question",
                            data=json.dumps(request_body),
                            content_type='application/json')

        self.assertEqual(response.json,{
            "code": 201,
            "message": "Question is successfully created",
            "data": {
                "QuestionID": 1,
            }
        })

    def test_create_answer(self):
        request_body = {
            "CourseID": 1,
            "ClassID": 1,
            "SectionID": 1,
            "QuizID": 1,
            "QuestionID": 1,
            "AnswerContent": "Test Answer 1",
            "Correct": 1
        }

        response = self.client.post("/create_answer",
                            data=json.dumps(request_body),
                            content_type='application/json')

        self.assertEqual(response.json,{
            "code": 201,
            "message": "Answer is successfully created",
        })

class TestGetUngradedQuiz(TestApp):
    maxDiff = None
    def test_retrieve_(self):
        quiz1 = Quiz(1, 1, 1, 'Test Quiz 1', 60)
        question1 = Question(1, 1, 1, 1, 'Test Question 1')
        answer1 = QuestionAnswer(1, 1, 1, 1, 1, 'Test Answer 1', 1)

        db.session.add(quiz1)
        db.session.add(question1)
        db.session.add(answer1)

        response = self.client.get("/get_quiz/1")    
        self.assertEqual(response.json, 
        {
            "code": 200,
            "data": {
                "Answers": [
                    {
                        "AnswerContent": "Test Answer 1",
                        "AnswerID": 1,
                        "ClassID": 1,
                        "Correct": True,
                        "CourseID": 1,
                        "QuestionID": 1,
                        "QuizID": 1,
                        "SectionID": 1
                    }
                ],
                "Questions": [
                    {
                        "ClassID": 1,
                        "CourseID": 1,
                        "QuestionContent": "Test Question 1",
                        "QuestionID": 1,
                        "QuizID": 1,
                        "SectionID": 1
                    }
                ],
                "Quiz": {
                    "ClassID": 1,
                    "CourseID": 1,
                    "QuizID": 1,
                    "QuizTimer": 60,
                    "QuizTitle": "Test Quiz 1",
                    "SectionID": 1
                }
            }
        })

class TestCreateFinalQuiz(TestApp):    
    def test_create_final_quiz(self):
        request_body = {
            "CourseID": 1,
            "QuizTitle": "Test Final Quiz 1",
            "QuizTimer" : 60
        }

        response = self.client.post("/create_graded_quiz",
                            data=json.dumps(request_body),
                            content_type='application/json')

        self.assertEqual(response.json,{
            "code": 201,
            "message": "Final quiz is successfully created",
            "data": {
                "QuizID": 1,
            }
        })

    def test_create_final_quiz_question(self):
        request_body = {
            "CourseID": 1,
            "QuizID": 1,
            "QuestionContent" : "Test Question 1"
        }

        response = self.client.post("/create_graded_question",
                            data=json.dumps(request_body),
                            content_type='application/json')

        self.assertEqual(response.json,{
            "code": 201,
            "message": "Question is successfully created",
            "data": {
                "QuestionID": 1,
            }
        })

    def test_create_final_quiz_answer(self):
        request_body = {
            "CourseID": 1,
            "QuizID": 1,
            "QuestionID": 1,
            "AnswerContent": "Test Answer 1",
            "Correct": 1
        }

        response = self.client.post("/create_graded_answer",
                            data=json.dumps(request_body),
                            content_type='application/json')

        self.assertEqual(response.json,{
            "code": 201,
            "message": "Answer is successfully created",
        })


if __name__ == '__main__':
    unittest.main()