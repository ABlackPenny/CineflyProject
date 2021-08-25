from collections import Counter
import cv2
import argparse


def age_gender_detect (str_source,if_show_video=False):

    # str_source = input("dir：")
    video = cv2.VideoCapture(str_source)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # out = cv2.VideoWriter('age+gender.mp4', fourcc, float(video.get(cv2.CAP_PROP_FPS)),
    #                       (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))


    def highlightFace(net, frame, conf_threshold=0.7):
        frameOpencvDnn = frame.copy()
        frameHeight = frameOpencvDnn.shape[0]
        frameWidth = frameOpencvDnn.shape[1]
        blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

        net.setInput(blob)
        detections = net.forward()
        faceBoxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                faceBoxes.append([x1, y1, x2, y2])
                # cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
        return frameOpencvDnn, faceBoxes


    parser = argparse.ArgumentParser()
    parser.add_argument('--image')

    args = parser.parse_args()

    faceProto = "opencv_face_detector.pbtxt"
    faceModel = "opencv_face_detector_uint8.pb"
    ageProto = "age_deploy.prototxt"
    ageModel = "age_net.caffemodel"
    genderProto = "gender_deploy.prototxt"
    genderModel = "gender_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList = ['Male', 'Female']

    faceNet = cv2.dnn.readNet(faceModel, faceProto)
    ageNet = cv2.dnn.readNet(ageModel, ageProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)

    padding = 20
    age_list = []
    gender_list = []
    empty_frame1 = 0;
    empty_frame2 = 0;
    empty_rate = 25
    while True:

        hasFrame, frame = video.read()
        if not hasFrame:
            cv2.waitKey(10)
            break

        resultImg, faceBoxes = highlightFace(faceNet, frame)
        if not faceBoxes:
            # print("No face detected")
            faceBoxes.append([0, 0, 0, 0])

        for faceBox in faceBoxes:
            face = frame[max(0, faceBox[1] - padding):
                         min(faceBox[3] + padding, frame.shape[0] - 1), max(0, faceBox[0] - padding)
                                                                        :min(faceBox[2] + padding, frame.shape[1] - 1)]

            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]

            if faceBoxes[-1] == [0, 0, 0, 0]:
                empty_frame1 += 1
                if empty_frame1 == empty_rate:
                    gender_list.append("No enough faces detected, unknown gender")
                    empty_frame1 = 0
            else:
                gender_list.append(str(gender))
                # print(f'Gender: {gender}')

            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            age = ageList[agePreds[0].argmax()]

            if faceBoxes[-1] == [0, 0, 0, 0]:
                empty_frame2 += 1
                if empty_frame2 == empty_rate:
                    age_list.append("No enough faces detected, unknown age")
                    empty_frame2 = 0
            else:
                age_list.append(age)
                # print(f'Age: {age[1:-1]} years')
            if if_show_video:
                cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 255), 2, cv2.LINE_AA)
                # out.write(resultImg)
                cv2.imshow("Detecting age and gender", resultImg)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                   break

    counter = Counter(age_list)
    counter_gender = Counter(gender_list)
    # print(counter)
    max_key = max(counter, key=counter.get)
    max_key_gender = max(counter_gender, key=counter_gender.get)
    # print(max_key)
    # print(max_key_gender)
    # out.release()
    video.release()
    cv2.destroyAllWindows()

    return max_key,max_key_gender

    print("Age & gender detection finished")