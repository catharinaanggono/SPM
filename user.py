from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:3306/one_stop_lms"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 86400
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'userTable'

    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(200), nullable=True)
    UserType = db.Column(db.String(200), nullable=True)

    def __init__ (self, UserID, UserName, UserType):
        self.UserID = UserID
        self.UserName = UserName
        self.UserType = UserType
    
    def json(self):
        return{"UserID": self.UserID, "UserName": self.UserName, "UserType": self.UserType}

@app.route('/user/<string:UserID>')
def get_acct_details(UserID):
    user = User.query.filter_by(UserID = UserID).all()
    if len(user):
        return jsonify({
            "code": 200,
            "data":{
                "user_details": [user_detail.json() for user_detail in user]
            }
        })
    return jsonify({
        "code": 400,
        "message": "There are no such user"
    }), 400




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)