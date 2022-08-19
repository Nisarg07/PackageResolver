from http import client
import pymongo

mongo_uri="mongodb://localhost:27017/"
client= pymongo.MongoClient(mongo_uri)
db=client.github_data

def retrieve_data(post):

    table=db.github_data

    if table.find_one({"file_url":post["file_url"]}):

        print('found')
        return True

    else:

        return False

def insert_data(temp):

    post=temp
    flag=retrieve_data(post)

    if not flag:

        table=db.github_data
        table.insert_one(post).inserted_id
        print('data inserted')

    else:
        
        print('not inserted')