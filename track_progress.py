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

class MaterialProgress(db.Model):
    __tablename__ = 'MaterialProgress'

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    SectionID = db.Column(db.Integer, primary_key=True)
    MaterialID = db.Column(db.Integer, primary_key=True)
    LearnerID = db.Column(db.Integer, primary_key=True)
    STATUS = db.Column(db.Integer, nullable=False)


    def __init__ (self, CourseID, ClassID, SectionID, MaterialID, LearnerID, STATUS):
            self.CourseID = CourseID
            self.ClassID = ClassID
            self.SectionID = SectionID
            self.MaterialID = MaterialID
            self.LearnerID = LearnerID
            self.STATUS = STATUS
    
    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "SectionID": self.SectionID, "MaterialID": self.MaterialID, "LearnerID": self.LearnerID, "STATUS": self.STATUS}

class finalStudentQuizResult(db.Model):
    __tablename__ = "finalStudentQuizResult"

    CourseID = db.Column(db.Integer, nullable=False)
    ClassID = db.Column(db.Integer, nullable=False)
    QuizID = db.Column(db.Integer, nullable=False)
    LearnerID = db.Column(db.Integer, nullable=False)
    Grade = db.Column(db.Integer, nullable=False)
    AttemptID = db.Column(db.Integer, primary_key=True)

    def __init__ (self, CourseID, ClassID, QuizID, LearnerID, Grade, AttemptID):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.QuizID = QuizID
        self.LearnerID = LearnerID
        self.Grade = Grade
        self.AttemptID = AttemptID

    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "QuizID": self.QuizID, "LearnerID": self.LearnerID, "Grade": self.Grade, "AttemptID": self.AttemptID}

class studentQuizResult(db.Model):
    __tablename__ = "studentQuizResult"

    CourseID = db.Column(db.Integer, nullable=False)
    ClassID = db.Column(db.Integer, nullable=False)
    SectionID = db.Column(db.Integer, nullable=False)
    QuizID = db.Column(db.Integer, nullable=False)
    LearnerID = db.Column(db.Integer, nullable=False)
    Grade = db.Column(db.Integer, nullable=False)
    AttemptID = db.Column(db.Integer, primary_key=True)

    def __init__ (self, CourseID, ClassID, SectionID, QuizID, LearnerID, Grade, AttemptID):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.SectionID = SectionID
        self.QuizID = QuizID
        self.LearnerID = LearnerID
        self.Grade = Grade
        self.AttemptID = AttemptID

    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "SectionID": self.SectionID, "QuizID": self.QuizID, "LearnerID": self.LearnerID, "Grade": self.Grade, "AttemptID": self.AttemptID}

@app.route('/learner_distribution_chart/<string:ClassID>')
def distribution(ClassID):

    #get all the learnerID using the classID
    learners = classLearner.query.filter_by(ClassID = ClassID).all()
    
    #the list of learners ID in the class
    learnerIDs = []
    course_status = []
    for learner in learners:
        learnerIDs.append(learner.json()['LearnerID'])
        course_status.append(learner.json()['ApplicationStatus'])
    
    #______________________________________________________________________Engineers Distribution chart_____________________

    #filtering to get user type from the learnerID list
    users = User.query.filter(User.UserID.in_(learnerIDs))


    #output to get the number of usertype in the class
    user_output = {}
    for user in users:
        if user.json()['UserType'] in user_output:
            user_output[user.json()['UserType']] += 1
        else:
            user_output[user.json()['UserType']] = 1
    # print(output)

    #______________________________________________________________________Number of learners completed the course chart_____________________

    status_output = {}
    for status in course_status:
        if status in status_output:
            status_output[status] += 1
        else:
            status_output[status] = 1

    print(status_output)

    #_____________________________________________________________________Number of completed sections in the class (section status)____________________________
    

    sections = MaterialProgress.query.filter_by(ClassID = ClassID).all()

    #section_output = {"Section1":{'completed':0, "imcomplete":0}, "Section2":{...}}

    section_output = {}
    for section in sections:
        #print(section.json()['SectionID'])
        if section.json()['SectionID'] in section_output:
            if section.json()['STATUS'] == 1:
                section_output[section.json()['SectionID']]['completed'] += 1
            else:
                section_output[section.json()['SectionID']]['incomplete'] += 1
        else:
            section_output[section.json()['SectionID']] = {'completed':0, 'incomplete':0}

    #print(section_output)

    #_____________________________________________________________________Final quiz distribution____________________________
    
    final_grades = finalStudentQuizResult.query.filter_by(ClassID=ClassID).all()

    #passing grade is 85%
    #take highest result
    #{'1': 73, '2':66, ....}

    final_grade_output = {}
    for final_grade in final_grades:
        #print(final_grade.json())
        learnerid = final_grade.json()['LearnerID']
        if learnerid in final_grade_output:
            if final_grade_output[learnerid] < final_grade.json()['Grade']:
                final_grade_output[learnerid] = final_grade.json()['Grade']
        else:
            final_grade_output[learnerid] = final_grade.json()['Grade']


    #print(final_grade_output)

    #_____________________________________________________________________number of pass/fail for each section____________________________


    section_quiz_result = studentQuizResult.query.filter_by(ClassID=ClassID).all()

    #{"1": {1:79, 2:30...}, "2": {1: 82, 3:0}}

    quiz_result_output = {}
    for result in section_quiz_result:
        #print(quiz_result_output)
        learnerid = result.json()['LearnerID']
        sectionid = result.json()['SectionID']
        grade = result.json()['Grade']
        if sectionid in quiz_result_output:
            if learnerid in quiz_result_output[sectionid]:
                if quiz_result_output[sectionid][learnerid] < grade:
                    quiz_result_output[sectionid][learnerid] = grade
            else:
                quiz_result_output[sectionid][learnerid] = grade
        else:
            quiz_result_output[sectionid] = {learnerid: grade}

    #print(quiz_result_output)


    return jsonify({
        "code": 200,
        "data": {
            "user_type_distribution": user_output,
            "course_status": status_output,
            "section_status": section_output,
            "final_grade":final_grade_output,
            "section_quiz_result": quiz_result_output
        }
    })




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)