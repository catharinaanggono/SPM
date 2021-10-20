import unittest
import flask_testing
import json
from course_and_class import app, db, SectionMaterial, ClassTaken, User, course, course_class
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
        u1 = User(1, 'John', 'Junior Engineer')
        u2 = User(2, 'Adam', 'Junior Engineer')
        course1 = course(None, 'Test Course 1', 'Test Course 1 Description', 'Test Course 1 Badge')
        class1 = course_class(1, 1, datetime.strptime('31-12-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('30-06-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('01-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('31-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        app1 = ClassTaken(1, 1, 2, 'applied')
        db.session.add(u1)
        db.session.add(course1)
        db.session.add(class1)
        db.session.add(app1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestCreateSelfEnrol(TestApp):

    
    def test_self_enrol(self):
        

        request_body = {
            'UserID': 1,
            'CourseID': 1,
            'ClassID': 1
        }
        
        response = self.client.post("/self-enrol",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
                        
        self.assertEqual(response.json, {
            "code": 201,
            "message": "Applied to class sucessfully",
            "data": {
                'LearnerID': 1,
                'CourseID': 1,
                'ClassID': 1
                }
        })

    def test_withdraw_application(self, CourseID=1, ClassID=1, UserID=2):
        response = self.client.post("/withdraw-application/{}/{}/{}".format(CourseID, ClassID, UserID))
        self.assertEqual(response.json, {
            "code": 201,
            "message": "Successfully withdrawn"
        })
        pass

if __name__ == '__main__':
    unittest.main()