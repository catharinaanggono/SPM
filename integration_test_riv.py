import unittest
import flask_testing
import json
from datetime import datetime
from assign_learner import app, db, prereq, classLearner, User, prereq, Class, course

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
        course1 = course(3, "WAD1", "Teach about programming", "python_badge.png")
        course2 = course(4, "WAD2", "Teach about programming", "python_badge.png")
        prereq1 = prereq(4, 3)
        class1 = Class(3, 1, datetime.strptime('31-12-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('30-06-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('01-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('31-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        class2 = Class(4, 1, datetime.strptime('31-12-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('30-06-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('01-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('31-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        learner1 = User(1, "Jhonny", "Senior Engineer")
        

        db.session.add(learner1)
        db.session.add(course1)
        db.session.add(course2)
        db.session.add(class1)
        db.session.add(class2)
        db.session.add(prereq1)
        
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestRetrieveLearner(TestApp):
    def test_retrieve_learner(self):

        classLearner1 = classLearner(3, 1, 1, "completed")
        classLearner2 = classLearner(4, 1, 1, "ongoing")

        db.session.add(classLearner1)
        db.session.add(classLearner2)

        request_body = {
            'CourseID': 4
        }


        response = self.client.post("/HrAssign",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json,{
            "code": 200,
            "data":{
                "user":[{'UserID': 1, 
                        'UserName': 'Jhonny', 
                        'UserType': 'Senior Engineer'}]
            }
        })
    
    def test_prereq(self):
        
        classLearner3 = classLearner(3, 1, 1, "ongoing")
        classLearner4 = classLearner(4, 1, 1, "self_enrolled")

        db.session.add(classLearner3)
        db.session.add(classLearner4)


        request_body = {
            'CourseID': 4
        }


        response = self.client.post("/HrAssign",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json,{
            "code": 200,
            "data":{
                "user":[]
            }
        })
    
    def test_no_prereq(self):
        
        course3 = course(1, "SPM", "Teach about programming", "python_badge.png")
        class3 = Class(1, 1, datetime.strptime('31-12-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('30-06-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('01-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('31-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        
        db.session.add(course3)
        db.session.add(class3)


        request_body = {
            'CourseID': 1
        }


        response = self.client.post("/HrAssign",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json,{
            "code": 200,
            "data":{
                "user":[{'UserID': 1, 
                        'UserName': 'Jhonny', 
                        'UserType': 'Senior Engineer'}]
            }
        })



if __name__ == '__main__':
    unittest.main()