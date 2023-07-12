from pymongo import MongoClient

# db
client = MongoClient('mongodb://test:test@localhost', 27017)
#client = MongoClient('localhost', 27017)
db = client.dbsparta
