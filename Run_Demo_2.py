from DemoTestVersion import run_demo_2
import csv

path=r"voice"
path_intro= r"intro"

fileName_List,vText_List,gender_List,age_List,amazonDir_List=run_demo_2(path,path_intro)



headers = ["fileName","name","age","gender","vText"]
newHeaders = []

for entityList in amazonDir_List:
    for i in range(len(entityList)):
        for j in list(entityList[i].keys()):
            if (not j in headers) and (not j in newHeaders):
                newHeaders.append(j)

with open('PersonInfo.csv','w',newline='') as f:
    writer = csv.DictWriter(f,fieldnames=headers+newHeaders)
    writer.writeheader()
f.close



with open('PersonInfo.csv', 'a', encoding='UTF-8', newline="") as f:
    
    writer = csv.DictWriter(f, fieldnames=headers+newHeaders)
    
    # csv.writer(f).writerow(["fileName","name","age","gender","vText"])
    # for entity in allEntity
    #     csv.writer(f).writerow([entity['fileName'],entity['vText'],entity['gender'],entity['age']])
    for i in range(len(fileName_List)):
        name=""

        thisList=amazonDir_List[i]

        for j in range(len(thisList)):
            thisDir=thisList[j]
            if type(thisDir)==type(""):
                break
            else:
                if "AGE" in thisDir.keys():
                    age_List[i]="("+thisDir["AGE"]+")"
                    break

        for j in range(len(thisList)):
            thisDir=thisList[j]
            if type(thisDir) == type(""):
                break
            else:
                if "NAME" in thisDir.keys():
                    name=thisDir["NAME"]
                    break
                    
                    
                    
        
        dictValue = {'fileName':fileName_List[i],'name':name,'age':age_List[i],'gender':gender_List[i],'vText':vText_List[i]}
        
        for j in range(len(thisList)):
            thisDir=thisList[j]
            for key in thisDir.keys():
                if key in newHeaders:
                    dictValue.update({key:thisDir[key]})
                    break
        write.writerow(dictValue)
    # for i in range(len(allEntity)):
    #     csv.writer(f).writerow([allEntity[i]['fileName'],allEntity[i]['gender'],allEntity[i]['age'],allEntity[i]['vText']])
    f.close
