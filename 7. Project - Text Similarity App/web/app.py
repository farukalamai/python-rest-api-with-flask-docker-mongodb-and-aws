from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os
from pymongo import MongoClient
import bcrypt
import spacy

app =Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB # new database
users = db["users"]


def UserExist(username):
    if users.count_documents({"Username": username}) == 0:
        return False
    else:
        return True
    

class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username  = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)
        
        hased_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hased_pw,
            "Tokens": 6,
        })
        retJson = {
            "status": 200,
            "msg": "You have successfully log in"
        }
        return jsonify(retJson)

def verifyPw(username, password):
    if not UserExist(username):
        return False
    
    hased_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hased_pw)==hased_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens

class Detect(Resource):
    def post(self):
        postedData = request.get_json()

        username  = postedData["username"]
        password = postedData["password"]

        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not UserExist(username):
            return jsonify({
                "status": 301,
                "msg": "Invalid Username"
            })
        
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            return jsonify({
                "status": 302,
                "msg": "YOu have entered a incorrect password"
            })
        
        num_tokens = countTokens(username)

        if num_tokens <=0 :
            return jsonify({
                "status": 303,
                "msg": "you are out of token, please refill"
            })
        
        # calculate the edit distance
        nlp = spacy.load("en_core_web_sm")

        text1 = nlp(text1)
        text2 = nlp(text2)

        # ratio is the number between 0 and 1
        # the more similar text1 and text2
        
        ratio = text1.similarity(text2)


        retJson = {
            "status": 200,
            "similarity": ratio,
            "msg": "Similarity score calculated successfuly"
        }
        
        current_tokens = countTokens(username)

        users.update_one({
            "Username": username
        },{
            "$set":{"Tokens": current_tokens-1}
        })

        return jsonify(retJson)
    
class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username  = postedData["username"]
        password = postedData["password"]
        refill_amount = postedData["refill"]

        if not UserExist(username):
            return jsonify({
                "status": 301,
                "msg": "Invalid Username"
            })
        
        correct_pw = "abc123"
        if not password == correct_pw:
            return jsonify({
                "status": "Invalid admin password"
            })
        
        
        users.update_one({
            "Username": username
        },{
            "$set": {"Tokens": refill_amount}
        })

        return jsonify({
            "status": 200,
            "msg": "Refilled Successfully"
        })


api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')

if __name__=="__main__":
    app.run(host='0.0.0.0')
