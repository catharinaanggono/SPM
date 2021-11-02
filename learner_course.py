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
        if not hasattr(self, 'course_class_id') and not hasattr(self, 'course_title') and not hasattr(self, 'class_start_date') and not hasattr(self, 'class_end_date'):
            self.course_class_id = ''
            self.course_title = ''
            self.class_start_date = ''
            self.class_end_date = ''
        return{"LearnerID": self.LearnerID, "CourseID": self.CourseID, "CourseTitle": self.course_title, "ClassID": self.course_class_id,  "ClassStartDate": self.class_start_date, "ClassEndDate": self.class_end_date, "Status": self.Status}

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
        if not hasattr(self, "CourseTitle"):
            self.CourseTitle = ''
        if not hasattr(self, 'class_start_date'):
            self.class_start_date = ''
        if not hasattr(self, 'class_end_date'):
            self.class_end_date = ''
        if not hasattr(self, 'ApplicationStatus'):
            self.ApplicationStatus = ''
        return{
                "CourseID": self.CourseID, 
                "ClassID": self.ClassID, 
                "LearnerID": self.LearnerID, 
                "ApplicationStatus": self.ApplicationStatus, 
                "CourseTitle": self.CourseTitle, 
                "ClassStartDate": self.class_start_date, 
                "ClassEndDate": self.class_end_date,
                "ApplicationStatus": self.ApplicationStatus
            }

class course(db.Model):
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

class course_class(db.Model):
    __tablename__ = 'class'

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
    RegistrationStartDate = db.Column(db.DateTime, nullable=False)
    RegistrationEndDate = db.Column(db.DateTime, nullable=False)


    def __init__(self, CourseID, ClassID, StartDate, EndDate, RegistrationStartDate, RegistrationEndDate):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.RegistrationEndDate = RegistrationEndDate
        self.RegistrationStartDate = RegistrationStartDate

    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "StartDate": self.StartDate, "EndDate": self.EndDate, "RegistrationStartDate": self.RegistrationStartDate, "RegistrationEndDate": self.RegistrationEndDate}

@app.route("/learner_ongoing_courses/<string:UserID>")
def get_leaner_ongoing_courses(UserID):
    Courses = classLearner.query.filter(classLearner.LearnerID == UserID, classLearner.ApplicationStatus.in_(['ongoing', 'self_approved', 'hr_enrolled'])).all()

    if len(Courses):
        print(Courses)
        for a_course in Courses:
            print(a_course)
            CourseID = a_course.CourseID
            print(CourseID)
            a_class_list = classLearner.query.filter_by(LearnerID = UserID, CourseID = CourseID).first()
            a_class_details = course_class.query.filter_by(ClassID = a_class_list.ClassID).first()
            a_course_title = course.query.filter_by(CourseID = CourseID).first()
            a_course.CourseTitle = a_course_title.CourseTitle
            a_course.course_class_id = a_class_list.ClassID 
            a_course.class_start_date = a_class_details.StartDate
            a_course.ApplicationStatus = a_class_list.ApplicationStatus
            a_course.class_end_date = a_class_details.EndDate 
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