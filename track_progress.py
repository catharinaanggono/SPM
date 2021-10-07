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


@app.route('/learner_distribution_chart/<string:ClassID>')
def distribution(ClassID):
    learners = classLearner.query.filter_by(ClassID = ClassID).all()
    learnerIDs = []
    for learner in learners:
        learnerIDs.append(learner.json()['LearnerID'])

    #print(learnerIDs)
    users = User.query.filter(User.UserID.in_(learnerIDs))

    output = {}
    for user in users:
        if user.json()['UserType'] in output:
            output[user.json()['UserType']] += 1
        else:
            output[user.json()['UserType']] = 1
    # print(output)
    return jsonify({
        "code": 200,
        "data": {
            "user_type_distribution": output,
        }
    })




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)