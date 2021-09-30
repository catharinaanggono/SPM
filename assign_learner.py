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

class classLearner(db.Model):
    __tablename__ = 'classLearner'

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    LearnerID = db.Column(db.Integer, primary_key=True)
    ApplicationStatus = db.Column(db.String(200), nullable=False)


    def __init__ (self, CourseID, ClassID, LearnerID, ApplicationStatus):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.LearnerID = LearnerID
        self.ApplicationStatus = ApplicationStatus
    
    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "LearnerID": self.LearnerID, "ApplicationStatus": self.ApplicationStatus}

class Class(db.Model):
    __tablename__ = 'class'

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
    ClassSize = db.Column(db.Integer, nullable=False)
    RegistrationStartDate = db.Column(db.DateTime, nullable=False)
    RegistrationEndDate = db.Column(db.DateTime, nullable=False)


    def __init__(self, CourseID, ClassID, StartDate, EndDate, ClassSize, RegistrationStartDate, RegistrationEndDate):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.ClassSize = ClassSize
        self.RegistrationEndDate = RegistrationEndDate
        self.RegistrationStartDate = RegistrationStartDate

    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "StartDate": self.StartDate, "EndDate": self.EndDate, "ClassSize": self.ClassSize, "RegistrationStartDate": self.RegistrationStartDate, "RegistrationEndDate": self.RegistrationEndDate}


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

    #i am assuming i can get the assigning courseID from previous pages!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11111111111111
    prereqIDs = prereq.query.filter_by(CourseID = data['CourseID']).all()
    #print(prereqIDs)

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


@app.route('/assign_learners', methods=['POST'])
def assign_learners():
    data = request.get_json()
    print(data)

    class_details = Class.query.filter_by(ClassID = data['ClassID'][0]).all()
    #number of learner in the class currently
    num_learner = len(classLearner.query.filter_by(ClassID = data['ClassID'][0]).all())
    
    #number of learner being assigned by HR
    num_assigned_learner = len(data['data'])

    class_details_dict = [attribute.json() for attribute in class_details]
    #the size of the class 
    class_size = class_details_dict[0]['ClassSize']

    # print(class_size)
    # print(num_learner)
    # print(num_assigned_learner)

    #number of availability in the class
    class_availability = class_size - num_learner

    #check if learner exist in the current class and return the learners that are exist in the class
    exist_learner = []
    for k in data['data']:
        check = classLearner.query.filter((classLearner.CourseID == k[0]) & (classLearner.ClassID == k[1]) & (classLearner.LearnerID == k[2]))
        if(check):
            for person in check:
                exist_learner.append(person.json())
    if(len(exist_learner) > 0):
        return jsonify({
        "code": 500,
        "data": exist_learner,
        "message": "An error occured while adding course, the following learner has already been assigned to this class"
        }), 500

    #if all the assigned learners does not exist in this class, then proceed to applying them to the class
    output = []
    if (class_availability - num_assigned_learner) > 0:
        for i in data['data']:
            upload_data = {'CourseID': i[0], 'ClassID': i[1], 'LearnerID': i[2], 'ApplicationStatus': i[3]}
            upload = classLearner(**upload_data)
            db.session.add(upload)
            db.session.commit()
            output.append(upload_data)
        return jsonify({
        "code": 200,
        "data": output,
        "message": "Engineers has been successfully applied for the course"
        }), 200
    else:
        return jsonify({
        "code": 501,
        "message": "There is no enough slot for this class"
        }), 501
                
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=True)


