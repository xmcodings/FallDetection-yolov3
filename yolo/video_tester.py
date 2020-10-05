import time
from collections import deque
import live_yolo_opencv as yolocv
import falldetection
import cv2
import imutils
import numpy as np


cap = cv2.VideoCapture('images/sl4.mp4')
yolodetect = yolocv.YoloDetection()
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
print(frame_width, frame_height)
width = int(frame_width * 30 / 100)
height = int(frame_height * 30 / 100)
out = cv2.VideoWriter('rotate_org_fasterrr.avi',cv2.VideoWriter_fourcc(*'XVID'), 180, (height,width))


c = 0

coord = []

while (cap.isOpened()):

    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    try:
        print('ret =', ret, 'W =', frame.shape[1], 'H =', frame.shape[0], 'channel =', frame.shape[2])
    except:
        ret = False
        cap.release()
        print("done")

    if ret == True:

        detect, object_diff, center_coordinates, image = yolodetect.start_detection(image=frame)
        print(center_coordinates)

        if c < 4:
            c +=1
            print(c)
            continue
        #print(image)
        dim = (height, width)
        obs = object_diff.split(" ")
        d = False
        for i, o in enumerate(obs):
            print(o)
            if o == "toothbrush" or o == "hair drier" or o == "bottle":
                print("yes")
                d = True
                coord.append(center_coordinates[i]["Y"])
        if d is False:
            if len(coord) > 0:
                coord.append(coord[-1])

        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        #cv2.imshow("hi", image)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    print("q pressed")
        #    break
        out.write(image)

#print(coord)
cap.release()
out.release()

