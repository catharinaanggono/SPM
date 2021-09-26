from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from dotenv import load_dotenv
import user

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("dbURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 86400
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'userTable'

    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(200), nullable=False)
    UserType = db.Column(db.String(200), nullable=False)

    def __init__ (self, UserID, UserName, UserType):
        self.UserID = UserID
        self.UserName = UserName
        self.UserType = UserType
    
    def json(self):
        return{"UserID": self.UserID, "UserName": self.UserName, "UserType": self.UserType}


class prereq(db.Model):
    __tablename__ = 'coursePrereq'

    CourseID = db.Column(db.Integer, primary_key=True)
    PrereqID = db.Column(db.Integer, primary_key=True)

    def __init__(self, CourseID, PrereqID):
        self.CourseID = CourseID
        self.PrereqID = PrereqID
    
    def json(self):
        return{"CourseID": self.CourseID, "Prereq": self.PrereqID}

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

@app.route('/HrAssign', methods=["POST"])
def get_learner():
    data = request.get_json()
    #print(data['CourseID'])

    #i am assuming i can get the assigning courseID from previous pages
    prereqIDs = prereq.query.filter_by(CourseID = data['CourseID']).all()
    print(prereqIDs)

    #to get the prereq IDs of the course that is being assigned
    prereqID_list = []
    for prereqID in prereqIDs:
        prereqID_list.append(prereqID.json()['Prereq'])
    print(prereqID_list)

    #to get the learner IDs that has completed the prereq of the course is being assigned
    #if there is any prereq, then it will get those learner that has completed the prereq course
    learnerID_list = []
    if len(prereqID_list):
        learnerIDs = LearnerCourse.query.filter(LearnerCourse.CourseID.in_(prereqID_list)).all()
        for learnerID in learnerIDs:
            status = learnerID.json()['Status']
            if status == 'completed':
                learnerID_list.append(learnerID.json()['LearnerID'])
        Users = User.query.filter(User.UserID.in_(learnerID_list)).all()
        print(learnerID_list)
        print(Users)
        return jsonify({
            "code": 200,
            "data": {
                    "user": [user.json() for user in Users]
                }
        })
    #if there is no prereq, then just return the whole list of engineers
    else:
        Users = User.query.all()
        if len(Users):
            return jsonify({
                "code": 200,
                "data":{
                    "user": [user.json() for user in Users]
                }
            })
        return jsonify({
            "code":400,
            "message":"There are no user"
        }), 404










if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=True)


