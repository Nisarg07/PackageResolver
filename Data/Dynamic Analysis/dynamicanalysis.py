import subprocess
import sys
import pandas

name_list = []

data = pandas.read_csv(r'C:\Users\Abcd\Downloads\projects10k.csv')

for i in range(len(data)):

    name_list.append(data['0'][i])

def install(package):

    for i in package:

        try:

            print(i)
            subprocess.check_call([sys.executable, "-m", "pip", "install", i])
        
        except:
            
            continue
    
install(name_list)