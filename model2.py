from pymongo import MongoClient

# db
# client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@svc.sel4.cloudtype.app:32165/?authMechanism=DEFAULT', 27017)
db = client.dbsparta
appSecret = "1!2@3#4$"