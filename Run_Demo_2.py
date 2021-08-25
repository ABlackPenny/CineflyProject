from DemoTestVersion import run_demo_2
import csv

path=r"voiceover"
path_intro=r"into"

fileName_List,vText_List,gender_List,age_List,amazonDir_List=run_demo_2(path,path_intro)

with open('PersonInfo.csv', 'w', encoding='UTF-8', newline="") as f:
    csv.writer(f).writerow(["fileName","name","age","gender","vText"])
    # for entity in allEntity
    #     csv.writer(f).writerow([entity['fileName'],entity['vText'],entity['gender'],entity['age']])
    for i in range(len(fileName_List)):
        name=""

        thisList=amazonDir_List[i]
        print(thisList)
        for j in range(len(thisList)):
            thisDir=thisList[j]
            print(thisDir)
            print(type(thisDir))
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
        csv.writer(f).writerow([fileName_List[i],name,age_List[i],gender_List[i],vText_List[i]])
    # for i in range(len(allEntity)):
    #     csv.writer(f).writerow([allEntity[i]['fileName'],allEntity[i]['gender'],allEntity[i]['age'],allEntity[i]['vText']])
    f.close