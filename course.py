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

class classes(db.Model):
    __tablename__ = 'class'

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
    ClassSize = db.Column(db.Integer, nullable = False)
    RegistrationStartDate = db.Column(db.Date, nullable=False)
    RegistrationEndDate = db.Column(db.Date, nullable=False)


    def __init__(self, CourseID, ClassID, StartDate, EndDate, ClassSize, RegistrationStartDate, RegistrationEndDate):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.ClassSize = ClassSize
        self.RegistrationStartDate = RegistrationStartDate
        self.RegistrationEndDate = RegistrationEndDate
    
    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "StartDate": self.StartDate, "EndDate": self.EndDate, "ClassSize": self.ClassSize, "RegistrationStartDate": self.RegistrationStartDate, "RegistrationEndDate": self.RegistrationEndDate}


@app.route('/courses', methods=["POST"])
def get_course():

    data = request.get_json()
    print(data['data'])

    #to get the respective list from the html
    CourseID = []
    ClassID = []
    for learner in data['data']:
        CourseID.append(learner['CourseID'])
        ClassID.append(learner['ClassID'])
    
    #geting data from the course table based on the course IDs
    course_output = course.query.filter(course.CourseID.in_(CourseID))

    #getting the data from the database fron the class table
    class_retrive = []
    for i in range(len(CourseID)):
        end_data_output = classes.query.filter((classes.CourseID == CourseID[i]) & (classes.ClassID == ClassID[i])).all()
        class_retrive.append(end_data_output)
    
    #changing the data from json obj to list
    class_output = []
    for j in class_retrive:
        for k in j:
            class_output.append(k.json())

    #print(class_output)
    return jsonify({
        "code": 200,
        "data": {
            "courses": [course.json() for course in course_output],
            "classes": class_output
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)