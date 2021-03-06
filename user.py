from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("dbURL") # STOP PUTTING UR PASSWORDS HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 86400
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'userTable'

    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(200), nullable=False)
    UserType = db.Column(db.String(200), nullable=False)

    def __init__ (self, UserID, UserName, UserType):
        self.UserID = UserID
        self.UserName = UserName
        self.UserType = UserType
    
    def json(self):
        return{"UserID": self.UserID, "UserName": self.UserName, "UserType": self.UserType}

class classLearner(db.Model):
    __tablename__ = 'classLearner'

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    LearnerID = db.Column(db.Integer, primary_key=True)
    ApplicationStatus = db.Column(db.String(200), nullable=False)


    def __init__ (self, CourseID, ClassID, LearnerID, ApplicationStatus):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.LearnerID = LearnerID
        self.ApplicationStatus = ApplicationStatus
    
    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "LearnerID": self.LearnerID, "ApplicationStatus": self.ApplicationStatus}

class LearnerCourse(db.Model):
    __tablename__ = 'LearnerCourse'

    LearnerID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.String(200), primary_key=True)

    def __init__(self, LearnerID, CourseID, Status):
        self.LearnerID = LearnerID
        self.CourseID = CourseID
        self.Status = Status
    
    def json(self):
        return{"LearnerID": self.LearnerID, "CourseID": self.CourseID, "Status": self.Status}


@app.route('/user')
def get_all():
    users = User.query.all()
    if len(users):
        return jsonify({
            "code": 200,
            "data":{
                "user": [user.json() for user in users]
            }
        })
    return jsonify({
        "code":400,
        "message":"There are no user"
    }), 404


@app.route('/user/<string:UserID>')
def get_acct_details(UserID):
    user = User.query.filter_by(UserID = UserID).all()
    Courses = classLearner.query.filter_by(LearnerID = UserID).all()
    if len(user) or len(Courses):
        return jsonify({
            "code": 200,
            "data":{
                "user_details": [user_detail.json() for user_detail in user], 
                "learner_courses": [course.json() for course in Courses]
            }
        })
    return jsonify({
        "code": 404,
        "message": "There are no such user"
    }), 404




class UserCourses(db.Model):
    __tablename__ = 'learnerCourse'

    LearnerID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.String(200), nullable=False)

    def __init__(self, LearnerID, CourseID, Status):
        self.LearnerID = LearnerID
        self.CourseID = CourseID
        self.Status = Status

    def json(self):
        return {"LearnerID": self.LearnerID, "CourseID": self.CourseID, "Status": self.Status}

@app.route('/user/prereq/<string:UserID>')
def get_acct_prereqs(UserID):
    user = UserCourses.query.filter_by(LearnerID = UserID, Status='completed').all()
    if len(user):
        return jsonify({
            "code": 200,
            "data":{
                "user_prereqs": [user_prereq.json() for user_prereq in user]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "User has not completed any courses"
    }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)