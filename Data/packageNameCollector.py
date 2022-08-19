from time import sleep
from wsgiref import headers
import sys
sys.path.insert(0,r'C:\Users\Abcd\Desktop\PackageResolver\Service')
import packageResolver as packageResolver
from http import client
import pymongo
import pandas


mongo_uri="mongodb://localhost:27017/"
client= pymongo.MongoClient(mongo_uri)
db=client['packagesDataset']

if db.list_collection_names()==[]:

	db.createCollection('projects')

def retrieve_data(post):

    table=db.projects

    if table.find_one({"package":post["package"]}):

        return True

    else:

        return False

def insert_data(post):

    if not retrieve_data(post):

        table=db.projects
        table.insert_one(post).inserted_id


# url = 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.json'

name_list = []

data = pandas.read_csv(r'C:\Users\Abcd\Desktop\PackageResolver\Data\Dynamic Analysis\projects10k.csv')

for i in range(len(data)):

    name_list.append(data['0'][i])

count = 0

for i in name_list:

    post = {}
    count += 1
    post['package'] = i
    print(count)

    if retrieve_data(post):

        continue

    packageResolver.find_packages(i)
    post['dependecies'] = list(packageResolver.packages.keys())
    insert_data(post)
    
    sleep(1)
