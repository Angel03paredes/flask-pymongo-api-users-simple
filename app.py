from flask import Flask , request, jsonify, Response
from flask_pymongo import PyMongo
from pymongo import message
from werkzeug.security import generate_password_hash,check_password_hash
from bson import json_util, ObjectId

#pip install virtualenv
#virtualenv venv


app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://localhost/pymongo-user'
mongo = PyMongo(app)

@app.route("/api/user",methods=['GET'])
def getUsers():
    users = mongo.db.user.find()
    response = json_util.dumps(users)
    return Response(response,mimetype="application/json")
  
@app.route("/api/user/<id>",methods=["GET"])
def getUser(id):
    user = mongo.db.user.find_one(ObjectId(id))
    response = json_util.dumps(user)
    return Response(response,mimetype="application/json")

@app.route("/api/user/<id>",methods=["DELETE"])
def deleteUser(id):
    mongo.db.user.delete_one({"_id":ObjectId(id)})
    return {"message": "User " + id + " was deleted successfully" }

@app.route("/api/user/<id>",methods=["PUT"])
def updateUser(id):
    body = request.json
    user = body['user']
    password = body['password']
    email = body["email"]
    if(user and password and email):
        hashedPassword = generate_password_hash(password)
        mongo.db.user.update_one({"_id":ObjectId(id)}, { "$set":{'userName':user,'email':email,'password': hashedPassword}})
        return {'message':"User " + id + "was updated successfully"}
    else:
        return {"message":"Error"}



@app.route("/api/user",methods=['POST'])
def addUser():
    body = request.json
    user = body['user']
    email = body['email']
    password = body['password']
    if (user and email and password):
        hashedPassword = generate_password_hash(password)
        id = mongo.db.user.insert({'userName':user,"password":hashedPassword,"email":email})
        return {
            'id': str(id),
            'user': user,
            'email': email,
            'password':hashedPassword 
            }
    else:
        return {'message':"not inserted user"}


@app.errorhandler(404)
def notFound(Error:None):
    response = jsonify({
        "message":"Resouce not found: " + request.url,
        "status": 404
    })
    response.status_code = 404
    return response
  



if __name__ == "__main__":
    app.run(debug=True)