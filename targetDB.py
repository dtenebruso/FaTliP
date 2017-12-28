import pymongo

__author__ = 'pr0c'

class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['targets']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def print(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)