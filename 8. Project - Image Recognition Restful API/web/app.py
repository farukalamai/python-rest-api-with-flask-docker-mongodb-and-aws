from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests
from keras.applications import InceptionV3
from keras.applications.inception_v3 import preprocess_input
from keras.applications import imagenet_utils
from tensorflow.keras.utils import img_to_array
from PIL import Image
from io import BytesIO

app = Flask(__name__)
api = Api(app)

pretained_model = InceptionV3(weights="imagenet")

client = MongoClient("mongodb://db:27017")
db = client.ImageRecongnition
users = db["users"]

def userExist(username):
    if users.count_documents({"Username":username}) == 0:
        return False
    else:
        return True
    
class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData['username']
        password = postedData['password']

        if userExist(username):
            return jsonify({
                "status": 301,
                "message": "Invalid username, user already exists"
            })
        hased_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hased_pw,
            "Tokens": 6
        })

        return jsonify({
            "status": 200,
            "message": "You have succesfully sigined up to api"
        })
def verify_pw(username, password):
    if not userExist(username):
        return False
    
    hased_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hased_pw) == hased_pw:
        return True
    else:
        return False
    
def verify_credentials(username, password):
    if not userExist(username):
        return generate_return_dictionary(301, "Invalid Username"), True
    
    correct_pw = verify_pw(username, password)

    if not correct_pw:
        return generate_return_dictionary(302, "Incorrect Password"), True
    
    return None, False

def generate_return_dictionary(status, msg):
    ret_json = {
        "status": status,
        "msg": msg
    }
    return ret_json

class Classify(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData['username']
        password = postedData['password']
        url = postedData["url"]

        ret_json, error = verify_credentials(username, password)
        if error:
            return jsonify({ret_json})
        
        tokens = users.find({
            "Username": username
        })[0]["Tokens"]

        if tokens <=0:
            return jsonify(generate_return_dictionary(303, "Not Enough Tokens"))
        
        if not url:
            return jsonify(({"error": "No url provided"}), 400)
        
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        img = img.resize((299, 299))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        prediction = pretained_model.predict(img_array)
        actual_prediction = imagenet_utils.decode_predictions(prediction, top=5)
        ret_json = {}

        for pred in actual_prediction[0]:
            ret_json[pred[1]] = float(pred[2]*100)
        
        users.update_one({
            "Username": username
        }, {
            "$set":{
                "Tokens": tokens-1
            }
        })

        return jsonify(ret_json)

class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["admin_pw"]
        refill_amount = postedData["refill"]

        # Check if the username exists
        if not userExist(username):
            return jsonify(generate_return_dictionary(301, "Invalid Username"))

        # Check if the admin password is correct (In this example, it's hardcoded as "abc123")
        correct_pw = "abc123"

        if not password == correct_pw:
            return jsonify(generate_return_dictionary(302, "Incorrect Password"))

        # Update the user's token balance
        users.update_one({
            "Username": username
        }, {
            "$set": {"Tokens": refill_amount}
        })

        return jsonify(generate_return_dictionary(200, "Refilled Successfully"))


api.add_resource(Register, '/register')
api.add_resource(Classify, "/classify")
api.add_resource(Refill, "/refill")

if __name__ == "__main__":
    app.run(host='0.0.0.0')