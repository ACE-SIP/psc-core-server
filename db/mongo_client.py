import pymongo
import os
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()


class Database(object):
    URI = os.environ.get("DB_URI")
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client.get_default_database()

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)


if __name__ == "__main__":
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_DEVICE')]
    # Database.DATABASE.insert("pharma_supply_chain",item_1)
    objInstance = ObjectId("6282054554f7fe55f048909c")
    data = collection.find_one({"_id": objInstance})
    print(data)
