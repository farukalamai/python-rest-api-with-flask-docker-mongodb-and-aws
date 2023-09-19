"""
Registaraction of a user
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentence on out database for 1 token
"""
# Import necessary modules and libraries
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os
from pymongo import MongoClient
import bcrypt

# Create a Flask web application
app = Flask(__name__)
api = Api(app)

# Set up a connection to a MongoDB database
client = MongoClient("mongodb://db:27017")
db = client.SentenceDatabase
users = db["users"] # user is collection here

class Register(Resource):
    def post(self):
        # Step: 1. Get posted data from the request
        postedData = request.get_json() 

        # Got the data 
        username = postedData["username"]
        password = postedData["password"]

        # hash(Fe8jal3jTT + salt) = djklwjoeralwdjf
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # store username an pw into the Sentences Database     
        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens": 6
        })

        retJson = {
            "status": 200,
            "msg": "You have succesfully signed up for the API"
        }   

        return jsonify(retJson)

def verifyPw(username, password):
    hashed_pw = users.find({
        "Username": username
    })[0]["Password"] #finding previoius password into the datavbase
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False
    
def countTokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens #number of tokens left for the user

class Store(Resource):
    def post(self):
        # Step:1 Get teh posted data
        postedData = request.get_json() 

        # Step:2 Read the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData['sentence']

        # Step: 3 Verify the username and password match
        correct_pw = verifyPw(username, password)
        if not correct_pw:
            retJson = {
                "status": 302
            } 
            return jsonify(retJson)
        

        # Step: 4 Verify if the user has enough tokens
        num_tokens = countTokens(username)
        if num_tokens <=0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)

        # Step: 5 Store the sentenve, take one token away and return 2000
        users.update_one({
            "Username": username
        },
        {
            "$set": {"Sentence":sentence, "Tokens":num_tokens}
        })
        retJson = {
                "status": 200,\
                "msg": "Sentence saved succesfully"
            }
        return jsonify(retJson)
    
class Get(Resource):
    def post(self):
        postedData = request.get_json() 

        #  Read the data
        username = postedData["username"]
        password = postedData["password"]

        correct_pw = verifyPw(username, password)
        if not correct_pw:
            retJson = {
                "status": 302
            } 
            return jsonify(retJson)

        num_tokens = countTokens(username)
        if num_tokens <=0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)
        
        # Make the user pay
        users.update_one({
            "Username": username
        },
        {
            "$set": {"Tokens":num_tokens-1}
        })
        retJson = {
                "status": 200,\
                "msg": "Sentence saved succesfully"
            }
        return jsonify(retJson)        
        
        sentence  = users.find({
            "Username": username
        })[0]["Sentence"]
        retJson = {
            "status": 200,
            "sentence": sentence
        }
        return jsonify(retJson)      


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')

if __name__=="__main__":
    app.run(host='0.0.0.0')


