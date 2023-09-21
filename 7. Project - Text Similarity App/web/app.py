# Import necessary libraries and modules
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os
from pymongo import MongoClient
import bcrypt
import spacy

# Create a Flask application
app = Flask(__name__)
api = Api(app)

# Connect to MongoDB
client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB  # Create a new database
users = db["users"]  # Create a collection named "users"


# Function to check if a user exists in the database
def UserExist(username):
    if users.count_documents({"Username": username}) == 0:
        return False
    else:
        return True


# Define a resource for user registration
class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        # Check if the username already exists
        if UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)

        # Hash the password using bcrypt
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # Insert the user into the database
        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 6,
        })
        retJson = {
            "status": 200,
            "msg": "You have successfully logged in"
        }
        return jsonify(retJson)


# Function to verify a user's password
def verifyPw(username, password):
    if not UserExist(username):
        return False

    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    # Check if the provided password matches the hashed password in the database
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


# Function to get the token count for a user
def countTokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens


# Define a resource for text similarity detection
class Detect(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        text1 = postedData["text1"]
        text2 = postedData["text2"]

        # Check if the username exists
        if not UserExist(username):
            return jsonify({
                "status": 301,
                "msg": "Invalid Username"
            })

        # Verify the user's password
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            return jsonify({
                "status": 302,
                "msg": "You have entered an incorrect password"
            })

        # Check the user's token balance
        num_tokens = countTokens(username)

        if num_tokens <= 0:
            return jsonify({
                "status": 303,
                "msg": "You are out of tokens, please refill"
            })

        # Calculate the similarity between text1 and text2 using spaCy
        nlp = spacy.load("en_core_web_sm")
        text1 = nlp(text1)
        text2 = nlp(text2)
        ratio = text1.similarity(text2)

        retJson = {
            "status": 200,
            "similarity": ratio,
            "msg": "Similarity score calculated successfully"
        }

        # Deduct one token from the user's balance
        current_tokens = countTokens(username)
        users.update_one({
            "Username": username
        }, {
            "$set": {"Tokens": current_tokens - 1}
        })

        return jsonify(retJson)


# Define a resource for refilling a user's tokens
class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        refill_amount = postedData["refill"]

        # Check if the username exists
        if not UserExist(username):
            return jsonify({
                "status": 301,
                "msg": "Invalid Username"
            })

        # Check if the admin password is correct (In this example, it's hardcoded as "abc123")
        correct_pw = "abc123"
        if not password == correct_pw:
            return jsonify({
                "status": "Invalid admin password"
            })

        # Update the user's token balance
        users.update_one({
            "Username": username
        }, {
            "$set": {"Tokens": refill_amount}
        })

        return jsonify({
            "status": 200,
            "msg": "Refilled Successfully"
        })


# Define API endpoints and associate them with resources
api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')

# Start the Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0')
