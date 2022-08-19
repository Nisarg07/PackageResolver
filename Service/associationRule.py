import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from http import client
import pymongo
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

mongo_uri="mongodb://localhost:27017/"
client= pymongo.MongoClient(mongo_uri)
db=client['packagesDataset']
table = db.projects
data = table.find()
dataset =[]

for i in data:

    dataset.append([i['package']]+i['dependecies'])

te = TransactionEncoder()
te_array = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_array, columns=te.columns_)

frequent_itemsets_ap = apriori(df, min_support=0.01, use_colnames=True)

rules_ap = association_rules(frequent_itemsets_ap, metric="confidence", min_threshold=0.7)
print(rules_ap)