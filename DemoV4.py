#https://github.com/matterport/Mask_RCNN
#https://www.youtube.com/c/NicholasRenotte/videos
#
# # !pip3 install tensorflow tensorflow-gpu pixellib opencv-python
#
# import pixellib
# from pixellib.instance import instance_segmentation
# import cv2
#
# segmentation_model = instance_segmentation()
# segmentation_model.load_model('mask_rcnn_coco.h5')
#
#
# # cap = cv2.VideoCapture(0)
# # # cap = cv2.VideoCapture(r"intro/hayden.t.1995.myreel.shot1.introductions.mp4")
# # while cap.isOpened():
# #     ret, frame = cap.read()
# #
# #     # Apply instance segmentation
# #     res = segmentation_model.segmentFrame(frame, show_bboxes=True)
# #     image = res[1]
# #
# #     cv2.imshow('Instance Segmentation', image)
# #
# #     if cv2.waitKey(10) & 0xFF == ord('q'):
# #         break
# #
# # cap.release()
#
# input=cv2.imread(r"testImage2.jpeg")
# res = segmentation_model.segmentFrame(input, show_bboxes=True)
# image = res[1]
# cv2.imshow('Instance Segmentation', image)
# cv2.imwrite('new.jpg',image)
# # cv2.destroyAllWindows()


