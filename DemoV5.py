def detect_labels(path):
    from google.cloud import vision
    import io

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    rst = {}

    for label in labels:
        rst[label.description] = label.score

    return rst


def getKeyImageFromVideos(path, imageAmount):
    import cv2
    rst = []
    inputVideo = cv2.VideoCapture(path)
    frameNum = inputVideo.get(7)

    for i in range(imageAmount):
        gap = (frameNum - (frameNum % imageAmount)) / imageAmount
        inputVideo.set(cv2.CAP_PROP_POS_FRAMES, i * gap)
        a, b = inputVideo.read()
        rst.append(b)

    return rst


def getAggregationRst(path, imageAmount):
    import cv2
    rst = {}
    dicList = []
    imageInputs = getKeyImageFromVideos(path, imageAmount)

    for i in range(imageAmount):
        cv2.imwrite("imInput.jpg", imageInputs[i])
        dicList.append(detect_labels("imInput.jpg"))

    allKeySet = set()

    for i in range(imageAmount):
        keyList = dicList[i].keys()
        for key in keyList:
            allKeySet.add(key)

    for key in allKeySet:
        count = 0
        sum = 0
        for dic in dicList:
            for thisKey in dic.keys():
                if thisKey == key:
                    count += 1
                    sum += dic[thisKey]

        mean = sum / count
        rst[key] = mean

        rstSorted = sorted(rst.items(), key=lambda x: x[1], reverse=True)

    return rstSorted


def processSingleVideo(inputVideo, imageAmount, GCkey):
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCkey  # Recall the Google key stored locally

    print("Analysed one video")

    return getAggregationRst(inputVideo, imageAmount)


def runDemoV5(prob, GCKey):
    import os

    Dic_Name = ["shot_3", "shot_4", "shot_5", "shot_6"]
    All_shot_infor = []

    uid_set = set()
    for dic in Dic_Name:
        shot_infor = []
        dic_path = os.path.join(r"video_cut", dic)
        files = os.listdir(dic_path)

        uid_list = []
        label_list = []

        for file in files:
            uid = file.split(".myreel.")[0]
            uid_list.append(uid)
            uid_set.add(uid)

            rstDic = processSingleVideo(os.path.join(dic_path, file), 3, GCKey)

            labels = ""

            for item in rstDic:
                if item[1] > prob:
                    labels += (item[0] + ", ")

            labels = labels[:-2]

            label_list.append(labels)

        shot_infor.append(uid_list)
        shot_infor.append(label_list)
        All_shot_infor.append(shot_infor)

    allRst = []
    rstUid = []

    for uid in uid_set:
        rstUid.append(uid)
        rstLabel = []
        for shot_infos in All_shot_infor:
            if uid in shot_infos[0]:
                idx = shot_infos[0].index(uid)
                rstLabel.append(shot_infos[1][idx])
            else:
                rstLabel.append("")
        allRst.append(rstLabel)

    return rstUid, allRst


def create_csv(header, uid, data):
    import csv
    if len(header) != len(data[0]) + 1:
        raise Exception('Please provide the header and data of the same length!')
    with open('uid_shots.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        # num_attribute = len(data)
        idx_users = 0
        while idx_users < len(uid):
            row = data[idx_users]
            row.append(uid[idx_users])
            writer.writerow(row)
            idx_users += 1
        csvfile.close()


rstUid, allRst = runDemoV5(0, "GCKey.json")

header = ["shot_3", "shot_4", "shot_5", "shot_6", "uid"]

create_csv(header, rstUid, allRst)
