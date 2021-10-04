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


class Course(db.Model):
    __tablename__ = 'course'

    CourseID = db.Column(db.Integer, primary_key=True)
    CourseTitle = db.Column(db.String(50), nullable=False)
    CourseDescription = db.Column(db.String(65535), nullable=False)
    Badge = db.Column(db.String(65535), nullable=False)

    def __init__(self, CourseTitle, CourseDescription, Badge):
        # self.CourseID = CourseID
        self.CourseTitle = CourseTitle
        self.CourseDescription = CourseDescription
        self.Badge = Badge
        # self.prereqList = []

    # def json(self):
    #     if not hasattr(self, 'prereqList'):
    #         self.prereqList = []
    #     return{"CourseID": self.CourseID, "CourseTitle": self.CourseTitle, "CourseDescription": self.CourseDescription, "Badge": self.Badge, "prereqList": self.prereqList}

class CoursePrereq(db.Model):
    __tablename__ = 'coursePrereq'

    CourseID = db.Column(db.Integer, primary_key=True)
    PrereqID = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.String(200), primary_key=True)

    def __init__(self, CourseID, PrereqID):
        self.CourseID = CourseID
        self.PrereqID = PrereqID
    
    def json(self):
        return{"CourseID": self.CourseID, "PrereqID": self.PrereqID}

class Class(db.Model):
    __tablename__ = 'class'

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    ClassSize = db.Column(db.Integer, nullable=False)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
    RegistrationStartDate = db.Column(db.DateTime, nullable=False)
    RegistrationEndDate = db.Column(db.DateTime, nullable=False)


    def __init__(self, ClassID, StartDate, EndDate, RegistrationStartDate, RegistrationEndDate, ClassSize):
        # self.CourseID = CourseID
        self.ClassID = ClassID
        self.ClassSize = ClassSize
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.RegistrationEndDate = RegistrationEndDate
        self.RegistrationStartDate = RegistrationStartDate

    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "ClassSize": self.ClassSize, "StartDate": self.StartDate, "EndDate": self.EndDate, "RegistrationStartDate": self.RegistrationStartDate, "RegistrationEndDate": self.RegistrationEndDate}




@app.route('/courses/<string:CourseID>')
def get_course(CourseID):
    if (Course.query.filter_by(CourseID=CourseID).first()):
        return jsonify({
            "code": 200,
            "message": "Course exists" 
        }), 201
    else:
        return jsonify({
            "code": 404,
            "message": "Course doesn't exist"
        }), 404

@app.route("/create_course", methods=["POST"])
def create_course():
    data = request.get_json()
    print(data)
    CourseTitle = data['CourseTitle']
    CourseDescription = data['CourseDescription']
    Badge = data['Badge']
    prereqList = data['prereqList']
    course = Course(CourseTitle, CourseDescription, Badge)

    db.session.add(course)
    db.session.commit()


    for prereq in prereqList:
        coursePrereq = CoursePrereq(course.CourseID, prereq)
        print(coursePrereq)
        db.session.add(coursePrereq)

    db.session.commit()
     
    return jsonify(
        {
            "code": 201,
            "message": "Course is successfully created"
        }
    ), 201        


@app.route("/create_class", methods=["POST"])
def create_class():
    data = request.get_json()
    cl = Class(**data)
    print(data)
    ClassSize = data['ClassSize']
    StartDate = data['StartDate']
    EndDate = data['EndDate']

    db.session.add(cl)
    db.session.commit()
     
    return jsonify(
        {
            "code": 201,
            "message": "Class is successfully created"
        }
    ), 201       


    # if (course.query.filter_by(CourseTitle=CourseTitle).first()):
    #     return jsonify(
    #         {
    #             "code": 400,
    #             "message": "Course already exists."
    #         }
    #     ), 400
    # try:
    #     db.session.add(c)
    #     db.session.commit()
    # except:
    #    return jsonify(
    #        {
    #             "code": 500,
    #             "message": "An error occurred in creating a course."
    #        }
    #    ), 500
 
    # return jsonify(
    #     {
    #         "code": 201,
    #         "data": c.json()
    #     }
    # ), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)

