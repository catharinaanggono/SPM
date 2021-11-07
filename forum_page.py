from flask import Flask, json, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("dbURL")
print(environ.get("dbURL"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 86400
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app) # initialise database with settings from app


class courseForum(db.Model):
    __tablename__ = 'courseforum'

    CourseID = db.Column(db.Integer, nullable=False)
    ForumID = db.Column(db.Integer, primary_key=True)
    ForumTitle = db.Column(db.String(500), nullable=False)
    UserID = db.Column(db.Integer, nullable=False)
    ForumDetails = db.Column(db.Text)
    ForumCreated = db.Column(db.DateTime)

    def __init__(self, CourseID, ForumID, ForumTitle, UserID, ForumDetails, ForumCreated):
        self.CourseID = CourseID
        self.ForumID = ForumID
        self.ForumTitle = ForumTitle
        self.UserID = UserID
        self.ForumDetails = ForumDetails
        self.ForumCreated = ForumCreated

    def json(self):
        return{"CourseID":self.CourseID, "ForumID":self.ForumID, "ForumTitle":self.ForumTitle, "UserID":self.UserID, "ForumDetails":self.ForumDetails, "ForumCreated":self.ForumCreated}


@app.route('/forum')
def get_forum_info():
    forum_info = courseForum.query.all()
    print(forum_info)
    return jsonify ({
        "code":200,
        "message": "Forum exists",
        "data": {
            "forum": [forum.json() for forum in forum_info]
        }
    })


class courseForumReply(db.Model):
    __tablename__ = 'courseforumreply'

    ForumID = db.Column(db.Integer, nullable=False)
    ReplyID = db.Column(db.Integer, primary_key=True)
    ReplyContent = db.Column(db.Text)
    UserID = db.Column(db.Integer, nullable=False)
    ReplyTime = db.Column(db.DateTime)

    def __init__(self, ForumID, ReplyID, ReplyContent, UserID, ReplyTime):
        self.ForumID = ForumID
        self.ReplyID = ReplyID
        self.ReplyContent = ReplyContent
        self.UserID = UserID
        self.ReplyTime = ReplyTime

    def json(self):
        return{"ForumID":self.ForumID, "ReplyID":self.ReplyID, "ReplyContent":self.ReplyContent, "UserID":self.UserID, "ReplyTime":self.ReplyTime}

@app.route('/forumreply')
def get_forum_reply():
    forum_reply = courseForumReply.query.all()
    print(forum_reply)
    return jsonify ({
        "code":200,
        "message": "Forum Reply exists",
        "data": {
            "reply": [reply.json() for reply in forum_reply]
        }
    })




class users(db.Model):
    __tablename__ = 'userTable'

    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(50), nullable=False)
    UserType = db.Column(db.String(100), nullable=False)

    def __init__(self, UserID, UserName, UserType):
        self.UserID = UserID
        self.UserName = UserName
        self.UserType = UserType

    def json(self):
        return {"UserID": self.UserID, "UserName": self.UserName, "UserType": self.UserType}


@app.route('/users')
def get_all_users():
    all_users = users.query.all()
    print(all_users)
    return jsonify ({
        "code":200,
        "message": "User exists",
        "data": {
            "user": [user.json() for user in all_users]
        }
    })





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)