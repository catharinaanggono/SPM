from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("dbURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 86400
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)


class Application(db.Model):
    __tablename__ = 'classLearner'

    CourseID = db.Column(db.Integer, primary_key = True)
    ClassID = db.Column(db.Integer, primary_key = True)
    LearnerID = db.Column(db.Integer, primary_key = True)
    ApplicationStatus = db.Column(db.String(100), nullable = False)

    def __init__(self, CourseID, ClassID, LearnerID, ApplicationStatus, UserName, CourseTitle):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.LearnerID = LearnerID
        self.ApplicationStatus = ApplicationStatus
        self.Username = UserName
        self.CourseTitle = CourseTitle

    def json(self):
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "LearnerID": self.LearnerID, "ApplicationStatus": self.ApplicationStatus, "UserName": self.UserName, "CourseTitle": self.CourseTitle}

class User(db.Model):
    __tablename__ = 'userTable'

    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.Integer)
    UserType = db.Column(db.Integer)

    def __init__(self, UserID, UserName, UserType):
        self.UserID = UserID
        self.UserName = UserName
        self.UserType = UserType
    
    def json(self):
        return {"UserID": self.UserID, "UserName": self.UserName, "UserType": self.UserType}

class Course(db.Model):
    __tablename__ = 'course'

    CourseID = db.Column(db.Integer, primary_key=True)
    CourseTitle = db.Column(db.String(50), nullable=False)
    CourseDescription = db.Column(db.String(65535), nullable=False)
    Badge = db.Column(db.String(65535), nullable=False)

    def __init__(self, CourseID, CourseTitle, CourseDescription, Badge):
        self.CourseID = CourseID
        self.CourseTitle = CourseTitle
        self.CourseDescription = CourseDescription
        self.Badge = Badge

    def json(self):
        return{"CourseID": self.CourseID, "CourseTitle": self.CourseTitle, "CourseDescription": self.CourseDescription, "Badge": self.Badge}

# @app.route('/applications')
# def get_all_pending_applications():
#     applications = Application.query.filter_by(ApplicationStatus="applied").all()
#     usernames = []
#     print (type(applications))
#     for application in applications:
#         print(type(application))
#         user = User.query.filter_by(UserID=application.LearnerID).first()
#         usernames.append(user)
#     if len(applications):
#         return jsonify({
#             "code": 200,
#             "data": {
#                 "courses": [application.json() for application in applications],
#                 "usernames": [username.json()["UserName"] for username in usernames]
#             }
#         }), 200
#     return jsonify({
#         "code": 404,
#         "message": "There are no applications."
#     }), 404

@app.route('/applications')
def get_all_pending_applications():
    applications = Application.query.filter_by(ApplicationStatus="applied").all()

    for application in applications:
        user = User.query.filter_by(UserID=application.LearnerID).first()
        application.UserName = user.UserName
        course = Course.query.filter_by(CourseID=application.CourseID).first()
        application.CourseTitle = course.CourseTitle

    if len(applications):
        return jsonify({
            "code": 200,
            "data": {
                "applications": [application.json() for application in applications]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no applications."
    }), 404

@app.route("/get_trainers")
def get_all_senior_engineeers():
    trainers = User.query.filter_by(UserType="Senior Engineer").all()
    if len(trainers):
        return jsonify({
            "code": 200,
            "data": {
                "trainers": [trainer.json() for trainer in trainers]
            }
        })
    return jsonify({
        "code": 404,
        "message": "There are no trainers."
    }), 404

@app.route("/accept_application", methods=['POST'])
def accept_application():
    data = request.get_json()
    print(data)
    CourseID = data['CourseID']
    ClassID = data['ClassID']
    LearnerID = data['LearnerID']
    application = Application.query.filter_by(CourseID=CourseID).filter_by(ClassID=ClassID).filter_by(LearnerID=LearnerID).first()
    application.ApplicationStatus = "self_approved"

    db.session.commit()

    return jsonify(
        {
            "code": 200,
            "message": "Application has been accepted"
        }
    ), 200

@app.route("/reject_application", methods=['POST'])
def reject_application():
    data = request.get_json()
    print(data)
    CourseID = data['CourseID']
    ClassID = data['ClassID']
    LearnerID = data['LearnerID']
    application = Application.query.filter_by(CourseID=CourseID).filter_by(ClassID=ClassID).filter_by(LearnerID=LearnerID).first()
    application.ApplicationStatus = "rejected"

    db.session.commit()

    return jsonify(
        {
            "code": 200,
            "message": "Application has been rejected"
        }
    ), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5007, debug=True)

