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

#to retrieve data from the learner_course table
class LearnerCourse(db.Model):
    __tablename__ = 'LearnerCourse'

    LearnerID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.String(200), nullable=False)

    def __init__(self, LearnerID, CourseID, Status):
        self.LearnerID = LearnerID
        self.CourseID = CourseID
        self.Status = Status
    
    def json(self):
        if not hasattr(self, 'course_class_id'):
            self.course_class_id = ''
        return{"LearnerID": self.LearnerID, "CourseID": self.CourseID, "ClassID": self.course_class_id, "Status": self.Status}

class classLearner(db.Model):
    __tablename__ = 'classLearner'

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    LearnerID = db.Column(db.Integer, primary_key=True)
    ApplicationStatus = db.Column(db.String(65535),nullable=False)

    def __init__(self, CourseID, ClassID, LearnerID, ApplicationStatus):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.LearnerID = LearnerID
        self.ApplicationStatus = ApplicationStatus
    
    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "LearnerID": self.LearnerID, "ApplicationStatus": self.ApplicationStatus}

@app.route("/learner_ongoing_courses/<string:UserID>")
def get_leaner_ongoing_courses(UserID):
    Courses = LearnerCourse.query.filter_by(LearnerID = UserID, Status = 'Ongoing').all()
    if len(Courses):
        print(Courses)
        for a_course in Courses:
            print(a_course)
            CourseID = a_course.CourseID
            print(CourseID)
            a_class_list = classLearner.query.filter_by(LearnerID = UserID, CourseID = CourseID).first()
            a_course.course_class_id = a_class_list.ClassID 
            print(a_class_list)
            print("LearnerID", a_course.LearnerID)
            print('EACH COURSE CLASS ID', a_course.course_class_id)

        return jsonify(
            {
                "code": 200,
                "data": {
                    "learner_courses": [course.json() for course in Courses] 
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no course."
        }
    ), 404 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)