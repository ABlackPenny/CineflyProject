import csv
import os
from collections import Counter

from DemoV1 import get_txt_from_file_name
from age_gender_detect import age_gender_detect

Dic_Name = ["shot_1", "shot_2", "shot_3", "shot_4", "shot_5", "shot_6", "shot_7", "shot_8"]
All_shot_infor = []
uid_set = set()
for dic in Dic_Name:
    shot_infor = []
    dic_path = os.path.join(r"video_cut", dic)
    files = os.listdir(dic_path)
    uid_list = []
    txt_list = []
    new_files = []
    for file in files:
        uid = file.split(".myreel.")[0]
        uid_list.append(uid)
        uid_set.add(uid)
        try:
            txt = get_txt_from_file_name(os.path.join(dic_path, file))
            txt_list.append(txt)
        except:
            txt_list.append('Video file is damaged or format is not supported.')
        afile = os.path.join(dic_path, file)
        new_files.append(afile)
    shot_infor.append(uid_list)
    shot_infor.append(txt_list)
    shot_infor.append(new_files)
    All_shot_infor.append(shot_infor)

with open('All_Txt.csv', 'w', encoding='UTF-8', newline="") as f:
    csv.writer(f).writerow(
        ["uid", "@shot1", "@shot2", "@shot3", "@shot4", "@shot5", "@shot6", "@shot7", "@shot8", "@age", "@gender"])

    for uid in uid_set:

        line = uid + ":::@"
        age_counter = Counter()
        gender_counter = Counter()
        for shot_infor in All_shot_infor:
            if uid in shot_infor[0]:
                idx = shot_infor[0].index(uid)
                try:
                    age, gender, dic = age_gender_detect(shot_infor[2][idx])
                    age_counter = age_counter + dic['age']
                    gender_counter = gender_counter + dic['gender']
                except:
                    continue

                line = line + shot_infor[1][idx] + ':::@'
            else:
                line = line + "Shot missed:::@"

        max_key = max(age_counter, key=age_counter.get)
        max_key_gender = max(gender_counter, key=gender_counter.get)
        line = line + str(max_key) + ":::@" + str(max_key_gender)

        line_list = line.split(':::')
        csv.writer(f).writerow(line_list)

f.close()
