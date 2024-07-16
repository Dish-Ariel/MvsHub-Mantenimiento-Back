from pymongo import MongoClient
import os

class ConnectionMongoControl:
    def getCollection(name):
        stringConnection = os.getenv('CONNECTION_MONGO_CONTROL')
        client = MongoClient(stringConnection)
        database = client["MTO_CTRL_MVSHUB"]
        return database[name]
    
    def getDatabase(name):
        stringConnection = os.getenv('CONNECTION_MONGO_CONTROL')
        client = MongoClient(stringConnection)
        return client[name]
