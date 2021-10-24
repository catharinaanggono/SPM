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
            "message": "Quiz are successfully created",
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
            "message": "Question are successfully created",
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
            "message": "Answer are successfully created"
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
                "message": "An error occurred creating the quiz."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "message": "Quiz are successfully created",
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
            "message": "Question are successfully created",
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
            "message": "Answer are successfully created"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)