import requests
import json
import csv

priorities = {-1:'-1 Blacklist', 1:'1 Low', 2:'2 Medium', 3:'3 High', 4:'4 Ultra', 5:'5 Super'}
minimums = {5:100000, 4:50000, 3:25000, 2:10000, 1:0}

url = 'https://tarkov-market.com/api/v1/items/all'
headers = {'x-api-key': 'By6Huefijm8sOjdS'}

r = requests.get(url, headers=headers)

apiData = r.json()

apiDictionary = {}

for item in apiData:
    apiDictionary[item['bsgId'].replace('-', '')] = item

with open('lootItems.csv', "r", encoding="utf8") as f:
    reader = csv.DictReader(f)
    default = list(reader)

for item in default:
    if item['Priority'] == priorities[-1]:
        continue

    key = item['Id']
    if key not in apiDictionary:
        continue
    apiRow = apiDictionary[item['Id']]
    pps = apiRow['avg24hPrice'] / int(apiRow['slots'])
    for i in reversed(range(1, 6)):
        if pps > minimums[i]:
            item['Priority'] = priorities[i]
            break

csvCols = ['Id', 'FriendlyName', 'Category', 'Priority']

try:
    with open("AUTOlootIems.csv", "w", encoding="utf8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csvCols)
        writer.writeheader()
        writer.writerows(default)
except IOError:
    print("I/O error")


