from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
from flask import render_template

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("dbURL")
print(environ.get("dbURL"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 86400
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app) # initialise database with settings from app


class course(db.Model): 
    __tablename__ = 'course'

    CourseID = db.Column(db.Integer, primary_key=True)
    CourseTitle = db.Column(db.String(200), nullable=False)
    CourseDescription = db.Column(db.String(50000), nullable=False)
    Badge = db.Column(db.String(50000), nullable=False)
    
    def __init__(self, CourseID, CourseTitle, CourseDescription, Badge):
        self.CourseID = CourseID
        self.CourseTitle = CourseTitle
        self.CourseDescription = CourseDescription
        self.Badge = Badge

    def json(self):
        return{"CourseID": self.CourseID, "CourseTitle": self.CourseTitle, "CourseDescription": self.CourseDescription, "Badge": self.Badge}


@app.route('/courses')
def get_all_courses_hr():
    all_courses = course.query.all()
    print(all_courses)
    return jsonify({
            "code": 200,
            "message": "Course exists",
            "data": {
                "course": [course.json() for course in all_courses]
            }
        })
    

# to search for course via course ID
@app.route('/courses/<int:CourseID>')
def get_course(CourseID):
    pass





    # if (course.query.filter_by(CourseID=CourseID).first()):
    #     return jsonify({
    #         "code": 200,
    #         "message": "Course exists"
    #     }), 200
    # else:
    #     return jsonify({
    #         "code":404,
    #         "message": "Course not found"
    #     }), 404


# classes within the course
class course_class(db.Model):
    __tablename__ = "class"

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
    ClassSize = db.Column(db.Integer, nullable=False)
    RegistrationStartDate = db.Column(db.DateTime, nullable=False)
    RegistrationEndDate = db.Column(db.DateTime, nullable=False)


    def __init__(self, CourseID, ClassID, StartDate, EndDate, ClassSize, RegistrationStartDate, RegistrationEndDate):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.ClassSize = ClassSize
        self.RegistrationStartDate = RegistrationStartDate
        self.RegistrationEndDate = RegistrationEndDate


    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "StartDate": self.StartDate, "EndDate": self.EndDate, "ClassSize": self.ClassSize, "RegistrationStartDate": self.RegistrationStartDate, "RegistrationEndDate": self.RegistrationEndDate}


# query all classes
@app.route('/classes')
def get_all_classes():
    all_classes = course_class.query.all()
    return jsonify({
        "code": 200,
        "message": "class exists",
        "data": {
            "course_class" : [course_class.json() for course_class in all_classes]
        }
    })

# @app.route('/classes/<int:ClassID>') # don't need because all the class will just show ?
# def get_class(ClassID):

#     if len(classes):        #classes present
#         return jsonify({
#             "code": 200,
#             "message": {
#                 "classes": [each_class.json() for each_class in classes]
#             }
#         }), 201

#     if (course_class.query.filter_by(ClassID = ClassID).first()):
#         return jsonify ({
#             "code": 200,
#             "output": [{
#                 "Message": "Class Exists",
#                 "Class": course_class.ClassID
#             }] 
#         }), 201

#     else:
#         return jsonify({
#             "code": 404,
#             "message": "Class doesn't exist"
#         }), 404



class course_prereq(db.Model):
    __tablename__ = "coursePrereq"

    CourseID = db.Column(db.Integer, primary_key=True)
    PrereqID = db.Column(db.Integer, primary_key=True)

    def __init__(self, CourseID, PrereqID):
        self.CourseID = CourseID
        self.PrereqID = PrereqID
    
    def json(self):
        return{"CourseID": self.CourseID, "PrereqID": self.PrereqID}


@app.route('/courseprereq')
def get_prereq():
    all_prereqs = course_prereq.query.all()

    if len(all_prereqs):
        return jsonify({
            "code": 200,
            "message":{
                "all_prereqs": [prereq.json() for prereq in all_prereqs]
            }
        }), 201
    else:
        return jsonify({
            "code": 404,
            "message": "There are no pre requisites for this course"
        }), 404


# viewing learner's courses

class learner_courses(db.Model):
    __tablename__ = "LearnerCourse"

    LearnerID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.String(50), nullable=False)

    def __init__(self, LearnerID, CourseID, Status):
        self.LearnerID = LearnerID
        self.CourseID = CourseID
        self.Status = Status


    def json(self):
        return {"LearnerID": self.LearnerID, "CourseID": self.CourseID, "Status": self.Status}



# view classes taken by learners + class' status

class class_learner(db.Model):
    __tablename__ = "classLearner"

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    LearnerID = db.Column(db.Integer, primary_key=True)
    ApplicationStatus = db.Column(db.String(200), nullable=False)

    def __init__(self, CourseID, ClassID, LearnerID, ApplicationStatus):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.LearnerID = LearnerID
        self.ApplicationStatus = ApplicationStatus

    def json(self):
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "LearnerID": self.LearnerID, "ApplicationStatus": self.ApplicationStatus}



# view class trainers

class class_trainer(db.Model):
    __tablename__ = "classTrainer"

    CourseID = db.Column(db.Integer)
    ClassID = db.Column(db.Integer, primary_key=True)
    TrainerID = db.Column(db.Integer, primary_key=True)

    def __init__ (self, CourseID, ClassID, TrainerID):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.TrainerID = TrainerID

    def json(self):
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "TrainerID": self.TrainerID}



class user(db.Model):
    __tablename__ = "user"

    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(50), nullable=False)
    UserType = db.Column(db.String(50))

    def __init__(self, UserID, UserName, UserType):
        self.UserID = UserID
        self.UserName = UserName
        self.UserType = UserType
    
    def json(self):
        return {"UserID": self.UserID, "UserName": self.UserName, "UserType": self.UserType}


@app.route('/create-class/<CourseID>')
def create_class(CourseID):
    return render_template('create-class.html', CourseID=CourseID)

@app.route('/assign-learner/<CourseID>/<ClassID>')
def assign_learner(CourseID, ClassID):
    return render_template('assign_learner.html', CourseID=CourseID, ClassID=ClassID)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5202, debug=True)
