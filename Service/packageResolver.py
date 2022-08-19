import sys
import requests
import imp
from bs4 import BeautifulSoup
from io import StringIO
from html.parser import HTMLParser

sys.path.insert(0,r'C:\Users\Abcd\Desktop\PackageResolver\parser')

import parse as parse

class MLStripper(HTMLParser):

    def __init__(self):

        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()

    def handle_data(self, d):

        self.text.write(d)

    def get_data(self):

        return self.text.getvalue()

def strip_tags(html):

    s = MLStripper()
    s.feed(html)
    return s.get_data()

packages={}
final_packages = []

def get_packages(package,version):

    url='https://libraries.io/pypi/'+package+'/'+version+'/dependencies'
    response=requests.get(url)
    list1=strip_tags(response.text).split()
    list1=list1[1:len(list1)-2]
    packages.clear()
    packages[package] = version

    for i in range(1,len(list1),2):

        if list1[i-1] in final_packages:

            continue

        final_packages.append(list1[i-1])
        packages[list1[i-1]]=list1[i]

    file2 = open('requirements.txt','a')

    for i in packages:

        s = i+' - '+packages[i]+'\n'
        file2.write(s)

def find_packages(package):

    url='https://libraries.io/pypi/'+package
    response=requests.get(url)
    sys.setrecursionlimit(1500)
    bs=BeautifulSoup(response.text,'html.parser')
    install_path=''
    temp=[]
    version=''

    for i in bs.find_all('strong'):

        if i.text=="This package has been removed from Pypi":

            # print('This package has been removed from Pypi')
            packages.clear()
            return

    for code in bs.find_all('span'):

        if 'Release' in code.text:

            install_path+=code.text
            temp=str.strip(code.text).split()

            if len(temp)<2:

                packages.clear()
                return

            version=temp[1]
            break

    if version:

        get_packages(package,version)
file1 = open(sys.argv[1])
lines=file1.readlines()
finalOutput=[]
allOutput=[]

parse.main()

for i in lines:

  if 'from' == i[0] or 'import' in i:

    finalOutput.append(str.strip(i))

  else:

    allOutput.append(str.strip(i))

temp=[]
python_version=3

for i in allOutput:

    if 'print' in i:

        if i[len('print'):len('print')+1]=='(':

            python_version=3

    else:

        python_version=2

libraries=[]

for i in finalOutput:

    if 'from' in i or 'import' in i:

        if '.' in i:

            temp=i.split('.')
            t=temp[0].split()

            if str.strip(t[1]) not in libraries:

                libraries.append(str.strip(t[1]))

        else:

            temp=i.split()

            if str.strip(temp[1]) not in libraries:

                libraries.append(str.strip(temp[1]))

print('python version:',python_version)

for i in libraries:

    if imp.is_builtin(i):

        print(i,' is built in')
        continue 
    
    find_packages(i)
