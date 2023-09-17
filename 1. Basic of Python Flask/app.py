from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/hi')
def hi():
    return 'HI faruk'

@app.route('/add', methods=["POST"])
def add():
    datadict = request.get_json()
    if "y" not in datadict:
        return "Error", 305
    x = datadict["x"]
    y = datadict["y"]

    z = x + y

    json = {
        "z": z
    }

    return jsonify(json), 200

# working with json
@app.route('/bye')
def bye():
    age = 25
    json = {
        'name': 'faruk',
        'age': age,
        'phones': [
            {
                'phonenmae': 'Iphone',
                'phonenumber': 3333
            },
                        {
                'phonenmae': 'Iphone pro',
                'phonenumber': 333243233
            },
                                    {
                'phonenmae': 'Iphone pro max',
                'phonenumber': 33324333233
            }
        ]
    }
    return jsonify(json)

if __name__=="__main__":
    app.run(
        debug=True
    )   


# for web application we return page
# foor web service we returen json

#all communication between server/server, server/browser, brwoser/brwoser in text



