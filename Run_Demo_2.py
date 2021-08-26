from DemoTestVersion import run_demo_2
import csv

path=r"voice"
path_intro= r"intro"

fileName_List,vText_List,gender_List,age_List,amazonDir_List=run_demo_2(path,path_intro)

with open('PersonInfo.csv', 'w', encoding='UTF-8', newline="") as f:
    csv.writer(f).writerow(["fileName","name","age","gender","vText"])
    # for entity in allEntity
    #     csv.writer(f).writerow([entity['fileName'],entity['vText'],entity['gender'],entity['age']])
    for i in range(len(fileName_List)):
        name="No name detected in intro clip"

        thisList=amazonDir_List[i]

        for j in range(len(thisList)):
            thisDir=thisList[j]
            if type(thisDir)==type(""):
                break
            else:
                if "AGE" in thisDir.values():
                    itemList=list(thisDir.items())
                    for k in range(len(itemList)):
                        thisTup=itemList[k]
                        if thisTup[1]=="AGE":
                            bgn=itemList[k+1][1]
                            end=itemList[k+2][1]
                            break
                    trans=thisList[-1]
                    age="("+trans[bgn:end]+")"
                    age_List[i]=age
                    break

        for j in range(len(thisList)):
            thisDir=thisList[j]
            if type(thisDir) == type(""):
                break
            else:
                if "NAME" in thisDir.values():
                    itemList=list(thisDir.items())
                    for k in range(len(itemList)):
                        thisTup=itemList[k]
                        if thisTup[1]=="NAME":
                            bgn=itemList[k+1][1]
                            end=itemList[k+2][1]
                            break
                    trans=thisList[-1]
                    name=trans[bgn:end]
                    break
        csv.writer(f).writerow([fileName_List[i],name,age_List[i],gender_List[i],vText_List[i]])
    # for i in range(len(allEntity)):
    #     csv.writer(f).writerow([allEntity[i]['fileName'],allEntity[i]['gender'],allEntity[i]['age'],allEntity[i]['vText']])
f.close