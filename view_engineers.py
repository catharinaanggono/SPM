from flask import Flask, json, jsonify
from os import environ
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#initialise app
app = Flask(__name__)

# app configurations
app.config['SQLAlCHEMY_DATABASE_URI'] = environ.get("dbURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 86400
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

# initiate database
db = SQLAlchemy(app) 

# create users class
class users(db.model):
    __tablename__ = 'userTable'

    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(50), nullable=False)
    UserType = db.Column(db.String(100), nullable=False)

    def __init__(self, UserID, UserName, UserType):
        self.UserID = UserID
        self.UserName = UserName
        self.UserType = UserType

    def json(self):
        return {"UserID": self.UserID, "UserName": self.UserName, "UserType": self.UserType}

@app.route('/users/<int:UserID>')
def get_user(UserID):
    if (users.query.filter_by(UserID=UserID).first()):
        return jsonify({
            "code": 200,
            "message": "User Found"
        }), 202
    else:
        return jsonify({
            "code":404,
            "message": "User not found"
        }), 404


# create classes class
class course_class(db.Model):
    __tablename__ = "class"

    ClassID = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
    ClassSize = db.Column(db.Integer, nullable=False)
    RegistrationStartDate = db.Column(db.DateTime, nullable=False)
    RegistrationEndDate = db.Column(db.DateTime, nullable=False)

    def __init__(self, ClassID, StartDate, EndDate, ClassSize, RegistrationStartDate, RegistrationEndDate):
        self.ClassID = ClassID
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.ClassSize = ClassSize
        self.RegistrationStartDate = RegistrationStartDate
        self.RegistrationEndDate = RegistrationEndDate

    def json(self):
        return {"ClassID": self.ClassID, "StartDate": self.StartID, "EndDate": self.EndDate, "ClassSize": self.ClassSize, "RegistrationStartDate": self.RegistrationStartDate, "RegistrationEndDate": self.RegistrationEndDate}


# class for learners (engineers)
class learner(db.Model):
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

@app.route('/learners/<int:LearnerID>')
def get_all_learners(LearnerID):
    list_of_learners = learner.query.all()      # get all learners

    if (len(list_of_learners)):                 # if learners exist
        return jsonify({
            "code": 200,
            "message": {
                "learners": [each_learner.json() for each_learner in list_of_learners]  # returns all engineers
            }
        }), 201

    if (learner.query.filter_by(LeaderID=LearnerID).first()):
        return jsonify ({
            "code": 200,
            "output": [{
                "Message": "Learner Found", 
                "learner": learner.LeaderID
            }]
        }), 201

    else: 
        return jsonify({
            "code": 404,
            "message": "Learner not found"
        }), 404



    



    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

