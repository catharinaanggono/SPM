from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("dbURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
 
class User(db.Model):
    __tablename__ = 'userTable'
 
    id = db.Column(db.Integer, primary_key=True)
 
    def __init__(self):
        pass
        
 
    def json(self):
        return {"id": self.id}


@app.route("/user", methods=['GET'])
def create_user():
    
 
    data = request.get_json()
    user = User(**data)
    nric = data['nric']

    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the patient record."
            }
        ), 500
 
    return jsonify(
        {
            "code": 201,
            "message": "User has been created" 
        }
    ), 201
    