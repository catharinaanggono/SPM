from types import ClassMethodDescriptorType
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

class Quiz(db.Model):
    __tablename__ = 'quiz'

    QuizID = db.Column(db.Integer, primary_key = True)
    CourseID = db.Column(db.Integer, primary_key = True)
    ClassID = db.Column(db.Integer, primary_key = True)
    SectionID = db.Column(db.Integer, primary_key = True)
    QuizTitle = db.Column(db.String(50), nullable=False)
    QuizTimer = db.Column(db.Integer, nullable=False)
    PassingScore = db.Column(db.Integer, nullable=False)

    def __init__(self, CourseID, ClassID, SectionID, QuizTitle, QuizTimer, PassingScore):
        self.CourseID = CourseID
        self.ClassID = ClassID
        self.SectionID = SectionID
        self.QuizTitle = QuizTitle
        self.QuizTimer = QuizTimer
        self.PassingScore = PassingScore

    def json(self):
        return{"QuizID": self.QuizID, "CourseID": self.CourseID, "ClassID": self.ClassID, "SectionID": self.SectionID, "QuizTitle": self.QuizTitle, "QuizTimer": self.QuizTimer, "PassingScore": self.PassingScore}

class Question(db.Model):
    __tablename__ = 'question'

    QuestionID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, primary_key = True)
    ClassID = db.Column(db.Integer, primary_key = True)
    SectionID = db.Column(db.Integer, primary_key = True)
    QuizID = db.Column(db.Integer, primary_key = True)
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
    CourseID = db.Column(db.Integer, primary_key = True)
    ClassID = db.Column(db.Integer, primary_key = True)
    SectionID = db.Column(db.Integer, primary_key = True)
    QuizID = db.Column(db.Integer, primary_key = True)
    QuestionID = db.Column(db.Integer, primary_key=True)
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
            "message": "Question are successfully created"
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
            "message": "Answer are successfully created"
        }
    ), 201     

# @app.route('/create_question', methods=["POST"])
# def create_question():

#     data = request.get_json()
#     print(data)

#     CourseID = data['CourseID']
#     ClassID = data['ClassID']
#     SectionID = data['SectionID']
#     QuizID = data['QuizID']
#     QuestionContent = data['QuestionContent']
#     AnswerOptions = data['AnswerOptions']

#     question = Question(CourseID, ClassID, SectionID, QuizID, QuestionContent)

#     try:
#         db.session.add(question)    
#         db.session.commit()

#         for each_ans in AnswerOptions:
#             AnswerContent = data['AnswerOptions'][each_ans]['AnswerContent']
#             Correct = data['AnswerOptions'][each_ans]['Correct']
#             answer = QuestionAnswer(CourseID, ClassID, SectionID, QuizID, AnswerContent, Correct)
#             db.session.add(answer)    

#         db.session.commit()

    
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "message": "An error occurred creating the question and answer."
#             }
#         ), 500


#     return jsonify(
#         {
#             "code": 201,
#             "message": "Question and answer are successfully created"
#         }
#     ), 201     



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)