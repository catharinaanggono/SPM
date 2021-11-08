from flask import Flask, json, render_template, jsonify, request
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


class publicForum(db.Model):
    __tablename__ = 'publicForum'

    ForumID = db.Column(db.Integer, primary_key=True)
    ForumTitle = db.Column(db.String(500), nullable=False)
    UserID = db.Column(db.Integer, nullable=False)
    ForumDetails = db.Column(db.Text)
    ForumCreated = db.Column(db.DateTime)

    def __init__(self, ForumID, ForumTitle, UserID, ForumDetails, ForumCreated):
        self.ForumID = ForumID
        self.ForumTitle = ForumTitle
        self.UserID = UserID
        self.ForumDetails = ForumDetails
        self.ForumCreated = ForumCreated

    def json(self):
        return{"ForumID":self.ForumID, "ForumTitle":self.ForumTitle, "UserID":self.UserID, "ForumDetails":self.ForumDetails, "ForumCreated":self.ForumCreated}

class publicForumReply(db.Model):
    __tablename__ = 'publicForumReply'

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



@app.route('/allforum')
def get_all_forum():
    forums = publicForum.query.all()
    output = {}

    for forum in forums:
        current_forum_dict = forum.json()
        username = User.query.filter_by(UserID=forum.json()['UserID']).first().json()['UserName']
        current_forum_dict['UserName'] = username
        output[forum.json()['ForumID']] = current_forum_dict

    #print(output)
    
    if (len(output)):
        return jsonify({
            "code": 200,
            "message": "Forum exist",
            'data': output 
        }), 200
    else:
        return jsonify({
            "code": 404,
            "message": "Forum doesn't exist"
        }), 404


@app.route('/individual_forum/<string:ForumID>')
def get_forum(ForumID):
    forum = publicForum.query.filter_by(ForumID=ForumID).first()
    username = User.query.filter_by(UserID=forum.json()['UserID']).first().json()['UserName']
    #print(username)
    output = forum.json()
    output['username'] = username

    return jsonify({
            "code": 200,
            "message": "Forum exist",
            'data': output
        }), 200

@app.route('/forum_replies/<string:ForumID>')
def get_forum_reply(ForumID):
    forum_reply = publicForumReply.query.filter_by(ForumID=ForumID).all()
    #print(forum_reply)
    output = {}

    for forum in forum_reply:
        #print(forum.json())
        current_forum_dict = forum.json()
        username = User.query.filter_by(UserID=forum.json()['UserID']).first().json()['UserName']
        current_forum_dict['userName'] = username
        output[forum.json()['ReplyID']] = current_forum_dict
    
    #print(output)


    return jsonify({
            "code": 200,
            "message": "Forum exist",
            'data': output
        }), 200


@app.route('/user_reply', methods=["POST"])
def submit_forum_reply():
    data = request.get_json()
    print(data)
    data["ReplyTime"] = datetime.strptime(data['ReplyTime'], '%d-%m-%Y %H:%M:%S')

    upload = publicForumReply(ReplyID=None, **data)
    print(upload.json())

    try:
        db.session.add(upload)
        db.session.commit()
        print(100)
    except:
        return jsonify({
            "code": 500,
            "message": "An error occured while adding reply"
        }), 500

    return jsonify({
        "code": 200,
        "data": upload.json()
    }), 200





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)