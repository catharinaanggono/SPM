import unittest
import flask_testing
import json
from datetime import datetime
from course_and_class import app, db, CoursePrereq, ClassTaken, User, CourseClass, Course

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
        course1 = Course(3, "WAD1", "Teach about programming", "python_badge.png")
        course2 = Course(4, "WAD2", "Teach about programming", "python_badge.png")
        prereq1 = CoursePrereq(4, 3)
        class1 = CourseClass(3, datetime.strptime('31-12-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('30-06-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('01-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('31-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        class2 = CourseClass(4, datetime.strptime('31-12-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('30-06-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('01-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('31-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        class1.ClassID = 1
        class2.ClassID = 2
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

#for assign_learner.py
class TestRetrieveLearner(TestApp):
    def test_retrieve_learner(self):

        classLearner1 = ClassTaken(3, 1, 1, "completed")
        classLearner2 = ClassTaken(4, 1, 1, "ongoing")

        db.session.add(classLearner1)
        db.session.add(classLearner2)

        request_body = {
            'CourseID': 4
        }


        response = self.client.post("/HrAssign",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        # print('-----------')
        # print(response.json)
        self.assertEqual(response.json,{
            "code": 200,
            "data":{
                "user":[{'UserID': 1, 
                        'UserName': 'Jhonny', 
                        'UserType': 'Senior Engineer'}]
            }
        })
    
    def test_prereq(self):
        
        classLearner3 = ClassTaken(3, 1, 1, "ongoing")
        classLearner4 = ClassTaken(4, 1, 1, "self_enrolled")

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
        
        course3 = Course(1, "SPM", "Teach about programming", "python_badge.png")
        class3 = CourseClass(1, datetime.strptime('31-12-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('30-06-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('01-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('31-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        class3.ClassID = 3

        db.session.add(course3)
        db.session.add(class3)


        request_body = {
            'CourseID': 1
        }


        response = self.client.post("/HrAssign",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        #should retrieve all the user
        self.assertEqual(response.json,{
            "code": 200,
            "data":{
                "user":[{'UserID': 1, 
                        'UserName': 'Jhonny', 
                        'UserType': 'Senior Engineer'}]
            }
        })
    
class TestAssignLeaner(TestApp):
    def test_assign_learner(self):
        learner2 = User(2, "Brenda", "Junior Engineer")
        learner3 = User(3, "Justin", "Junior Engineer")

        db.session.add(learner2)
        db.session.add(learner3)

        request_body = {
          "CourseID": "3",
          "ClassID": "1",
          "data": [[3, 1, 2, "hr_enrolled"], [3, 1, 3, "hr_enrolled"]]
        }

        response = self.client.post("/assign_learners",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json,{
            "code": 201,
            "data": [{
                    'CourseID': 3, 
                    'ClassID': 1, 
                    'LearnerID': 2, 
                    'ApplicationStatus': "hr_enrolled"},
                    {
                    'CourseID': 3, 
                    'ClassID': 1, 
                    'LearnerID': 3, 
                    'ApplicationStatus': "hr_enrolled"
                    }],
            "message": "Engineers has been successfully applied for the course"
        })
    
    def test_existing_learner(self):

        classLearner5 = ClassTaken(3, 1, 1, "ongoing")

        db.session.add(classLearner5)

        request_body = {
          "CourseID": "3",
          "ClassID": "1",
          "data": [[3, 1, 1, "hr_enrolled"]]
        }

        response = self.client.post("/assign_learners",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        print(response.json)
        self.assertEqual(response.json,{
        "code": 500,
        "data":[{'ApplicationStatus': 'ongoing',
                'ClassEndDate': '',
                'ClassID': 1,
                'ClassStartDate': '',
                'CourseID': 3,
                'CourseTitle': '',
                'LearnerID': 1,
                'UserName': ""}],
        "message": "An error occured while adding course, the following learner has already been assigned to this class"
        })

    def test_class_availability(self):

        class4 = CourseClass(3, datetime.strptime('31-12-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('30-06-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 0, datetime.strptime('01-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('31-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        class4.ClassID = 4

        db.session.add(class4)

        request_body = {
          "CourseID": "3",
          "ClassID": "4",
          "data": [[3, 4, 1, "hr_enrolled"]]
        }

        response = self.client.post("/assign_learners",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json,{
        "code": 501,
        "available_seat": 0,
        "message": "There is no enough slot for this class."
        })





if __name__ == '__main__':
    unittest.main()