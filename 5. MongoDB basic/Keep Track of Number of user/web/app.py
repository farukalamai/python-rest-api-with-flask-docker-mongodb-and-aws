# Import necessary modules and libraries
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os
from pymongo import MongoClient

# Create a Flask web application
app = Flask(__name__)
api = Api(app)

# Set up a connection to a MongoDB database
client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

# Insert an initial document into the UserNum collection
UserNum.insert_one({
    'num_of_users': 0
})

# Define a resource class 'Visit' to handle user visits
class Visit(Resource):
    def get(self):
        # Retrieve the current number of users and increment it by 1
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update_one({}, {"$set": {"num_of_users": new_num}})
        return str("Hello user " + str(new_num))

# Define a function to check the validity of posted data
def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301  # Missing parameter
        else:
            return 200
    elif (functionName == "division"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"]) == 0:
            return 302  # Division by zero
        else:
            return 200

# Define a resource class 'Add' to handle addition
class Add(Resource):
    def post(self):
        # Get posted data from the request
        postedData = request.get_json()

        # Verify the validity of posted data
        status_code = checkPostedData(postedData, "add")
        if (status_code != 200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        # If valid, perform addition
        x = int(postedData["x"])
        y = int(postedData["y"])
        ret = x + y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

# Define a resource class 'Subtract' to handle subtraction
class Subtract(Resource):
    def post(self):
        # Get posted data from the request
        postedData = request.get_json()

        # Verify the validity of posted data
        status_code = checkPostedData(postedData, "subtract")

        if (status_code != 200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        # If valid, perform subtraction
        x = int(postedData["x"])
        y = int(postedData["y"])
        ret = x - y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

# Define a resource class 'Multiply' to handle multiplication
class Multiply(Resource):
    def post(self):
        # Get posted data from the request
        postedData = request.get_json()

        # Verify the validity of posted data
        status_code = checkPostedData(postedData, "multiply")

        if (status_code != 200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        # If valid, perform multiplication
        x = int(postedData["x"])
        y = int(postedData["y"])
        ret = x * y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

# Define a resource class 'Divide' to handle division
class Divide(Resource):
    def post(self):
        # Get posted data from the request
        postedData = request.get_json()

        # Verify the validity of posted data
        status_code = checkPostedData(postedData, "division")

        if (status_code != 200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        # If valid, perform division (casting to float to handle division by zero)
        x = int(postedData["x"])
        y = int(postedData["y"])
        ret = (x * 1.0) / y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

# Add the resource classes to the API with their respective endpoints
api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/division")
api.add_resource(Visit, "/hello")

# Define a basic route for the root URL
@app.route('/')
def hello_world():
    return "Hello World!"

# Run the Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0')
