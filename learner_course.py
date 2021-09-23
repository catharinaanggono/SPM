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
    Status = db.Column(db.String(200), primary_key=True)

    def __init__(self, LearnerID, CourseID, Status):
        self.LearnerID = LearnerID
        self.CourseID = CourseID
        self.Status = Status
    
    def json(self):
        return{"LearnerID": self.LearnerID, "CourseID": self.CourseID, "Status": self.Status}

@app.route("/learner_course/<string:UserID>")
def get_leaner_courses(UserID):
    Courses = LearnerCourse.query.filter_by(LearnerID = UserID).all()
    if len(Courses):
        print(Courses)
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