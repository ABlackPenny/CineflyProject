import csv
import json
import pandas as pd

headers = []
newHeaders = []

allList = []
with open(r'output', 'r') as f:
    lines = f.readlines()
    for line in lines:
        entity = json.loads(line)
        allList.append(entity)

# find new labels
for entityDict in allList:
    for entities in entityDict['Entities']:
        if (not entities['Type'] in headers) and (not entities['Type'] in newHeaders):
            newHeaders.append(entities['Type'])

# write labels at the beginning of csv file
with open(r'PersonInfo.csv', 'w+', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers + newHeaders)
    writer.writeheader()

with open(r'PersonInfo.csv', 'a+', encoding='UTF-8', newline="") as f:
    writer = csv.DictWriter(f, fieldnames=headers + newHeaders)

    for i in range(len(allList)):
        name = "No name detected in intro clip or format error"

        entityDict = allList[i]
        dictValue = {}

        for entities in entityDict['Entities']:
            if type(entities) == type(""):
                continue
            else:
                if (entities['Type'] in newHeaders) and (entities['Score'] >= 0.80):

                    if (entities['Type'] in dictValue.keys()) and (not dictValue[entities['Type']] == ""):
                        dictValue.update({entities['Type']: dictValue[entities['Type']] + ',' + entities['Text']})
                    else:
                        dictValue.update({entities['Type']: entities['Text']})

        writer.writerow(dictValue)

f.close()

with open(r'All_Txt.csv', 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

f.close()

with open(r'PersonInfo.csv', 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    rows2 = [row for row in reader]

for i in range(0, len(rows)):
    for j in range(0, 5):
        rows[i].append(rows2[i][j])

f.close()

test = pd.DataFrame(data=rows)

test.to_csv(r'Final.csv', encoding='gbk')