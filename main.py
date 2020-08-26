#!./venv/bin/python3

import json
from flask import Flask, request, Response
from flask_api import status
# from flask_cors import CORS, cross_origin
from UserService import User

app = Flask(__name__)


@app.route('/')
def hello():
    return {"text": "API v0 for Orderify"}


@app.route('/login', methods=['POST'])
# @cross_origin(support_credentials=True)
def login():
    if request.method == 'POST':
        reqJson = request.get_json()
        response = User.login(reqJson)
    else:
        response = Response('LOGIN ROUTE')
    return response


@app.route('/user/<username>', methods=['GET'])
# @cross_origin(support_credentials=True)
def user(username=None):
    if request.method == 'GET':
        response = User.getUser(username, request.headers.get("Authorization"))
    else:
        response = Response('USER ROUTE')
    return response


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        try:
            reqJson = request.get_json()
            usr = User.createUser(reqJson)
            User.saveUser(usr)
            response = Response(json.dumps({"token": usr.toObj().get('tokens')[0].decode()}), status=status.HTTP_200_OK,
                                mimetype="application/json")
        except Exception as e:
            response = Response(json.dumps({"error": str(e)}), mimetype='application/json',
                                status=status.HTTP_400_BAD_REQUEST)
    else:
        response = Response('SIGNUP ROUTE')
    return response


if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=True)
