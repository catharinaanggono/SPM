import unittest
import flask_testing
import json
from course_and_class import app, db, ClassTaken, User, Course, CourseClass, TrainerClass
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
        u1 = User(6, 'Lily', 'Junior Engineer')
        u2 = User(7, 'Aaron', 'Senior Engineer')
        u3 = User(8, 'Julie', 'Senior Engineer')

        course = Course(1, "WAD", "Course Desc", "badge test")
        # cl = CourseClass(1, datetime.strptime('05-11-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('28-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('25-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('01-11-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        # cl.ClassID = 2

        app1 = ClassTaken(1, 2, 6, "applied")
        app2 = ClassTaken(1, 2, 7, "applied")
        
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(course)
        # db.session.add(cl)
        db.session.add(app1)
        db.session.add(app2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestCreateClass(TestApp):
    def test_create_class(self):
        x = "2021-10-11T07:01:24.000000"
        y = datetime(2021, 11, 10, 10, 10, 10)
        request_body = {
          "CourseID": 1,
          "StartDate": x,
          "EndDate": x,
          "ClassSize": 20,
          "RegStartDate": x,
          "RegEndDate": x, 
          "TrainerIDList": [7, 8]
        }

        response = self.client.post("/create_class",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json,{
            "code": 201,
            "message": "Class is successfully created",
            "class": {
                "CourseID": 1,
                "ClassID": 1,
                "ClassSize": 20,
                "StartDate": "Sat, 05 Nov 2021 00:00:00 GMT",
                "EndDate": "Tue, 28 Dec 2021 00:00:00 GMT",
                "RegistrationStartDate": "Mon, 25 Oct 2021 00:00:00 GMT",
                "RegistrationEndDate": "Mon, 01 Nov 2021 00:00:00 GMT",
                },
            "trainers": [7, 8]
        })




class TestViewApplication(TestApp):

    
    def test_get_all_applications(self):
        
        response = self.client.get("/applications")
        self.assertEqual(response.json, 
        {
            "code":200,
            "data":{
                "applications":[
                    {
                        "CourseID": 1, 
                        "ClassID": 2, 
                        "LearnerID": 6, 
                        "ApplicationStatus": "applied", 
                        "UserName": "Lily", 
                        "CourseTitle": "WAD",
                        "ClassStartDate": "",
                        "ClassEndDate": ""
                    },
                    {
                        "CourseID": 1, 
                        "ClassID": 2, 
                        "LearnerID": 7, 
                        "ApplicationStatus": "applied", 
                        "UserName": "Aaron", 
                        "CourseTitle": "WAD",
                        "ClassStartDate": "",
                        "ClassEndDate": ""
                    }
                ]
            }
            })


    def test_approve_application(self):

        request_body = {
          "CourseID": 1,
          "ClassID": 2,
          "LearnerID": 6
        }

        response = self.client.post("/accept_application",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json,{
            "code": 201,
            "message": "Application has been accepted",
            "data": {
                "CourseID": 1, 
                "ClassID": 2, 
                "LearnerID": 6, 
                "ApplicationStatus": "self_approved", 
                "UserName": "Lily", 
                "CourseTitle": "WAD",
                "ClassStartDate": "",
                "ClassEndDate": ""
            }
        })


    # def test_approve_application_error(self):
    #     class1 = CourseClass(1, 3, datetime.strptime('05-11-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('28-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('25-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('01-11-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))


    #     request_body = {
    #       "CourseID": 1,
    #       "ClassID": 3,
    #       "LearnerID": 6
    #     }

    #     response = self.client.post("/accept_application",
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')

    #     self.assertEqual(response.json,{
    #         "code": 400,
    #         "message": "Unable to accept application because class has started"
    #     })


    def test_reject_application(self):

        request_body = {
        "CourseID": 1,
        "ClassID": 2,
        "LearnerID": 7
        }

        response = self.client.post("/reject_application",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json,{
            "code": 201,
            "message": "Application has been rejected",
            "data": {
                "CourseID": 1, 
                "ClassID": 2, 
                "LearnerID": 7, 
                "ApplicationStatus": "rejected", 
                "UserName": "Aaron", 
                "CourseTitle": "WAD",
                "ClassStartDate": "",
                "ClassEndDate": ""
            }
        })

if __name__ == '__main__':
    unittest.main()