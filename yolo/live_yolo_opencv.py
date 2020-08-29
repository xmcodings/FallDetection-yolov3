import time
from collections import deque

import falldetection

import cv2
import numpy as np

CONFIDENCE = 0.1
SCORE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.5
config_path = "cfg/yolov3.cfg"
weights_path = "weights/yolov3.weights"
font_scale = 1
thickness = 1
labels = open("data/coco.names").read().strip().split("\n")
colors = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")
detect_keywords = ["person", "sports ball", "bottle", "pottedplant"]
ignore_keywords = ["bird"]

net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

cap = cv2.VideoCapture(0)

# variables
q = deque()
center_coord_q = deque()
class_id_q = deque()

center_coord = []
capture_queue = []




while True:
    _, image = cap.read()

    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (256, 256), swapRB=True, crop=False)
    net.setInput(blob)
    start = time.perf_counter()
    layer_outputs = net.forward(ln)
    time_took = time.perf_counter() - start
    print("Time took:", time_took)
    boxes, confidences, class_ids = [], [], []

    # 모델 OUTPUT의 모든 class 를 확인
    for output in layer_outputs:

        # Output에서 나온 object를 확인
        for detection in output:
            # label 과 Confidence 추출

            scores = detection[5:] # confidence 배열
            class_id = np.argmax(scores) # 가장 높은 Confidence는 label이 됨
            confidence = scores[class_id] # Confidence 저장

            # Confidence 이용해 확률 적은 물체 버림

            if confidence > CONFIDENCE:
                # 바운딩 박스 좌표계

                box = detection[:4] * np.array([w, h, w, h])
                (centerX, centerY, width, height) = box.astype("int")

                # center 좌표로 x, y 구함

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                #현재 Detect 중인 Class 중심좌표와 label 출력
                #print("class: ", labels[class_id], "/ center", "x: ", centerX,"y: ", centerY)

                # 바운딩 박스, 좌표 업데이트
                # 클래스 ID 업데이트
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                center_coord.append({"X": centerX, "Y": centerY})

    # perform the non maximum suppression given the scores defined before
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, SCORE_THRESHOLD, IOU_THRESHOLD)

    center_coord_q.append(center_coord) # 전 4 frame으로부터 받은 object 정보
    class_id_q.append(class_ids) # 전 4 frame으로부터 받은 물체 id
    font_scale = 1
    thickness = 1
    #print("nms indexs: ", idxs)
    print("detected class ids: ", class_ids) # 한 frame 에서 검출된 물체 id
    print("centor coordinates: ", center_coord) # 물체 center

    if len(center_coord_q) > 4:
        center_coord_q.popleft()
    if len(class_id_q) > 4:
        class_id_q.popleft()

    if(len(class_id_q) > 3):
        print("----")
        print(falldetection.detectFall(class_id_q, center_coord_q))


    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            x, y = boxes[i][0], boxes[i][1]
            w, h = boxes[i][2], boxes[i][3]

            # draw a bounding box rectangle and label on the image
            color = [int(c) for c in colors[class_ids[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color=color, thickness=thickness)
            text = f"{labels[class_ids[i]]}: {confidences[i]:.2f}"
            # calculate text width & height to draw the transparent boxes as background of the text
            (text_width, text_height) = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=font_scale, thickness=thickness)[0]
            text_offset_x = x
            text_offset_y = y - 5
            box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height))
            overlay = image.copy()
            cv2.rectangle(overlay, box_coords[0], box_coords[1], color=color, thickness=cv2.FILLED)
            # add opacity (transparency to the box)
            image = cv2.addWeighted(overlay, 0.6, image, 0.4, 0)
            # now put the text (label: confidence %)
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=font_scale, color=(0, 0, 0), thickness=thickness)

    cv2.imshow("image", image)
    if ord("q") == cv2.waitKey(1):
        break

cap.release()
cv2.destroyAllWindows()


def detectFall(classids, centercoords):
    # takes classids, centers, and calculates detection
    QUEUESIZE = 4
    threshold = 1
    detect = False
    recent = classids[QUEUESIZE-1]
    ob_length = len(recent)
    count = 0
    for detect in classids[1:2]:
        if ob_length != len(detect):
             count = count + 1
    if count > threshold:
        detect = True

    # calculate what object is detected

    return detect, centercoords



def warnUser():

    return 1
