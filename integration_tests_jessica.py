import unittest
import flask_testing
import json
from course_and_class import app, db, ClassTaken, User, Course, CourseClass
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

# IMPORTANT: For this TDD test, it will create a mock database in our cloud database

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:4ordX9IZBFbU@3.140.60.132:3306/one_stop_lms_testing"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    app.config.update({
    'SQLALCHEMY_POOL_SIZE': None,
    'SQLALCHEMY_POOL_TIMEOUT': None
    })
    db = SQLAlchemy(app)

    def create_app(self):
        return app

    def setUp(self):
        self.engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:4ordX9IZBFbU@3.140.60.132:3306") # connect to server
        self.engine.execute("""
        DROP DATABASE IF EXISTS one_stop_lms_testing;
        """)
        self.engine.execute("""        
        CREATE DATABASE one_stop_lms_testing;
        """)
        self.engine.execute("USE one_stop_lms_testing") # select new db
        self.engine.execute("""CREATE TABLE IF NOT EXISTS userTable(
        UserID INT NOT NULL AUTO_INCREMENT,
        UserName TEXT NOT NULL,
        UserType TEXT NOT NULL,
        PRIMARY KEY (UserID)
        );""")
        self.engine.execute("""
        CREATE table if not exists course(
        CourseID INT NOT NULL AUTO_INCREMENT,
        CourseTitle VARCHAR(50) NOT NULL,
        CourseDescription TEXT NOT NULL,
        Badge TEXT NOT NULL,
        PRIMARY KEY (CourseID)
        );
        """)

        self.engine.execute("""
        CREATE table if not exists class(
        CourseID INT NOT NULL,
        ClassID INT NOT NULL AUTO_INCREMENT,
        StartDate DATETIME NOT NULL,
        EndDate DATETIME NOT NULL,
        ClassSize INT NOT NULL,
        RegistrationStartDate DATETIME NOT NULL,
        RegistrationEndDate DATETIME NOT NULL,
        PRIMARY KEY (ClassID),
        FOREIGN KEY (CourseID) REFERENCES course(CourseID)
        );
        """)
        self.engine.execute("""
        CREATE TABLE IF NOT EXISTS classLearner(
        CourseID INT NOT NULL,
        ClassID INT NOT NULL,
        LearnerID INT NOT NULL,
        ApplicationStatus TEXT NOT NULL, -- self_enrolled, hr_enrolled, rejected, failed, ongoing, completed
        PRIMARY KEY (ClassID, LearnerID),
        FOREIGN KEY (CourseID, ClassID) REFERENCES class(CourseID, ClassID),
        FOREIGN KEY (LearnerID) REFERENCES userTable(UserID) 
        );""")
        self.engine.execute("""
        CREATE TABLE IF NOT EXISTS classTrainer(
            CourseID INT NOT NULL,
            ClassID INT NOT NULL,
            TrainerID INT NOT NULL,
            PRIMARY KEY (ClassID, TrainerID),
            FOREIGN KEY (CourseID, ClassID) REFERENCES class(CourseID, ClassID),
            FOREIGN KEY (TrainerID) REFERENCES userTable(UserID)
        );
        """)


        u1 = User(6, 'Lily', 'Junior Engineer')
        u2 = User(7, 'Aaron', 'Senior Engineer')
        u3 = User(8, 'Julie', 'Senior Engineer')

        course = Course(1, "WAD", "Course Desc", "badge test")
        cl = CourseClass(1, datetime.strptime('30-11-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('28-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('25-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('01-11-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))
        cl.ClassID = 2

        app1 = ClassTaken(1, 2, 6, "self_enrolled")
        app2 = ClassTaken(1, 2, 7, "self_enrolled")
        
        

        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(course)
        db.session.commit()

        db.session.add(cl)
        db.session.commit()
        

        db.session.add(app1)
        db.session.add(app2)
        db.session.commit()


class TestCreateClass(TestApp):
    def test_create_class_assign_multiple_trainers(self):

        request_body = {
          "CourseID": 1,
          "StartDate": "2021-11-05T00:00:00.000000",
          "EndDate": "2021-12-28T07:01:24.000000",
          "ClassSize": 20,
          "RegStartDate": "2021-10-25T00:00:00.000000",
          "RegEndDate": "2021-11-01T00:00:00.000000", 
          "TrainerIDList": [7, 8]
        }

        response = self.client.post("/create_class",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.json,{
   "class":{
      "ClassID":3,
      "ClassSize":20,
      "CourseID":1,
      "EndDate":"Tue, 28 Dec 2021 07:01:24 GMT",
      "GreyOut":False,
      "RegistrationEndDate":"Mon, 01 Nov 2021 00:00:00 GMT",
      "RegistrationStartDate":"Mon, 25 Oct 2021 00:00:00 GMT",
      "RemainingSlot":False,
      "StartDate":"Fri, 05 Nov 2021 00:00:00 GMT",
      "Status":"",
      "TrainerList":False
   },
   "code":201,
   "message":"Class is successfully created",
   "trainers":[7,8]
})

    def test_create_class_assign_one_trainer(self):

            request_body = {
            "CourseID": 1,
            "StartDate": "2021-11-05T00:00:00.000000",
            "EndDate": "2021-12-28T07:01:24.000000",
            "ClassSize": 25,
            "RegStartDate": "2021-10-25T00:00:00.000000",
            "RegEndDate": "2021-11-01T00:00:00.000000", 
            "TrainerIDList": [7]
            }

            response = self.client.post("/create_class",
                                        data=json.dumps(request_body),
                                        content_type='application/json')
            
            self.assertEqual(response.json,{
    "class":{
        "ClassID":3,
        "ClassSize":25,
        "CourseID":1,
        "EndDate":"Tue, 28 Dec 2021 07:01:24 GMT",
        "GreyOut":False,
        "RegistrationEndDate":"Mon, 01 Nov 2021 00:00:00 GMT",
        "RegistrationStartDate":"Mon, 25 Oct 2021 00:00:00 GMT",
        "RemainingSlot":False,
        "StartDate":"Fri, 05 Nov 2021 00:00:00 GMT",
        "Status":"",
        "TrainerList":False
    },
    "code":201,
    "message":"Class is successfully created",
    "trainers":[7]
    })

    def test_create_class_no_trainer_selected(self):

            request_body = {
            "CourseID": 1,
            "StartDate": "2021-11-05T00:00:00.000000",
            "EndDate": "2021-12-28T07:01:24.000000",
            "ClassSize": 25,
            "RegStartDate": "2021-10-25T00:00:00.000000",
            "RegEndDate": "2021-11-01T00:00:00.000000", 
            "TrainerIDList": []
            }

            response = self.client.post("/create_class",
                                        data=json.dumps(request_body),
                                        content_type='application/json')
            
            self.assertEqual(response.json,{
            "code": 400,
            "message": "Trainer is not selected"
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
                        "ApplicationStatus": "self_enrolled", 
                        "UserName": "Lily", 
                        "CourseTitle": "WAD",
                        "ClassStartDate": "",
                        "ClassEndDate": ""
                    },
                    {
                        "CourseID": 1, 
                        "ClassID": 2, 
                        "LearnerID": 7, 
                        "ApplicationStatus": "self_enrolled", 
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


    def test_approve_application_after_class_started_error(self):
        class1 = CourseClass(1, datetime.strptime('05-11-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('28-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('25-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('01-11-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))

        class1.ClassID = 3
        db.session.add(class1)
        db.session.commit()

        request_body = {
          "CourseID": 1,
          "ClassID": 3,
          "LearnerID": 6
        }

        response = self.client.post("/accept_application",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json,{
            "code": 400,
            "message": "Unable to accept application because class has started"
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


    def test_reject_application_after_class_started_error(self):
        class1 = CourseClass(1, datetime.strptime('05-11-2021 00:00:00.000000', '%d-%m-%Y %H:%M:%S.%f'), datetime.strptime('28-12-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), 20, datetime.strptime('25-10-2021 00:00:00', '%d-%m-%Y %H:%M:%S'), datetime.strptime('01-11-2021 00:00:00', '%d-%m-%Y %H:%M:%S'))

        class1.ClassID = 3
        db.session.add(class1)
        db.session.commit()

        request_body = {
        "CourseID": 1,
        "ClassID": 3,
        "LearnerID": 6
        }

        response = self.client.post("/reject_application",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json,{
            "code": 400,
            "message": "Unable to reject application because class has started"
        })


if __name__ == '__main__':
    unittest.main()