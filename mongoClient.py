import pymongo
from bson.objectid import ObjectId


class MongoClient:
    def __init__(self, url="mongodb://localhost:27017/", database="", collection=""):
        self.connection = pymongo.MongoClient(url)
        self.database = database
        self.collection = collection
        if database != "":
            self.database = self.connection[database]
            if collection != "":
                self.collection = self.database[collection]

    def db(self, name):
        self.database = self.connection[name]

    def col(self, name):
        if self.database == "":
            raise Exception('You have not connected any database.')
        self.collection = self.database[name]

    def insert(self, data):
        if self.collection == "":
            raise Exception('You have not connected any collection.')
        return self.collection.insert_one(data)

    def getCols(self):
        if self.database == "":
            raise Exception('You have not connected any database.')
        return self.database.list_collection_names()

    def find(self, condition, bonus, findType=""):
        if self.collection == "":
            raise Exception('You have not connected any collection.')
        if findType == 'one':
            return self.collection.find_one(condition, bonus)
        return self.collection.find(condition, bonus)

    def delete(self, condition, deleteType=""):
        if deleteType == "one":
            return self.collection.delete_one(condition)
        return self.collection.delete(condition)

    def dropCol(self):
        return self.collection.drop()

    def update(self, condition, newValues, updateType=""):
        if updateType == "one":
            self.collection.update_one(condition, newValues)
        else:
            return self.collection.update_many(condition, newValues)

    def generateID(self):
        return str(ObjectId())
