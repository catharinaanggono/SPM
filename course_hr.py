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

    def __init__(self, CourseTitle, CourseDescription, Badge, prereqList):
        # self.CourseID = CourseID
        self.CourseTitle = CourseTitle
        self.CourseDescription = CourseDescription
        self.Badge = Badge
        self.prereqList = []

    def json(self):
        if not hasattr(self, 'prereqList'):
            self.prereqList = []
        return{"CourseID": self.CourseID, "CourseTitle": self.CourseTitle, "CourseDescription": self.CourseDescription, "Badge": self.Badge, "prereqList": self.prereqList}

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
    course = Course(**data)
    print(data)
    CourseTitle = data['CourseTitle']
    CourseDescription = data['CourseDescription']
    prereqList = data['prereqList']

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

