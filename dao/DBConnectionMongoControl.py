from pymongo import MongoClient
import os

class ConnectionMongoControl:
    def getDatabase(name):
        stringConnection = os.getenv('CONNECTION_MONGO_CONTROL')
        client = MongoClient(stringConnection)
        return client[name]
