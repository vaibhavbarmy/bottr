from pymongo import MongoClient
import pymongo
from bson import json_util

client = MongoClient('localhost', 27017)
mydb = client.test_database_1

def load_data():
    with open('question_answer_data_set.json') as data_file:
        data = json_util.loads(data_file.read())
        record_id = mydb.mytable.insert_many(data)
        print (record_id)
        print (mydb.collection_names())

def create_indexes():
    mydb.mytable.create_index([('tags', pymongo.TEXT), ("question", pymongo.TEXT)], name='search_index', default_language='english')

load_data()
create_indexes()