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

    def __init__(self, CourseID, ClassID, LearnerID, ApplicationStatus):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.LearnerID = LearnerID
        self.ApplicationStatus = ApplicationStatus

    def json(self):
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "LearnerID": self.LearnerID, "ApplicationStatus": self.ApplicationStatus}

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

@app.route('/applications')
def get_all_courses():
    applications = Application.query.all()
        
    if len(applications):
        return jsonify({
            "code": 200,
            "data": {
                "courses": [application.json() for application in applications]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no applications."
    }), 404


# @app.route("/create_course", methods=["POST"])
# def create_course():
#     data = request.get_json()
#     print(data)
#     CourseTitle = data['CourseTitle']
#     CourseDescription = data['CourseDescription']
#     Badge = data['Badge']
#     prereqList = data['prereqList']
#     course = Course(CourseTitle, CourseDescription, Badge)

#     db.session.add(course)
#     db.session.commit()

#     if prereqList:
#         for prereq in prereqList:
#             coursePrereq = CoursePrereq(course.CourseID, prereq)
#             print(coursePrereq)
#             db.session.add(coursePrereq)

#     db.session.commit()
     
#     return jsonify(
#         {
#             "code": 200,
#             "message": "Course is successfully created"
#         }
#     ), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5007, debug=True)

