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
        if not hasattr(self, 'classList'):
            self.classList = []
        if not hasattr(self, 'GreyOut'):
            self.GreyOut = False
        if not hasattr(self, 'prereqList'):
            self.prereqList = []
        return{"CourseID": self.CourseID, "CourseTitle": self.CourseTitle, "CourseDescription": self.CourseDescription, "Badge": self.Badge, "classList": self.classList, "GreyOut": self.GreyOut, 'prereqList': self.prereqList}


class SectionMaterial(db.Model):
    __tablename__ = 'sectionMaterial'

    CourseID = db.Column(db.Integer)
    ClassID = db.Column(db.Integer)
    SectionID = db.Column(db.Integer)
    MaterialID = db.Column(db.Integer, primary_key=True)
    MaterialContent = db.Column(db.Text)
    '''
    CourseID INT NOT NULL,
    ClassID INT NOT NULL,
    SectionID INT NOT NULL,
    MaterialID INT NOT NULL AUTO_INCREMENT,
    MaterialContent TEXT NOT NULL,
    '''

    def __init__(self, CourseID, ClassID, SectionID, MaterialContent):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.SectionID = SectionID
        self.MaterialContent = MaterialContent

    def create_path(self):

        course_path = 'course_material/' + str(self.CourseID)
        class_path = 'course_material/' + str(self.CourseID) + '/' + str(self.ClassID)
        section_path = 'course_material/' + str(self.CourseID) + '/' + str(self.ClassID) + '/' + str(self.SectionID)

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
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "SectionID": self.SectionID, "MaterialID": self.MaterialID, "MaterialContent": self.MaterialContent}

def security_input_check(text):
    return True


class course_class(db.Model):
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


class course_prereq(db.Model):
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
        
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "LearnerID": self.LearnerID}



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
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "TrainerID": self.TrainerID}


class User(db.Model):
    __tablename__ = 'userTable'

    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.Integer)
    UserType = db.Column(db.Integer)

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

    def __init__(self, CourseID, ClassID, SectionID, QuizID, LearnerID, Grade):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.SectionID = SectionID
        self.QuizID = QuizID
        self.LearnerID = LearnerID
        self.Grade = Grade

    def json(self):
        return {"CourseID": self.CourseID, "ClassID": self.ClassID, "SectionID": self.SectionID, "QuizID": self.QuizID, "LearnerID": self.LearnerID, "Grade": self.Grade}
    
@app.route('/get-learner-quiz/<string:LearnerID>/<string:CourseID>/<string:ClassID>')
def get_quiz_attempts(LearnerID, CourseID, ClassID):
    sections = db.session.query(Section.SectionID).filter_by(CourseID = CourseID).filter_by(ClassID = ClassID).all()
    result = db.session.query(StudentQuizResult.SectionID).filter_by(CourseID = CourseID).filter_by(ClassID = ClassID).filter_by(LearnerID = LearnerID).all()
    allowed_sections = []
    for a_section in sections:
        if a_section not in result:
            allowed_sections.append(a_section[0])
            break
   
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
        files[file].save('course_material/{}/{}/{}/{}'.format(CourseID, ClassID, SectionID, files[file].filename))
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
    if (course.query.filter_by(CourseID=CourseID).first()):
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
    classes = course_class.query.all()
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
    if (course_class.query.filter_by(ClassID=ClassID).first()):
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
    prereqs = course_prereq.query.all()
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
    takenPrereq = ClassTaken.query.filter(ClassTaken.ApplicationStatus == 'completed', ClassTaken.LearnerID == UserID)
    for prereq in takenPrereq:
        prereq_courses.append(prereq.CourseID)
    for a_class in takenClasses:
        if a_class.ApplicationStatus == 'enrolled' or a_class.ApplicationStatus == 'self_enrolled': # check if user already enrolled
            enrolled_courses.append(a_class.CourseID)
        elif a_class.ApplicationStatus == 'applied':
            applied_courses.append([a_class.CourseID, a_class.ClassID])
    courses = course.query.filter(~course.CourseID.in_(enrolled_courses), ~course.CourseID.in_(prereq_courses)) # '~' refers to not (a negate function)
    class_per_course = []
    for a_course in courses:
        print(a_course.CourseID)
        shown_classes = []
        prereqList = []
        CourseID = a_course.CourseID
        course_prereqs = course_prereq.query.filter_by(CourseID = CourseID)
        for a_prereq in course_prereqs:
            prereqName = course.query.filter_by(CourseID = a_prereq.PrereqID).first().CourseTitle
            prereqList.append(prereqName)
            if a_prereq.PrereqID not in prereq_courses:
                a_course.GreyOut = True
        a_course.prereqList = prereqList
        now = datetime.now()
        print(now)
        classes = course_class.query.filter(CourseID == a_course.CourseID, now <= course_class.RegistrationEndDate, now >= course_class.RegistrationStartDate) # check registration date
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
            currentlyEnrolled = ClassTaken.query.filter(CourseID == a_class.CourseID, ClassTaken.ClassID == a_class.ClassID, ClassTaken.ApplicationStatus == "enrolled") # check remaining class sizes
            totalEnrolled = currentlyEnrolled.count()
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

'''testing render_template'''

@app.route('/test-render-template/<CourseID>/<ClassID>/<SectionID>')
def test_template(CourseID, ClassID, SectionID):
    return render_template('add-section-material.html', CourseID=CourseID, ClassID=ClassID, SectionID=SectionID)

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
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

