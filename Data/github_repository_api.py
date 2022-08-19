from time import sleep
from wsgiref import headers
import requests
import json
import sys
sys.path.insert(0,r'C:\Users\Abcd\Desktop\PackageResolver\Service')
from mongodbService import insert_data

def save_repo(res,count):

    temp=dict()

    for x in res['items']:

        count+=1
        print(count)
        sleep(10)

        temp={
            'file_name': x['name'],
            'file_url': x['url'],
            'file_git_url': x['git_url'],
            'author': x['repository']['owner']['login'],
            'repo': x['repository']['name']
        }

        insert_data(temp)

for i in range(0,1000,20):

    try:

        # https://github.com/search?l=&p=1&q=extension%3A.txt+filename%3Arequirements&ref=advsearch&type=Code
        url = 'https://api.github.com/search/code?q=extension:.txt +filename:requirements +size:'+str(i)+'..'+str(i+20)+'&order=desc'
        
        headers={
            'Authorization': 'Token GITHUB PERSONAL ACCESS TOKEN'
        }

        count=0
        response = requests.request('GET',url,headers=headers)
        res=json.loads(response.text)
        save_repo(res,count)
        link = response.headers.get('link', None)
        page = 1
        sleep(30)

        if link is not None:

            print(link)
            
            while('next' in response.links.keys()):
            
                page+=1
                response=requests.request('GET',url='https://api.github.com/search/code?q=extension:.txt +filename:requirements +size:'+str(i)+'..'+str(i+20)+'&order=desc&page='+str(page),headers=headers)
                res=json.loads(response.text)
                save_repo(res,count)
                sleep(30)

    except:

        sleep(30)

    
