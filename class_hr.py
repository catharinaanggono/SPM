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

class Class(db.Model):
    __tablename__ = 'class'

    CourseID = db.Column(db.Integer, nullable=False)
    ClassID = db.Column(db.Integer, primary_key=True)
    ClassSize = db.Column(db.Integer, nullable=False)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
    RegistrationStartDate = db.Column(db.DateTime, nullable=False)
    RegistrationEndDate = db.Column(db.DateTime, nullable=False)


    def __init__(self, CourseID, StartDate, EndDate, RegistrationStartDate, RegistrationEndDate, ClassSize):
        self.CourseID = CourseID
        self.ClassSize = ClassSize
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.RegistrationEndDate = RegistrationEndDate
        self.RegistrationStartDate = RegistrationStartDate

    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "ClassSize": self.ClassSize, "StartDate": self.StartDate, "EndDate": self.EndDate, "RegistrationStartDate": self.RegistrationStartDate, "RegistrationEndDate": self.RegistrationEndDate}


class Trainer(db.Model):
    __tablename__ = 'classTrainer'

    CourseID = db.Column(db.Integer, nullable=False)
    ClassID = db.Column(db.Integer, primary_key=True)
    TrainerID = db.Column(db.Integer, primary_key=True)

    def __init__(self, CourseID, ClassID, TrainerID):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.TrainerID = TrainerID
    
    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "TrainerID": self.TrainerID}


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

@app.route("/get_trainers")
def get_all_senior_engineeers():
    trainers = User.query.filter_by(UserType="Senior Engineer").all()
    if len(trainers):
        return jsonify({
            "code": 200,
            "data": {
                "trainers": [trainer.json() for trainer in trainers]
            }
        })
    return jsonify({
        "code": 404,
        "message": "There are no trainers."
    }), 404


@app.route("/create_class", methods=["POST"])
def create_class():
    data = request.get_json()
    print(data)
    CourseID = data['CourseID']
    ClassSize = data['ClassSize']
    StartDate = data['StartDate']
    EndDate = data['EndDate']
    RegistrationStartDate = data['RegStartDate']
    RegistrationEndDate = data['RegEndDate']
    TrainerID = data['TrainerID']
    cl = Class(CourseID, StartDate, EndDate, RegistrationStartDate, RegistrationEndDate, ClassSize)

    db.session.add(cl)
    db.session.commit()

    classTrainer = Trainer(CourseID, cl.ClassID, TrainerID)
    db.session.add(classTrainer)
    db.session.commit()
     
    return jsonify(
        {
            "code": 200,
            "message": "Class is successfully created"
        }
    ), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5006, debug=True)

