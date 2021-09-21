from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

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
        return{"CourseID": self.CourseID, "CourseTitle": self.CourseTitle, "CourseDescription": self.CourseDescription, "Badge": self.Badge}

@app.route('/courses')
def get_all_courses():
    courses = course.query.all()
    if len(courses):
        return jsonify({
            "code": 200,
            "data": {
                "courses": [each_course.json() for each_course in courses]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no courses."
    }), 404

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
    RegistrationStartDate = db.Column(db.DateTime, nullable=False)
    RegistrationEndDate = db.Column(db.DateTime, nullable=False)


    def __init__(self, CourseID, ClassID, TrainerID, StartDate, EndDate, RegistrationStartDate, RegistrationEndDate):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.TrainerID = TrainerID
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.RegistrationEndDate = RegistrationEndDate
        self.RegistrationStartDate = RegistrationStartDate

    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "TrainerID": self.TrainerID, "StartDate": self.StartDate, "EndDate": self.EndDate, "RegistrationStartDate": self.RegistrationStartDate, "RegistrationEndDate": self.RegistrationEndDate}

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

