from pymongo import MongoClient

# db
#client = MongoClient('mongodb://test:test@localhost', 27017) ##localhost db내부 접속
client = MongoClient('mongodb://test:test@mongo', 27017) ##cloudtype db내부 접속
#client = MongoClient('mongodb://test:test@svc.sel4.cloudtype.app:32165/?authMechanism=DEFAULT', 27017) ##cloudtype db외부 접속
db = client.dbsparta
appSecret = "1!2@3#4$"
