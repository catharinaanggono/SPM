from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("dbURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
 
class User(db.Model):
    __tablename__ = 'userTable'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    type = db.Column(db.String(1000), nullable=False)

 
    def __init__(self, name, type):
        self.name = name
        self.type = type
        pass
        
 
    def json(self):
        return {"id": self.id}


@app.route("/user", methods=['POST'])
def create_user():
    
 
    data = request.get_json()
    user = User(**data)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the record."
            }
        ), 500
 
    return jsonify(
        {
            "code": 201,
            "message": "User has been created" 
        }
    ), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
