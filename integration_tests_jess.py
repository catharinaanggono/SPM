import unittest
import flask_testing
import json
from course_and_class import app, db, ClassTaken, User, Course
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

        course = Course(1, "WAD", "Course Desc", "badge test")
        app1 = ClassTaken(1, 2, 6, "applied")
        app2 = ClassTaken(1, 2, 7, "applied")
        
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(course)
        db.session.add(app1)
        db.session.add(app2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()




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