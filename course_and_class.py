from flask import Flask, json, request, jsonify, render_template, abort
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
import os
load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("dbURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 86400
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
print(environ.get("dbURL"))


class FinalStudentQuizResult(db.Model):
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


class Course(db.Model):
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
        if not hasattr(self, 'classList'):
            self.classList = []
        if not hasattr(self, 'GreyOut'):
            self.GreyOut = False
        if not hasattr(self, 'prereqList'):
            self.prereqList = []
        return{"CourseID": self.CourseID, "CourseTitle": self.CourseTitle, "CourseDescription": self.CourseDescription, "Badge": self.Badge, "classList": self.classList, "GreyOut": self.GreyOut, 'prereqList': self.prereqList}


class SectionMaterial(db.Model):
    __tablename__ = 'sectionMaterial'

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    SectionID = db.Column(db.Integer, primary_key=True)
    MaterialContent = db.Column(db.String(255), primary_key=True)
    '''
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    MaterialContent TEXT NOT NULL,
    '''

    def __init__(self, CourseID, ClassID, SectionID, MaterialContent):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.SectionID = SectionID
        self.MaterialContent = MaterialContent

    def create_path(self):

        course_path = 'static/course_material/' + str(self.CourseID)
        class_path = 'static/course_material/' + str(self.CourseID) + '/' + str(self.ClassID)
        section_path = 'static/course_material/' + str(self.CourseID) + '/' + str(self.ClassID) + '/' + str(self.SectionID)

        course_path_exists = os.path.isdir(course_path)
        class_path_exists = os.path.isdir(class_path)
        section_path_exists = os.path.isdir(section_path)

        if not course_path_exists:
            os.mkdir(course_path)

        if not class_path_exists:
            os.mkdir(class_path)

        if not section_path_exists:
            os.mkdir(section_path)
    
    def json(self):
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "SectionID": self.SectionID, "MaterialContent": self.MaterialContent}


class MaterialProgress(db.Model):
    __tablename__ = 'materialProgress'

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    SectionID = db.Column(db.Integer, primary_key=True)
    MaterialContent = db.Column(db.String(255), primary_key=True)
    LearnerID = db.Column(db.Integer, primary_key=True)

    def __init__(self, CourseID, ClassID, SectionID, MaterialContent, LearnerID):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.SectionID = SectionID
        self.MaterialContent = MaterialContent
        self.LearnerID = LearnerID


class CourseClass(db.Model):
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
        if not hasattr(self, 'GreyOut'):
            self.GreyOut = False
        if not hasattr(self, 'RemainingSlot'):
            self.RemainingSlot = False
        if not hasattr(self, 'TrainerList'):
            self.TrainerList = False
        if not hasattr(self, 'Status'):
            self.Status = ''
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "StartDate": self.StartDate, "EndDate": self.EndDate, "ClassSize": self.ClassSize, "RegistrationStartDate": self.RegistrationStartDate, "RegistrationEndDate": self.RegistrationEndDate, "GreyOut": self.GreyOut, "RemainingSlot": self.RemainingSlot, "TrainerList": self.TrainerList, "Status": self.Status}


class CoursePrereq(db.Model):
    __tablename__ = 'coursePrereq'

    CourseID = db.Column(db.Integer, primary_key = True)
    PrereqID = db.Column(db.Integer, primary_key = True)

    def __init__(self, CourseID, PrereqID):
        self.CourseID = CourseID
        self.PrereqID = PrereqID
    
    def json(self):
        return {"CourseID": self.CourseID, "PrereqID": self.PrereqID}


class ClassTaken(db.Model):
    __tablename__ = 'classLearner'

    # CourseID INT NOT NULL,
    # ClassID INT NOT NULL,
    # LearnerID INT NOT NULL,
    # ApplicationStatus TEXT NOT NULL, -- applied, enrolled, rejected

    CourseID = db.Column(db.Integer, primary_key = True)
    ClassID = db.Column(db.Integer, primary_key = True)
    LearnerID = db.Column(db.Integer, primary_key = True)
    ApplicationStatus = db.Column(db.String(100), nullable = False)

    def __init__(self, CourseID, ClassID, LearnerID, ApplicationStatus):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.LearnerID = LearnerID
        self.ApplicationStatus = ApplicationStatus

    def json(self):
        if not hasattr(self, "CourseTitle"):
            self.CourseTitle = ''
        if not hasattr(self, 'class_start_date'):
            self.class_start_date = ''
        if not hasattr(self, 'class_end_date'):
            self.class_end_date = ''
        
        return{
                "CourseID": self.CourseID, 
                "ClassID": self.ClassID, 
                "LearnerID": self.LearnerID, 
                "ApplicationStatus": self.ApplicationStatus, 
                "CourseTitle": self.CourseTitle, 
                "ClassStartDate": self.class_start_date, 
                "ClassEndDate": self.class_end_date,
                "ApplicationStatus": self.ApplicationStatus
            }

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


class TrainerClass(db.Model):
    __tablename__ = 'classTrainer'

    CourseID = db.Column(db.Integer)
    ClassID = db.Column(db.Integer, primary_key=True)
    TrainerID = db.Column(db.Integer, primary_key=True)

    def __init__(self, CourseID, ClassID, TrainerID):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.TrainerID = TrainerID
    
    def json(self):
        if not hasattr(self, "CourseTitle"):
            self.CourseTitle = ''
        if not hasattr(self, 'ClassStartDate'):
            self.ClassStartDate = ''
        if not hasattr(self, 'ClassEndDate'):
            self.ClassEndDate = ''
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "TrainerID": self.TrainerID, "CourseTitle": self.CourseTitle, "ClassStartDate": self.ClassStartDate, "ClassEndDate": self.ClassEndDate}


class User(db.Model):
    __tablename__ = 'userTable'

    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(200), nullable=False)
    UserType = db.Column(db.String(200), nullable=False)

    def __init__(self, UserID, UserName, UserType):
        self.UserID = UserID
        self.UserName = UserName
        self.UserType = UserType
    
    def json(self):
        return {"UserID": self.UserID, "UserName": self.UserName, "UserType": self.UserType}


class Section(db.Model):
    __tablename__ = 'section'

    CourseID = db.Column(db.Integer, nullable=False)
    ClassID = db.Column(db.Integer, nullable=False)
    SectionID = db.Column(db.Integer, primary_key=True)
    SectionName = db.Column(db.Text)

    def __init__(self, CourseID, ClassID, SectionName=''):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.SectionName = SectionName
    
    def json(self):
        if not hasattr(self, "SectionMaterialList"):
            self.SectionMaterialList = []
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "SectionID": self.SectionID,"SectionName": self.SectionName, "SectionMaterialList": self.SectionMaterialList}


class StudentQuizResult(db.Model):
    __tablename__ = 'studentQuizResult'

    '''
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    QuizID INT NOT NULL,
    LearnerID INT NOT NULL,
    Grade INT NOT NULL,
    AttemptID INT NOT NULL AUTO_INCREMENT,
    '''

    CourseID = db.Column(db.Integer, nullable=False)
    ClassID = db.Column(db.Integer, nullable=False)
    SectionID = db.Column(db.Integer, nullable=False)
    QuizID = db.Column(db.Integer, nullable=False)
    LearnerID = db.Column(db.Integer, nullable=False)
    Grade = db.Column(db.Integer, nullable=False)
    AttemptID = db.Column(db.Integer, primary_key=True)

    def __init__(self, CourseID, ClassID, SectionID, QuizID, LearnerID, Grade=0):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.SectionID = SectionID
        self.QuizID = QuizID
        self.LearnerID = LearnerID
        self.Grade = Grade

    def json(self):
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "SectionID": self.SectionID, "QuizID": self.QuizID, "LearnerID": self.LearnerID, "Grade": self.Grade}


# ungraded quiz
class Quiz(db.Model):
    __tablename__ = 'quiz'

    QuizID = db.Column(db.Integer, primary_key = True)
    CourseID = db.Column(db.Integer, nullable=False)
    ClassID = db.Column(db.Integer, nullable=False)
    SectionID = db.Column(db.Integer, nullable=False)
    QuizTitle = db.Column(db.String(50), nullable=False)
    QuizTimer = db.Column(db.Integer, nullable=False)

    def __init__(self, CourseID, ClassID, SectionID, QuizTitle, QuizTimer):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.SectionID = SectionID
        self.QuizTitle = QuizTitle
        self.QuizTimer = QuizTimer

    def json(self):
        return{"QuizID": self.QuizID, "CourseID": self.CourseID, "ClassID": self.ClassID, "SectionID": self.SectionID, "QuizTitle": self.QuizTitle, "QuizTimer": self.QuizTimer}


class Question(db.Model):
    __tablename__ = 'question'

    QuestionID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, nullable=False)
    ClassID = db.Column(db.Integer, nullable=False)
    SectionID = db.Column(db.Integer, nullable=False)
    QuizID = db.Column(db.Integer, nullable=False)
    QuestionContent = db.Column(db.Text, nullable=False)


    def __init__(self, CourseID, ClassID, SectionID, QuizID, QuestionContent):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.SectionID = SectionID
        self.QuizID = QuizID
        self.QuestionContent = QuestionContent
    
    def json(self):
        return{"QuestionID": self.QuestionID, "CourseID": self.CourseID, "ClassID": self.ClassID, "SectionID": self.SectionID, "QuizID": self.QuizID, "QuestionContent": self.QuestionContent}


class QuestionAnswer(db.Model):
    __tablename__ = 'questionAnswer'

    AnswerID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, nullable=False)
    ClassID = db.Column(db.Integer, nullable=False)
    SectionID = db.Column(db.Integer, nullable=False)
    QuizID = db.Column(db.Integer, nullable=False)
    QuestionID = db.Column(db.Integer, nullable=False)
    AnswerContent = db.Column(db.Text, nullable=False)
    Correct = db.Column(db.Boolean, nullable=False)


    def __init__(self, CourseID, ClassID, SectionID, QuizID, QuestionID, AnswerContent, Correct):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.SectionID = SectionID
        self.QuizID = QuizID
        self.QuestionID = QuestionID
        self.AnswerContent = AnswerContent
        self.Correct = Correct
    
    def json(self):
        return{"AnswerID": self.AnswerID, "CourseID": self.CourseID, "ClassID": self.ClassID, "SectionID": self.SectionID, "QuizID": self.QuizID, "QuestionID": self.QuestionID, "AnswerContent": self.AnswerContent, "Correct": self.Correct}


class StudentAnswer(db.Model):
    __tablename__ = 'studentAnswer'

    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    SectionID = db.Column(db.Integer, primary_key=True)
    QuizID = db.Column(db.Integer, primary_key=True)
    QuestionID = db.Column(db.Integer, primary_key=True)
    LearnerID = db.Column(db.Integer, primary_key=True)
    AnswerID = db.Column(db.Integer, nullable=False)
    AttemptID = db.Column(db.Integer, primary_key=True)


    def __init__(self, CourseID, ClassID, SectionID, QuizID, QuestionID, LearnerID, AnswerID, AttemptID):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.SectionID = SectionID
        self.QuizID = QuizID
        self.QuestionID = QuestionID
        self.LearnerID = LearnerID
        self.AnswerID = AnswerID
        self.AttemptID = AttemptID
    
    def json(self):
        return{"CourseID": self.CourseID, "ClassID": self.ClassID, "SectionID": self.SectionID, "QuizID": self.QuizID, "QuestionID": self.QuestionID, "LearnerID": self.LearnerID, "AnswerID": self.AnswerID, "AttemptID": self.AttemptID}


# graded quiz
class FinalQuiz(db.Model):
    __tablename__ = 'finalQuiz'

    QuizID = db.Column(db.Integer, primary_key = True)
    CourseID = db.Column(db.Integer, nullable=False)
    QuizTitle = db.Column(db.String(50), nullable=False)
    QuizTimer = db.Column(db.Integer, nullable=False)

    def __init__(self, CourseID, QuizTitle, QuizTimer):
        self.CourseID = CourseID
        self.QuizTitle = QuizTitle
        self.QuizTimer = QuizTimer

    def json(self):
        return{"QuizID": self.QuizID, "CourseID": self.CourseID, "QuizTitle": self.QuizTitle, "QuizTimer": self.QuizTimer}


class FinalQuizQuestion(db.Model):
    __tablename__ = 'finalQuizQuestion'

    QuestionID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, nullable=False)
    QuizID = db.Column(db.Integer, nullable=False)
    QuestionContent = db.Column(db.Text, nullable=False)


    def __init__(self, CourseID, QuizID, QuestionContent):
        self.CourseID = CourseID
        self.QuizID = QuizID
        self.QuestionContent = QuestionContent
    
    def json(self):
        return{"QuestionID": self.QuestionID, "CourseID": self.CourseID, "QuizID": self.QuizID, "QuestionContent": self.QuestionContent}


class FinalQuizQuestionAnswer(db.Model):
    __tablename__ = 'finalQuizQuestionAnswer'

    AnswerID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, nullable=False)
    QuizID = db.Column(db.Integer, nullable=False)
    QuestionID = db.Column(db.Integer, nullable=False)
    AnswerContent = db.Column(db.Text, nullable=False)
    Correct = db.Column(db.Boolean, nullable=False)


    def __init__(self, CourseID, QuizID, QuestionID, AnswerContent, Correct):
        self.CourseID = CourseID
        self.QuizID = QuizID
        self.QuestionID = QuestionID
        self.AnswerContent = AnswerContent
        self.Correct = Correct
    
    def json(self):
        return{"AnswerID": self.AnswerID, "CourseID": self.CourseID, "QuizID": self.QuizID, "QuestionID": self.QuestionID, "AnswerContent": self.AnswerContent, "Correct": self.Correct}


def security_input_check(text):
    return True


@app.route('/get-learner-quiz/<string:LearnerID>/<string:CourseID>/<string:ClassID>')
def get_quiz_attempts(LearnerID, CourseID, ClassID):
    sections = db.session.query(Section.SectionID).filter_by(CourseID = CourseID).filter_by(ClassID = ClassID).all()
    result = db.session.query(StudentQuizResult.SectionID).filter_by(CourseID = CourseID).filter_by(ClassID = ClassID).filter_by(LearnerID = LearnerID).all()
    print(sections)
    allowed_sections = []
    for a_section in sections:
        if a_section not in result:
            allowed_sections.append(a_section[0])
            break
        else:
            allowed_sections.append(a_section[0])
   
    return {'allowed_sections': allowed_sections}


@app.route('/view-section/<string:CourseID>/<string:ClassID>')
def show_section(CourseID, ClassID):
    pass
    sections = Section.query.filter_by(CourseID = CourseID).filter_by(ClassID = ClassID).all()
    sections_count = Section.query.filter_by(CourseID = CourseID).filter_by(ClassID = ClassID).count()
    '''
    CourseID = db.Column(db.Integer)
    ClassID = db.Column(db.Integer)
    SectionID = db.Column(db.Integer)
    MaterialID = db.Column(db.Integer, primary_key=True)
    MaterialContent = db.Column(db.Text)
    '''
    section_list = []
    print(sections)
    for i in range(sections_count):
        section_courseid = sections[i].CourseID
        section_classid = sections[i].ClassID
        section_sectionid = sections[i].SectionID
        section_material_list = SectionMaterial.query.filter_by(SectionID = section_sectionid)
        material_list = []
        for a_material in section_material_list:
            material_list.append(a_material)
        section_list.append([sections[i], material_list])
    actual_section = []
    for i in range(len(section_list)):
        section_list[i][0].SectionMaterialList = [section_mat.json() for section_mat in section_list[i][1]]
        actual_section.append(section_list[i][0])    
    if len(sections) > 0:
        return {
            "code": 200,
            "data": [a_section.json() for a_section in actual_section]
        }


@app.route('/open-material/<string:CourseID>/<string:ClassID>/<string:SectionID>/<string:MaterialContent>/<string:LearnerID>')
def open_material(CourseID, ClassID, SectionID, MaterialContent, LearnerID):
    opened = MaterialProgress.query.filter_by(CourseID = CourseID, ClassID=ClassID, SectionID=SectionID, MaterialContent = MaterialContent, LearnerID = LearnerID).first()
    if not opened:
        try:
            db.session.add(MaterialProgress(CourseID, ClassID, SectionID, MaterialContent, LearnerID))
            db.session.commit()
            return jsonify({
                "code": 201,
                "message": "Progress updated"
            })
        except:
            return jsonify({
                "code": 500,
                "message": "An error occurred"
            })
    else:
        return jsonify({
            "code": 400,
            "message": "Progress already made before"
        })


@app.route('/check-opened-material/<string:CourseID>/<string:ClassID>/<string:SectionID>/<string:MaterialContent>/<string:LearnerID>')
def check_opened(CourseID, ClassID, SectionID, MaterialContent, LearnerID):
    opened = MaterialProgress.query.filter_by(CourseID = CourseID, ClassID=ClassID, SectionID=SectionID, MaterialContent = MaterialContent, LearnerID = LearnerID).first()
    if opened:
        return jsonify({
            'code': 200,
            'message': 'OPENED'
        }), 200
    else:
        return jsonify({
            'code': 404,
            'message': 'NOT OPENED'
        }), 404


@app.route('/uploader-section-name/<string:CourseID>/<string:ClassID>/<string:SectionID>', methods=['POST'])
def update_section_name(CourseID, ClassID, SectionID):
    data = request.get_json()
    section_name = data['SectionName']
    section = Section.query.filter_by(SectionID=SectionID).first()
    section.SectionName = section_name
    db.session.commit()
   

@app.route('/uploader/<string:CourseID>/<string:ClassID>/<string:SectionID>', methods = ['POST'])
def add_material_link(CourseID, ClassID, SectionID):
    data = request.get_json()
    print(data)
    for a_link in data:
        material_title = a_link['title']
        material_content_raw = a_link['link']
        if security_input_check(material_title) and security_input_check(material_content_raw):
            material_content = '<a href="https://' + material_content_raw + '"> ' + material_title + '</a>'
            section_material = SectionMaterial(CourseID, ClassID, SectionID, material_content)
            db.session.add(section_material)
    try:
        db.session.commit()
    except:
        return {
            'code': 500,
            'message': 'Upload Links Failed'
        }
    return {
        'code': 201,
        'message': 'Upload Links Sucessful'
    }


@app.route('/uploader-file/<string:CourseID>/<string:ClassID>/<string:SectionID>', methods = ['POST'])
def add_material_file(CourseID, ClassID, SectionID):
    files = request.files
    for file in files:
        section_material = SectionMaterial(CourseID, ClassID, SectionID, files[file].filename)
        section_material.create_path()
        files[file].save('static/course_material/{}/{}/{}/{}'.format(CourseID, ClassID, SectionID, files[file].filename))
        db.session.add(section_material)
    try:
        db.session.commit()
    except:
        return {
            'code': 500,
            'message': 'Upload Files Failed'
        }
    return {
        'code': 201,
        'message': 'Upload Files Sucessful'
    }


@app.route('/create-section', methods=['POST'])
def create_section():
    data = request.get_json()
    courseid = data['CourseID']
    classid = data['ClassID']
    section_name = data['SectionName']
    
    section = Section(courseid, classid, section_name)
    
    try:
        db.session.add(section)
        db.session.flush()
        db.session.commit()
        return jsonify({
            "code": 201,
            "data": section.json()
            }), 201
    except:
        return jsonify({
            "code": 500,
            "message": "An error has occurred"
        }), 500

# def upload_file(CourseID, ClassID, SectionID):

#     # How to get courseid, classid, sectionid from page?

#     # see flask render_template()

#    if request.method == 'POST':
#       f = request.files.getlist("file")
#       for a_file in f:
#           # 1. make an object out of each file with a_file.filename as MaterialContent
#           # 2. call create_path() for the first object
#           # 3. Insert the file into course_material/
#           # 4. Make a call to database to record the file
#           path = 'course_material/' + None # Will change None to path for CourseID, ClassID, and SectionID
#           a_file.save(path + a_file.filename)
#       return 'file uploaded successfully'
    

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


@app.route('/classes')
def get_all_classes():
    classes = CourseClass.query.all()
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
    if (CourseClass.query.filter_by(ClassID=ClassID).first()):
        return jsonify({
            "code": 200,
            "message": "Class exists" 
        }), 201
    else:
        return jsonify({
            "code": 404,
            "message": "Class doesn't exist"
        }), 404


@app.route('/courseprereq')
def get_prereq():
    prereqs = CoursePrereq.query.all()
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


@app.route('/courses-all/<string:UserID>')
def get_all_courses(UserID):
    enrolled_courses = []
    takenClasses = ClassTaken.query.filter_by(LearnerID = UserID)
    applied_courses = []
    prereq_courses = []
    rejected_courses = []
    takenPrereq = ClassTaken.query.filter(ClassTaken.ApplicationStatus == 'completed', ClassTaken.LearnerID == UserID)
    for prereq in takenPrereq:
        prereq_courses.append(prereq.CourseID)
    for a_class in takenClasses:
        if a_class.ApplicationStatus == 'hr_enrolled': # check if user already enrolled
            enrolled_courses.append(a_class.CourseID)
        elif a_class.ApplicationStatus == 'self_enrolled' or a_class.ApplicationStatus == 'self_approved':
            applied_courses.append([a_class.CourseID, a_class.ClassID])
        elif a_class.ApplicationStatus == 'rejected':
            rejected_courses.append([a_class.CourseID, a_class.ClassID])
    courses = Course.query.filter(~Course.CourseID.in_(enrolled_courses), ~Course.CourseID.in_(prereq_courses)) # '~' refers to not (a negate function)
    class_per_course = []
    for a_course in courses:
        shown_classes = []
        prereqList = []
        CourseID = a_course.CourseID
        course_prereqs = CoursePrereq.query.filter_by(CourseID = CourseID)
        for a_prereq in course_prereqs:
            prereqName = Course.query.filter_by(CourseID = a_prereq.PrereqID).first().CourseTitle
            prereqList.append(prereqName)
            if a_prereq.PrereqID not in prereq_courses:
                a_course.GreyOut = True
        a_course.prereqList = prereqList
        now = datetime.now()
        classes = CourseClass.query.filter(CourseID == a_course.CourseID, now <= CourseClass.RegistrationEndDate, now >= CourseClass.RegistrationStartDate) # check registration date
        for a_class in classes:
            '''
            CHECK IF ALREADY APPLIED --> GREY OUT AND SHOW 'APPLIED'
            '''
            currentTrainers = TrainerClass.query.filter_by(CourseID = a_class.CourseID).filter_by(ClassID = a_class.ClassID)
            trainerList = []
            if currentTrainers.count() > 0:
                for a_trainer in currentTrainers:
                    trainerInfo = a_trainer.json()
                    trainerObj = User.query.filter(User.UserID == trainerInfo['TrainerID'])
                    for item in trainerObj:
                        trainerName = item.json()['UserName']
                    trainerList.append(trainerName)
            if [a_class.CourseID, a_class.ClassID] in applied_courses:
                a_class.GreyOut = True
                a_class.Status = 'applied'
            if [a_class.CourseID, a_class.ClassID] in rejected_courses:
                a_class.Status = 'rejected'
            currentlyEnrolled = ClassTaken.query.filter(CourseID == a_class.CourseID, ClassTaken.ClassID == a_class.ClassID, ClassTaken.ApplicationStatus.in_(["hr_enrolled", "self_approved"])) # check remaining class sizes
            totalEnrolled = currentlyEnrolled.count()
            print(totalEnrolled)
            if totalEnrolled < a_class.ClassSize and a_class.CourseID == a_course.CourseID:
                a_class.RemainingSlot = a_class.ClassSize - totalEnrolled
                a_class.TrainerList = trainerList
                shown_classes.append(a_class)
            trainerList = []
        class_per_course.append([a_course, shown_classes])
    actual_courses = [] 
    # By logic, the step from here below is not needed, but SQLAlchemy magic works in a very weird way :).. -- Each course may have been reset to its default values, so classList is gone except for the last course, so I had to repopulate myself courses myself.
    for i in range(0, len(class_per_course)):
        class_per_course[i][0].classList = [each_class.json() for each_class in class_per_course[i][1]]
        actual_courses.append(class_per_course[i][0])
    if courses.count():
        return jsonify({
            "code": 200,
            "data": {
                "courses": [each_course.json() for each_course in actual_courses]
            }
        }), 200
    return jsonify({
        "code": 404,
        "message": "There are no courses."
    }), 404


@app.route('/self-enrol', methods=['POST'])
def self_enrol():
    data = request.get_json()
    userID = data['UserID']
    courseID = data['CourseID']
    classID = data['ClassID']
    
    apply_class = ClassTaken(courseID, classID, userID, 'applied')

    check = ClassTaken.query.filter_by(CourseID=courseID, ClassID=classID, LearnerID=userID, ApplicationStatus='rejected').first()
    if check:
        try:
            db.session.add(apply_class)
            db.session.commit()
        except:
            return jsonify(
            {
                    "code": 500,
                    "message": "An error occurred in applying to class."
            }
        ), 500
    else:
        try:
            db.session.add(apply_class)
            db.session.commit()
        except:
            return jsonify(
                {
                        "code": 500,
                        "message": "An error occurred in applying to class."
                }
            ), 500
    
    return jsonify(
        {
            "code": 201,
            "message": "Applied to class sucessfully",
            "data": apply_class.json()
        }
    ), 201


@app.route('/withdraw-application/<int:CourseID>/<int:ClassID>/<int:UserID>', methods=['POST'])
def withdraw_application(CourseID, ClassID, UserID):
    ClassTaken.query.filter_by(CourseID = CourseID).filter_by(ClassID = ClassID).filter_by(LearnerID = UserID).delete()
    try:
        db.session.commit()
        return jsonify({
            "code": 201,
            "message": "Successfully withdrawn"
        })
    except:
        return jsonify({
            "code": 500,
            "message": "An error occurred in withdrawing class application"
        }), 500


@app.route('/user-role/<string:UserID>')
def get_user_role(UserID):
    user = User.query.filter_by(UserID=UserID).first()

    if (user):
        return jsonify({
            "code": 200,
            "data": {
                "UserRole": user.UserType
            }
        })
    return jsonify({
        "code": 404,
        "message": "There are no classes."
    }), 404


@app.route('/classes-taught/<string:UserID>')
def get_classes_taught(UserID):
    classes = TrainerClass.query.filter_by(TrainerID=UserID).all()
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


@app.route('/course-details/<string:CourseID>')
def get_course_details(CourseID):
    c = Course.query.filter_by(CourseID=CourseID).first()

    if (c):
        return jsonify({
            "code": 200,
            "data": {
                "course": c.json()
            }
        })
    return jsonify({
        "code": 404,
        "message": "There are no classes."
    }), 404


@app.route('/remove-material', methods=['POST'])
def remove_material():
    data = request.get_json()
    courseID = data['CourseID']
    classID = data['ClassID']
    sectionID = data['SectionID']
    material_content = data['MaterialContent']

    material = SectionMaterial.query.filter_by(CourseID=courseID, ClassID=classID, SectionID=sectionID, MaterialContent=material_content).first()
    if os.path.exists('static/course_material/' + str(courseID) + '/' + str(classID) + '/' + str(sectionID) + '/' + str(material_content)):
        os.remove('static/course_material/' + str(courseID) + '/' + str(classID) + '/' + str(sectionID) + '/' + str(material_content))
    
    db.session.delete(material)
    db.session.commit()

    return jsonify({
        "code": 200,
        "message": "Deletion of material is successful"
    }), 200


@app.route('/class-details/<string:ClassID>')
def get_class_details(ClassID):
    c = CourseClass.query.filter_by(ClassID=ClassID).first()

    if (c):
        return jsonify({
            "code": 200,
            "data": {
                "class": c.json()
            }
        })
    return jsonify({
        "code": 404,
        "message": "There are no classes."
    }), 404



@app.route('/get-section-quiz/<CourseID>/<ClassID>/<SectionID>/<LearnerID>')
def get_section_quiz(CourseID, ClassID, SectionID, LearnerID):
    materialProgress = MaterialProgress.query.filter_by(LearnerID=LearnerID, CourseID=CourseID, ClassID=ClassID, SectionID=SectionID).count()
    sectionMaterialCount = SectionMaterial.query.filter_by(CourseID=CourseID, ClassID=ClassID, SectionID=SectionID).count()
    print(materialProgress)
    quiz = Quiz.query.filter_by(CourseID=CourseID, ClassID=ClassID, SectionID=SectionID).first()
    if materialProgress == sectionMaterialCount:    
        return jsonify({
            "code": 200,
            "data": quiz.json(),
            "greyOut": False
        })
    else:
        return jsonify({
            "code": 200,
            "data": quiz.json(),
            "greyOut": True
        })

@app.route('/get-section-quiz-trainer/<CourseID>/<ClassID>/<SectionID>')
def get_section_quiz_trainer(CourseID, ClassID, SectionID):

    quiz = Quiz.query.filter_by(CourseID=CourseID, ClassID=ClassID, SectionID=SectionID).first()
    if quiz:    
        return jsonify({
            "code": 200,
            "data": quiz.json()
        })
    else:
        return jsonify({
            "code": 404,
            "message": "No quizzes found for this section"
        })
    
# for ungraded quiz
@app.route('/create_quiz', methods=["POST"])
def create_quiz():

    data = request.get_json()
    print(data)

    quiz = Quiz(**data)

    try:
        db.session.add(quiz)    
        db.session.commit()
    
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the quiz."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "message": "Quiz is successfully created",
            "data": {
                "QuizID": quiz.QuizID
            }
        }
    ), 201     


@app.route('/create_question', methods=["POST"])
def create_question():

    data = request.get_json()
    print(data)

    question = Question(**data)

    try:
        db.session.add(question)    
        db.session.commit()
    
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the question."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "message": "Question is successfully created",
            "data": {
                "QuestionID": question.QuestionID
            }
        }
    ), 201     


@app.route('/create_answer', methods=["POST"])
def create_answer():

    data = request.get_json()
    print(data)

    answer = QuestionAnswer(**data)

    try:
        db.session.add(answer)    
        db.session.commit()
    
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the answer."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "message": "Answer is successfully created"
        }
    ), 201     


# for graded quiz
@app.route('/create_graded_quiz', methods=["POST"])
def create_graded_quiz():

    data = request.get_json()
    print(data)

    final_quiz = FinalQuiz(**data)

    try:
        db.session.add(final_quiz)    
        db.session.commit()
    
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the final quiz."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "message": "Final quiz is successfully created",
            "data": {
                "QuizID": final_quiz.QuizID
            }
        }
    ), 201     


@app.route('/create_graded_question', methods=["POST"])
def create_graded_question():

    data = request.get_json()
    print(data)

    final_quiz_question = FinalQuizQuestion(**data)

    try:
        db.session.add(final_quiz_question)    
        db.session.commit()
    
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the question."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "message": "Question is successfully created",
            "data": {
                "QuestionID": final_quiz_question.QuestionID
            }
        }
    ), 201    


@app.route('/create_graded_answer', methods=["POST"])
def create_graded_answer():

    data = request.get_json()
    print(data)

    final_quiz_answer = FinalQuizQuestionAnswer(**data)

    try:
        db.session.add(final_quiz_answer)    
        db.session.commit()
    
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the answer."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "message": "Answer is successfully created"
        }
    ), 201     


# get ungraded quiz
@app.route('/get_quiz/<string:QuizID>')
def get_quiz(QuizID):
    get_quiz_content = Quiz.query.filter(Quiz.QuizID == QuizID).first()
    get_quiz_questions = Question.query.filter(Question.QuizID == QuizID).all()
    get_quiz_answers = QuestionAnswer.query.filter(QuestionAnswer.QuizID == QuizID).all()
    if get_quiz_content:
        return jsonify({
            "code": 200,
            "data":{
                "Quiz": get_quiz_content.json(),
                "Questions":
                    [question.json() for question in get_quiz_questions],
                "Answers":
                    [answer.json() for answer in get_quiz_answers]                
            }
        })
    return jsonify({
        "code":400,
        "message":"There is  no quiz"
    }), 404


#post student answers for ungraded quiz
@app.route('/post_ans', methods=["POST"])
def post_ans():
    data = request.get_json()
    print(data)

    stu_answer = StudentAnswer(**data)

    try:
        db.session.add(stu_answer)    
        db.session.commit()
    
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the answer."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "message": "Answer is successfully sent"
        }
    ), 201     


#post student result for ungraded quiz
@app.route('/post_result', methods=["POST"])
def post_result():
    data = request.get_json()
    print(data)

    stu_result = StudentQuizResult(**data)

    try:
        db.session.add(stu_result)    
        db.session.commit()
    
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating student's result."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "message": "Result is successfully created",
            "data": {
                "AttemptID": stu_result.AttemptID
            }
        }
    ), 201     


@app.route('/learner-courses', methods=["POST"])
def get_course_learner():

    data = request.get_json()
    print(data['data'])

    #to get the respective list from the html
    CourseID = []
    ClassID = []
    for learner in data['data']:
        CourseID.append(learner['CourseID'])
        ClassID.append(learner['ClassID'])
    
    #geting data from the course table based on the course IDs
    course_output = Course.query.filter(Course.CourseID.in_(CourseID))

    #getting the data from the database fron the class table
    class_retrive = []
    for i in range(len(CourseID)):
        end_data_output = CourseClass.query.filter((CourseClass.CourseID == CourseID[i]) & (CourseClass.ClassID == ClassID[i])).all()
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


@app.route('/user/<string:UserID>')
def get_acct_details(UserID):
    user = User.query.filter_by(UserID = UserID).all()
    Courses = ClassTaken.query.filter_by(LearnerID = UserID).all()
    
    if len(user) and len(Courses):
        return jsonify({
            "code": 200,
            "data":{
                "user_details": [user_detail.json() for user_detail in user], 
                "learner_courses": [course.json() for course in Courses]
            }
        })
    return jsonify({
        "code": 404,
        "message": "There are no such user"
    }), 404


@app.route('/HrAssign', methods=["POST"])
def get_learner():
    data = request.get_json()
    # print(data['CourseID'])

    #i am assuming i can get the assigning courseID from previous pages!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11111111111111
    prereqIDs = CoursePrereq.query.filter_by(CourseID = data['CourseID']).all()
    #print(prereqIDs)

    #to get the prereq IDs of the course that is being assigned
    prereqID_list = []
    for prereqID in prereqIDs:
        prereqID_list.append(prereqID.json()['PrereqID'])
    # print("Pre req id list")
    # print(prereqID_list)

    #to get the learner IDs that has completed the prereq of the course is being assigned
    #if there is any prereq, then it will get those learner that has completed the prereq course
    learnerID_list = []
    if len(prereqID_list):
        learnerIDs = ClassTaken.query.filter(ClassTaken.CourseID.in_(prereqID_list)).all()
        # print("here")
        # print(learnerIDs)
        for learnerID in learnerIDs:
            status = learnerID.json()['ApplicationStatus']
            if status == 'completed':
                learnerID_list.append(learnerID.json()['LearnerID'])
        # print("Learner id")
        # print(learnerID_list)
        Users = User.query.filter(User.UserID.in_(learnerID_list)).all()
        # print(learnerID_list)
        # print(Users)
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
    #print(data)

    class_details = CourseClass.query.filter_by(ClassID = data['ClassID'][0]).all()
    #number of learner in the class currently
    num_learner = len(ClassTaken.query.filter_by(ClassID = data['ClassID'][0]).all())
    
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
        check = ClassTaken.query.filter((ClassTaken.CourseID == k[0]) & (ClassTaken.ClassID == k[1]) & (ClassTaken.LearnerID == k[2]))
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
            #print(i)
            upload_data = {'CourseID': i[0], 'ClassID': i[1], 'LearnerID': i[2], 'ApplicationStatus': i[3]}
            upload = ClassTaken(**upload_data)
            db.session.add(upload)
            db.session.commit()
            output.append(upload_data)
        return jsonify({
        "code": 201,
        "data": output,
        "message": "Engineers has been successfully applied for the course"
        }), 201
    else:
        return jsonify({
        "code": 501,
        "available_seat": class_availability,
        "message": "There is no enough slot for this class."
        }), 501


@app.route('/learner_distribution_chart/<string:ClassID>')
def distribution(ClassID):
    #get all the learnerID using the classID
    learners = ClassTaken.query.filter_by(ClassID = ClassID).all()

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

    #print(status_output)

    #_____________________________________________________________________Number of completed sections in the class (section status)____________________________
    

    # sections = MaterialProgress.query.filter_by(ClassID = ClassID).all()

    # #section_output = {"Section1":{'completed':0, "imcomplete":0}, "Section2":{...}}

    # section_output = {}
    # for section in sections:
    #     #print(section.json()['SectionID'])
    #     if section.json()['SectionID'] in section_output:
    #         if section.json()['STATUS'] == 1:
    #             section_output[section.json()['SectionID']]['completed'] += 1
    #         else:
    #             section_output[section.json()['SectionID']]['incomplete'] += 1
    #     else:
    #         section_output[section.json()['SectionID']] = {'completed':0, 'incomplete':0}

    #print(section_output)

    #_____________________________________________________________________Final quiz distribution____________________________
    
    final_grades = FinalStudentQuizResult.query.filter_by(ClassID=ClassID).all()

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


    section_quiz_result = StudentQuizResult.query.filter_by(ClassID=ClassID).all()

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
            # "section_status": section_output,
            "final_grade":final_grade_output,
            "section_quiz_result": quiz_result_output
        }
    })

#Get All Courses
@app.route('/courses')
def get_all_courses_hr():
    all_courses = Course.query.all()
    print(all_courses)
    return jsonify({
            "code": 200,
            "message": "Course exists",
            "data": {
                "course": [course.json() for course in all_courses]
            }
        })

#Create Course
@app.route("/create_course", methods=["POST"])
def create_course():
    data = request.get_json()
    print(data)
    CourseTitle = data['CourseTitle']
    CourseDescription = data['CourseDescription']
    Badge = data['Badge']
    prereqList = data['prereqList']
    course = Course(None, CourseTitle, CourseDescription, Badge)

    db.session.add(course)
    db.session.commit()

    if prereqList:
        for prereq in prereqList:
            coursePrereq = CoursePrereq(course.CourseID, prereq)
            print(coursePrereq)
            db.session.add(coursePrereq)

    db.session.commit()
     
    return jsonify(
        {
            "code": 201,
            "message": "Course is successfully created",
            "data": course.json()
            
        }
    ), 201

#Get All Trainers
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

#Create Class
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
    TrainerIDList = data['TrainerIDList']
    cl = CourseClass(CourseID, None, StartDate, EndDate, ClassSize, RegistrationStartDate, RegistrationEndDate)

    db.session.add(cl)
    db.session.commit()

    for TrainerID in TrainerIDList:
        classTrainer = TrainerClass(CourseID, cl.ClassID, TrainerID)
        print(classTrainer)
        db.session.add(classTrainer)
    db.session.commit()

    return jsonify(
        {
            "code": 201,
            "message": "Class is successfully created"
        }
    ), 201


@app.route("/learner_ongoing_courses/<string:UserID>")
def get_leaner_ongoing_courses(UserID):
    Courses = ClassTaken.query.filter(ClassTaken.LearnerID == UserID, ClassTaken.ApplicationStatus.in_(['ongoing', 'self_approved', 'hr_enrolled'])).all()

    if len(Courses):
        print(Courses)
        for a_course in Courses:
            print(a_course)
            CourseID = a_course.CourseID
            print(CourseID)
            a_class_list = ClassTaken.query.filter_by(LearnerID = UserID, CourseID = CourseID).first()
            a_class_details = CourseClass.query.filter_by(ClassID = a_class_list.ClassID).first()
            a_course_title = Course.query.filter_by(CourseID = CourseID).first()
            a_course.CourseTitle = a_course_title.CourseTitle
            a_course.course_class_id = a_class_list.ClassID 
            a_course.class_start_date = a_class_details.StartDate
            a_course.ApplicationStatus = a_class_list.ApplicationStatus
            a_course.class_end_date = a_class_details.EndDate 
            print(a_class_list)
            print("LearnerID", a_course.LearnerID)
            print('EACH COURSE CLASS ID', a_course.course_class_id)
            
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


@app.route('/create-new-section/<CourseID>/<ClassID>')
def create_section_page(CourseID, ClassID):
    return render_template('create-section.html', CourseID=CourseID, ClassID=ClassID)


@app.route('/add-section-material/<CourseID>/<ClassID>/<SectionID>/<SectionName>')
def test_template(CourseID, ClassID, SectionID, SectionName):
    return render_template('add-section-material.html', CourseID=CourseID, ClassID=ClassID, SectionID=SectionID, SectionName=SectionName)


@app.route('/view-section-material/<CourseID>/<ClassID>')
def section_material_template(CourseID, ClassID):
    return render_template('view-section-material-student.html', CourseID=CourseID, ClassID=ClassID)


@app.route('/view-material/<CourseID>/<ClassID>/<SectionID>/<url>')
def view_material(CourseID, ClassID, SectionID, url):
    allowed_sections = get_quiz_attempts('1', CourseID, ClassID)['allowed_sections']
    
    if int(SectionID) in allowed_sections:
        return render_template('view-file.html', CourseID=CourseID, ClassID=ClassID, SectionID=SectionID, url=url)
    else:
        abort(403)


@app.route('/after-assign')
def after_assign():
    return render_template('after-assign.html')


@app.route('/create-ungraded-quiz/<CourseID>/<ClassID>/<SectionID>')
def create_ungraded_quiz_template(CourseID, ClassID, SectionID):
    return render_template('create-ungraded-quiz.html', CourseID=CourseID, ClassID=ClassID, SectionID=SectionID)


@app.route('/create-graded-quiz/<CourseID>')
def create_graded_quiz_template(CourseID):
    return render_template('create-graded-quiz.html', CourseID=CourseID)


@app.route('/view-section-trainer/<CourseID>/<ClassID>')
def view_section_page_trainer(CourseID, ClassID):
    return render_template('view-section-material-trainer.html', CourseID=CourseID, ClassID=ClassID)


@app.route('/take-ungraded-quiz/<QuizID>')
def take_ungraded_quiz(QuizID):
    return render_template('take-ungraded-quiz.html',QuizID=QuizID)


@app.route('/timeout/<CourseID>/<ClassID>')
def timeout(CourseID, ClassID):
    return render_template('timeout.html', CourseID=CourseID, ClassID=ClassID)


@app.route('/successful-submission/<CourseID>/<ClassID>')
def successful_submission(CourseID, ClassID):
    return render_template('successful-submission.html', CourseID=CourseID, ClassID=ClassID)


@app.route('/successful-creation/<CourseID>/<ClassID>')
def successful_creation(CourseID, ClassID):
    return render_template('successful-creation.html', CourseID=CourseID, ClassID=ClassID)


@app.route('/successful-creation-hr')
def successful_creation_hr():
    return render_template('successful-creation-hr.html')


@app.route('/view-courses')
def view_course_hr():
    return render_template('view-courses.html')


@app.route('/create-class/<CourseID>')
def create_class_hr(CourseID):
    return render_template('create-class.html', CourseID=CourseID)


@app.route('/create-course')
def create_course_hr():
    return render_template('create-course.html')


@app.route('/assign-learner/<CourseID>/<ClassID>')
def assign_learner(CourseID, ClassID):
    return render_template('assign-learner.html', CourseID=CourseID, ClassID=ClassID)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

