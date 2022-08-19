# PackageResolver

# DATA:

github_repository_api.py : This is the file to collect the requirements.txt files from the GitHub. In this file one needs to generate the GitHub Personal Access Token. And put this token in the headers. Here I’ve used the mongodb so to replicate this file one needs to have configured the mongodb. This file stores data as following JSON format:
{
            'file_name': x['name'],
            'file_url': x['url'],
            'file_git_url': x['git_url'],
            'author': x['repository']['owner']['login'],
            'repo': x['repository']['name']
        }

# DATA/DYNAMIC ANALYSIS:

This folder contains the csv file of dynamic analysis. If one wants to do their own dynamic analysis, you can run dynamicanalysis.py file with names of the packages.

# GITHUB_DATA:

This folder contains the data collected from the github_repository_api.py file.

# PARSER:

This folder contains two files parser.py and visitor.py. Basically this files helps to create AST of the code snippet and classifies imported modules, resources and attributes.

# SERVICE:

associationRule.py: This file generates the association rules. One can run this files with the input of packages and its dependencies.(DockerFiles or requirements.txt)

mongodbService.py: This file establish connection to mongodb. Its has two methods retrieve_data and insert_data. Retrieve_data get the data from the particular dataset. Insert_data inserts data into the given dataset.

packageResolver.py: This file infers and generates the requirements.txt file. One can run this file in CMD with command $python packageResolver.py PYTHON FILE PATH.  And one needs to change the output path for requirements.txt file in the code for file2.

(NOTE: In many files paths needs to be changed to run the particular files).
