from flask import Flask, jsonify, request
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


def checkPostedData(postedData, functionname):
    if (functionname == "add" or functionname == "subtract" or functionname == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
    elif (functionname == "divison"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif postedData ["y"] == 0:
            return 302
        else:
            return 200
        
         
class Add(Resource):
    def post(self):
        # if i am then resource add was requested using the method pos

        #step -1: get posted data
        postedData = request.get_json()

        statuscode = checkPostedData(postedData, "add")
        if (statuscode != 200):
            retJson = {
                "Message": "An error is occured",
                "Status Code": statuscode
            }
            return jsonify(retJson)
        
        # if I am here then status code is 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        # Step -2: add the data
        ret = x + y
        retMap = {
            'Message': ret,
            'Status Code':200
        }

        return jsonify(retMap)

class Subtraction(Resource):
    def post(self):
        # if i am then resource subtract was requested using the method pos

        #step -1: get posted data
        postedData = request.get_json()

        statuscode = checkPostedData(postedData, "subtract")
        if (statuscode != 200):
            retJson = {
                "Message": "An error is occured",
                "Status Code": statuscode
            }
            return jsonify(retJson)
        
        # if I am here then status code is 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        # Step -2: subtract the data
        ret = x - y
        retMap = {
            'Message': ret,
            'Status Code':200
        }

        return jsonify(retMap)

class MUltiply(Resource):
    def post(self):
        # if i am then resource subtract was requested using the method pos

        #step -1: get posted data
        postedData = request.get_json()

        statuscode = checkPostedData(postedData, "multiply")
        if (statuscode != 200):
            retJson = {
                "Message": "An error is occured",
                "Status Code": statuscode
            }
            return jsonify(retJson)
        
        # if I am here then status code is 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        # Step -2: multipy the data
        ret = x * y
        retMap = {
            'Message': ret,
            'Status Code':200
        }

        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        # if i am then resource subtract was requested using the method pos

        #step -1: get posted data
        postedData = request.get_json()

        statuscode = checkPostedData(postedData, "divison")
        if (statuscode != 200):
            retJson = {
                "Message": "An error is occured",
                "Status Code": statuscode
            }
            return jsonify(retJson)
        
        # if I am here then status code is 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        # Step -2: multipy the data
        ret = (x*1.0) / y
        retMap = {
            'Message': ret,
            'Status Code':200
        }

        return jsonify(retMap)

@app.route('/')
def hello_world():
    return "Hello World"

api.add_resource(Add, "/add")
api.add_resource(Subtraction, "/subtract")
api.add_resource(MUltiply, "/multiply")
api.add_resource(Divide, "/divsion")

if __name__=="__main__":
    app.run(
        host='0.0.0.0'
    )   


# for web application we return page
# foor web service we returen json

#all communication between server/server, server/browser, brwoser/brwoser in text



