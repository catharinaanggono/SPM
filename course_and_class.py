from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("dbURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 86400
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)


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
        if not hasattr(self, 'classList'):
            self.classList = []
        return{"CourseID": self.CourseID, "CourseTitle": self.CourseTitle, "CourseDescription": self.CourseDescription, "Badge": self.Badge, "classList": self.classList}



@app.route('/courses/<string:CourseID>')
def get_course(CourseID):
    if (course.query.filter_by(CourseID=CourseID).first()):
        return jsonify({
            "code": 200,
            "message": "Course exists" 
        }), 201
    else:
        return jsonify({
            "code": 404,
            "message": "Course doesn't exist"
        }), 404


class course_class(db.Model):
    __tablename__ = 'class'

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
    ClassSize = db.Column(db.Integer, nullable = False)
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
        if not hasattr(self, 'GreyOut'):
            self.GreyOut = False
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "StartDate": self.StartDate, "EndDate": self.EndDate, "ClassSize": self.ClassSize, "RegistrationStartDate": self.RegistrationStartDate, "RegistrationEndDate": self.RegistrationEndDate, "GreyOut": self.GreyOut}

@app.route('/classes')
def get_all_classes():
    classes = course_class.query.all()
    if len(classes):
        return jsonify({
            "code": 200,
            "data": {
                "classes": [each_class.json() for each_class in classes]
            }
        })
    return jsonify({
        "code": 404,
        "message": "There are no classes."
    }), 404

@app.route('/classes/<string:ClassID>')
def get_class(ClassID):
    if (course_class.query.filter_by(ClassID=ClassID).first()):
        return jsonify({
            "code": 200,
            "message": "Class exists" 
        }), 201
    else:
        return jsonify({
            "code": 404,
            "message": "Class doesn't exist"
        }), 404


class course_prereq(db.Model):
    __tablename__ = 'coursePrereq'

    CourseID = db.Column(db.Integer, primary_key = True)
    PrereqID = db.Column(db.Integer, primary_key = True)

    def __init__(self, CourseID, PrereqID):
        self.CourseID = CourseID
        self.PrereqID = PrereqID
    
    def json(self):
        return {"CourseID": self.CourseID, "PrereqID": self.PrereqID}

@app.route('/courseprereq')
def get_prereq():
    prereqs = course_prereq.query.all()
    if len(prereqs):
        return jsonify({
            "code": 200,
            "data": {
                "prereqList": [prereq.json() for prereq in prereqs]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no prerequisites"
    }), 404

class ClassTaken(db.Model):
    __tablename__ = 'classLearner'

    # CourseID INT NOT NULL,
    # ClassID INT NOT NULL,
    # LearnerID INT NOT NULL,
    # ApplicationStatus TEXT NOT NULL, -- applied, enrolled, rejected

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
        
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "LearnerID": self.LearnerID}

# CHECK REMAINING CLASS SLOTS -- DONE

# IF REJECTED, ALLOW APPLICATION AGAIN

# Checking for completed prereq

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


@app.route('/courses-all/<string:UserID>')
def get_all_courses(UserID):
    enrolled_courses = []
    takenClasses = ClassTaken.query.filter_by(LearnerID = UserID)

    prereq_courses = []
    takenPrereq = LearnerCourse.query.filter_by(LearnerID = UserID)
    for prereq in takenPrereq:
        prereq_courses.append(prereq.CourseID)
    for a_class in takenClasses:
        if a_class.ApplicationStatus == 'enrolled': # check if user already enrolled
            enrolled_courses.append(a_class.CourseID)
    courses = course.query.filter(course.CourseID not in enrolled_courses)
    x = 1
    class_per_course = []
    for a_course in courses:
        shown_classes = []
        if a_course.CourseID not in enrolled_courses:
            CourseID = a_course.CourseID
            course_prereqs = course_prereq.query.filter_by(CourseID = CourseID)
            for a_prereq in course_prereqs:
                if a_prereq.PrereqID not in prereq_courses:
                    x = 0
            now = datetime.date(datetime.today())
            classes = course_class.query.filter(CourseID == a_course.CourseID, now < course_class.RegistrationEndDate, now > course_class.RegistrationStartDate) # check registration date
            for a_class in classes:
                if x == 0:
                    a_class.GreyOut = True
                currentlyEnrolled = ClassTaken.query.filter(CourseID == CourseID, a_class.ClassID == a_class.ClassID, ClassTaken.ApplicationStatus == "enrolled") # check remaining class sizes
                totalEnrolled = currentlyEnrolled.count()
                if totalEnrolled < a_class.ClassSize and a_class.CourseID == a_course.CourseID:
                    shown_classes.append(a_class)
            class_per_course.append([a_course, shown_classes])
        x = 1
    actual_courses = [] 
    # By logic, the step from here below is not needed, but SQLAlchemy magic works in a very weird way :).. -- Each course may have been reset to its default values, so classList is gone except for the last course, so I had to repopulate myself courses myself.
    for i in range(0, len(class_per_course)):
        print(class_per_course[i][1])
        class_per_course[i][0].classList = [each_class.json() for each_class in class_per_course[i][1]]
        actual_courses.append(class_per_course[i][0])
    if courses.count():
        return jsonify({
            "code": 200,
            "data": {
                "courses": [each_course.json() for each_course in actual_courses]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no courses."
    }), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

