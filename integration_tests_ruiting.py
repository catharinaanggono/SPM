import unittest
import flask_testing
import json
from course_and_class import app, db, User, Course, CourseClass
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

        learner1 = User(1, 'Anna', 'Junior Engineer')
        learner2 = User(2, 'Max', 'Senior Engineer')
        course1 = Course(1, 'SPM', 'SPM description', 'Course Badge')
        course2 = Course(2, 'Programming', 'Programming Description', 'Course Badge')

        class1 = CourseClass(1, datetime.strptime('31-11-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('27-05-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 50, datetime.strptime('02-08-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('31-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        class1.ClassID = 1

        class2 = CourseClass(2, datetime.strptime('31-11-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('27-05-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 50, datetime.strptime('02-08-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('31-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        class2.ClassID = 2

        # trainer1 = TrainerClass(1, 1, 1)
        trainer1 = User(3, 'Oliver', 'Senior Engineer')

        db.session.add(learner1)
        db.session.add(learner2)
        db.session.add(course1)
        db.session.add(course2)
        db.session.add(class1)
        db.session.add(class2)
        db.session.add(trainer1)

        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    
class TestCreateCourses(TestApp):
    def test_get_all_courses(self):

        response = self.client.get("/courses")
        self.assertEqual(response.json, {
            "code": 200, 
            "data": {
                "course": [
                    {
                        "Badge": "Course Badge", 
                        "CourseDescription": "SPM description", 
                        "CourseID": 1, 
                        "CourseTitle": "SPM", 
                        "GreyOut": False, 
                        "classList": [
                            {
                                "ClassID": 1,
                                "ClassSize": 50,
                                "CourseID": 1,
                                "EndDate": "Thu, 27 May 2021 00:00:00 GMT",
                                "GreyOut": False,
                                "RegistrationEndDate": "Fri, 31 Dec 2021 00:00:00 GMT",
                                "RegistrationStartDate": "Thu, 2 Aug 2021 00:00:00 GMT",
                                "StartDate": "Fri, 31 Dec 2021 00:00:00 GMT",
                                "Status": "",
                                "TrainerList": [
                                    {
                                        "UserID": 3,
                                        "UserName": "Oliver",
                                        "UserType": "Senior Engineer"
                                    }
                                ]
                            }
                        ], 
                        "prereqList": []
                    }, 
                    {
                        "Badge": "Course Badge", 
                        "CourseDescription": "Programming description", 
                        "CourseID": 2, 
                        "CourseTitle": "Programming", 
                        "GreyOut": False, 
                        "classList": [], 
                        "prereqList": []
                    }
                ]
            }, 
            "message": "Course exists"
        })


    def test_create_courses(self):

        request_body = {
            'CourseTitle': 'WAD',
            'CourseDescription': 'Web Development',
            'CourseID': 3,
            'Badge': 'Course Badge'
        }

        response = self.client.post("/create_course",
                                    data= json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json, {
            "data": {
                "course": {
                    'Badge': 'Course Badge',
                    'CourseTitle': 'WAD',
                    'CourseDescription': 'Web Development',
                    'CourseID': 3
                }
            },
    
            "code": 201,
            "message": "Course has been successfully created"
        })

    
    def test_reject_create_course(self):
        course1 = Course(CourseTitle='SPM', CourseDescription='SPM Description', 
                        CourseID = 1, Badge='Course Badge')

        db.session.add(course1)
        db.session.commit()

        request_body = {
            'CourseTitle': course1.CourseTitle,
            'CourseDescription': course1.CourseDescription,
            'CourseID': course1.CourseID,
            'Badge':course1.Badge
        }
        response = self.client.post("/create_course",
                                    data= json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.json, {
            "code": 400,
            "message": "Course already exists"
        })


if __name__ == '__main__':
    unittest.main()