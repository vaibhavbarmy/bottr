from pymongo import MongoClient
import pymongo
import datetime
from bson import json_util
import json
import nltk

client = MongoClient('localhost', 27017)
mydb = client.test_database_1

def load_data():
    with open('/Users/vaibhav/Projects/bottr/ChatBotBottr/question_answer_data_set.json') as data_file:
        data = json_util.loads(data_file.read())
        record_id = mydb.mytable.insert_many(data)
        print (record_id)
        print (mydb.collection_names())

def create_indexes():
    mydb.mytable.create_index([('tags', pymongo.TEXT), ("question", pymongo.TEXT)], name='search_index', default_language='english')

def get_query_results(query):
    result_direct_match = query_direct_match(query)
    result = []
    if len(result_direct_match) > 0:
        for item in result_direct_match:
            row = {}
            row['answer'] = item['answer']
            row['question'] = item['question']
            row['tags'] = item['tags']
            result.append(row)
    else:
        for item in query_list_tags_match(get_tag_from_question_query(query)):
            row = {}
            row['answer'] = item['answer']
            row['question'] = item['question']
            row['tags'] = item['tags']
            result.append(row)

    if len(result) == 0:
        row = {}
        row['answer'] = "I don't know this"
        row['question'] = query
        row['tags'] = []
        result.append(row)

    return result

# Code to search for direct question match
def query_direct_match(query):
    result = []
    for post in mydb.mytable.find({"question": query}):
        row = {}
        row['answer'] = post['answer']
        row['question'] = post['question']
        row['tags'] = post['tags']
        result.append(row)
    return result

def query_tags_match(query):
    result = []
    for post in mydb.mytable.find({"tags": query}):
        result.append(post)
    return result

# code to get all possible questions with tags in database matching those from input tags list
def query_list_tags_match(tags):
    questions = []
    result = []
    for tag in tags:
        for data in mydb.mytable.find({"tags": tag}):
            if data['question'] not in questions:
                result.append(data)
                questions.append(data['question'])
    return result

# Code to see for all noun phrases in a sentence
def get_tag_from_question_query(query):
    tags = []
    text = nltk.word_tokenize(query.lower())
    pos_tags = nltk.pos_tag(text)
    i = 0
    last_noun_index = 0
    for word, pos in pos_tags:
        print (word, pos)
        if(pos == 'NN' or pos == 'NNS'):
            if i == last_noun_index + 1:
                tags.append(tags[len(tags) - 1] + ' ' + word)
            else:
                last_noun_index = i
            tags.append(word)
        i += 1
    print tags
    return tags

# create_indexes()
# query_direct_match("Where have you worked in the past?")
# print (get_query_results("hrl"))
print (query_list_tags_match(get_tag_from_question_query("what do you think of the Kardashian?")))

# print(query_tags_match("microsoft"))
