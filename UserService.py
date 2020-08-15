import json
import os
import bcrypt
import re
from jwtClient import JwtClient
from mongoClient import MongoClient
from flask import Response
from flask_api import status

SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
jwt = JwtClient(SECRET_KEY)

mongo = MongoClient(database="orderifyTest")
mongo.col('users')


class UserSchema:
    def __init__(self, req):
        self._id = mongo.generateID()
        self.email = req["email"]
        self.username = req["username"]
        password = req["pass"]
        if not len(password) > 7:
            raise Exception('Password should contain more than 7 characters.')
        elif not re.search("[a-z]", password):
            raise Exception('Password should contain at least 1 lowercase letter.')
        elif not re.search("[A-Z]", password):
            raise Exception('Password should contain at least 1 uppercase letter.')
        elif not re.search("[0-9]", password):
            raise Exception('Password should contain at least 1 number.')
        elif re.search("\s", password):
            raise Exception('Password can not contain space.')
        self.password = bcrypt.hashpw(req["pass"].encode(), bcrypt.gensalt(8))
        self.accountType = req["accountType"]
        self.jwt = jwt.encode(self._id)

    def toObj(self):
        return {
            "email": self.email,
            "username": self.username,
            "pass": self.password,
            "accountType": self.accountType,
            "_id": self._id,
            "tokens": [self.jwt]
        }


def tokenExist(userObj, token):
    tokenArr = userObj["tokens"]
    accessToken = token.split()[1].encode()
    return accessToken in tokenArr


class User:
    @staticmethod
    def createUser(req):
        return UserSchema(req)

    @staticmethod
    def saveUser(user):
        mongo.insert(user.toObj())

    # @staticmethod
    # def updateUser(query, value):
    #     pass

    @staticmethod
    def login(req):
        gotUser = mongo.find({"username": req["username"]}, bonus={"_id": 1, "username": 1, "pass": 1},
                             findType="one")
        if bcrypt.checkpw(req["pass"].encode(), gotUser["pass"]):
            newToken = jwt.encode(gotUser["_id"])
            mongo.update({"_id": gotUser["_id"]}, {"$push": {"tokens": newToken}})
            return Response(json.dumps({"token": newToken.decode()}), status=status.HTTP_200_OK,
                            mimetype='application/json')
        else:
            return Response(json.dumps({"error": "Check your credentials"}), status=status.HTTP_400_BAD_REQUEST,
                            mimetype='application/json')

    @staticmethod
    def getUser(username, token):
        idForUser = jwt.decode(token.split()[1].encode())
        gotUser = mongo.find({"username": username, "_id": idForUser},
                             {"tokens": 1, "_id": 1, "username": 1, "accountType": 1},
                             findType="one")
        if gotUser and tokenExist(gotUser, token):
            return Response(json.dumps({
                "username": gotUser["username"],
                "accountType": gotUser["accountType"]
            }), status=status.HTTP_200_OK,
                mimetype='json')
        else:
            return Response(json.dumps({"error": "Account not found"}), mimetype='application/json',
                            status=status.HTTP_400_BAD_REQUEST)
