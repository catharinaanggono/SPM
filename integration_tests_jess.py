import unittest
import flask_testing
import json
from application_hr import app, db, Application, User, Course
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
        # u2 = User(7, 'Adam', 'Senior Engineer')
        course = Course(1, "WAD", "Course Desc", "badge test")
        app1 = Application(1, 2, 6, "applied", None, None)
        
        db.session.add(u1)
        db.session.add(course)
        db.session.add(app1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()




class TestGetAllApplications(TestApp):

    
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
                        "CourseTitle": "WAD"
                    }
                ]
            }
            })

    # def test_get_all_courses_no_prereq(self):
    #     course2 = course(None, 'Test Course 2 - Prereq 1', 'Test Course 2 Description', 'Test Course 2 Badge')
    #     courseprereq1 = course_prereq(2, 1)
    #     class2 = course_class(2, 2, datetime.strptime('31-12-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('30-06-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('01-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('31-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
    #     db.session.add(course2)
    #     db.session.add(courseprereq1)
    #     db.session.add(class2)
    #     db.session.commit()

    #     response = self.client.get("/courses-all/1")
    #     self.assertEqual(response.json, 
    #     {
    #     "code":200,
    #     "data":{
    #         "courses":[
    #             {
    #                 "Badge":"Test Course 1 Badge",
    #                 "CourseDescription":"Test Course 1 Description",
    #                 "CourseID":1,
    #                 "CourseTitle":"Test Course 1",
    #                 "GreyOut":False,
    #                 "classList":[
    #                 {
    #                     "ClassID":1,
    #                     "ClassSize":20,
    #                     "CourseID":1,
    #                     "EndDate":"Wed, 30 Jun 2021 00:00:00 GMT",
    #                     "GreyOut":False,
    #                     "RegistrationEndDate":"Fri, 31 Dec 2021 00:00:00 GMT",
    #                     "RegistrationStartDate":"Fri, 01 Oct 2021 00:00:00 GMT",
    #                     "RemainingSlot":20,
    #                     "StartDate":"Fri, 31 Dec 2021 00:00:00 GMT",
    #                     "Status":"",
    #                     "TrainerList":[
                            
    #                     ]
    #                 }
    #                 ],
    #                 "prereqList":[
                    
    #                 ]
    #             },
    #             {
    #                 "Badge":"Test Course 2 Badge",
    #                 "CourseDescription":"Test Course 2 Description",
    #                 "CourseID":2,
    #                 "CourseTitle":"Test Course 2 - Prereq 1",
    #                 "GreyOut":True, # Notice GreyOut in this course is True
    #                 "classList":[
    #                 {
    #                     "ClassID":2,
    #                     "ClassSize":20,
    #                     "CourseID":2,
    #                     "EndDate":"Wed, 30 Jun 2021 00:00:00 GMT",
    #                     "GreyOut":False,
    #                     "RegistrationEndDate":"Fri, 31 Dec 2021 00:00:00 GMT",
    #                     "RegistrationStartDate":"Fri, 01 Oct 2021 00:00:00 GMT",
    #                     "RemainingSlot":20,
    #                     "StartDate":"Fri, 31 Dec 2021 00:00:00 GMT",
    #                     "Status":"",
    #                     "TrainerList":[
                            
    #                     ]
    #                 }
    #                 ],
    #                 "prereqList":[
    #                 "Test Course 1" #Prereq list
    #                 ]
    #             }
    #         ]
    #     }
    #     })

    # def test_self_enrol(self):
        

    #     request_body = {
    #         'UserID': 1,
    #         'CourseID': 1,
    #         'ClassID': 1
    #     }
        
    #     response = self.client.post("/self-enrol",
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')
                        
    #     self.assertEqual(response.json, {
    #         "code": 201,
    #         "message": "Applied to class sucessfully",
    #         "data": {
    #             'LearnerID': 1,
    #             'CourseID': 1,
    #             'ClassID': 1
    #             }
    #     })

    # def test_self_enrol_no_prereq(self):

    #     request_body = {
    #         'UserID': 1,
    #         'CourseID': 2,
    #         'ClassID': 2
    #     }

    #     response = self.client.post("/self-enrol",
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')
                        
    #     self.assertEqual(response.json, {
    #         "code": 403,
    #         "message": "Prerequisite not completed",
            
    #     })


if __name__ == '__main__':
    unittest.main()