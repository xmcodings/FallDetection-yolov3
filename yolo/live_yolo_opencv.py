import time
from collections import deque

import falldetection

import cv2
import numpy as np

class YoloDetection:

    def __init__(self):
        self.config_path = "cfg/yolov3.cfg"
        self.weights_path = "weights/yolov3.weights"
        self.font_scale = 1
        self.thickness = 1
        self.labels = open("data/coco.names").read().strip().split("\n")
        self.colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype="uint8")
        self.detect_keywords = ["person", "sports ball", "bottle", "pottedplant"]
        self.ignore_keywords = ["bird"]
        self.toggle_camera = False
        self.net = cv2.dnn.readNetFromDarknet(self.config_path, self.weights_path)
        # variables
        self.q = deque()
        self.center_coord_q = deque()
        self.class_id_q = deque()

        self.capture_queue = []

        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        self.CONFIDENCE = 0.1
        self.SCORE_THRESHOLD = 0.5
        self.IOU_THRESHOLD = 0.5

    def monitor_camera(self):

        while True:
            self.cap = cv2.VideoCapture(0)
            self._, self.image = self.cap.read()

            h, w = self.image.shape[:2]
            self.blob = cv2.dnn.blobFromImage(self.image, 1 / 255.0, (256, 256), swapRB=True, crop=False)
            self.net.setInput(self.blob)
            start = time.perf_counter()
            self.layer_outputs = self.net.forward(self.ln)
            time_took = time.perf_counter() - start
            print("Time took:", time_took)
            self.boxes, self.confidences, self.class_ids = [], [], []

            # 모델 OUTPUT의 모든 class 를 확인
            for output in self.layer_outputs:

                # Output에서 나온 object를 확인
                for detection in output:
                    # label 과 Confidence 추출

                    scores = detection[5:]  # confidence 배열
                    class_id = np.argmax(scores)  # 가장 높은 Confidence는 label이 됨
                    confidence = scores[class_id]  # Confidence 저장

                    # Confidence 이용해 확률 적은 물체 버림

                    if confidence > self.CONFIDENCE:
                        # 바운딩 박스 좌표계

                        box = detection[:4] * np.array([w, h, w, h])
                        (centerX, centerY, width, height) = box.astype("int")

                        # center 좌표로 x, y 구함

                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        # 현재 Detect 중인 Class 중심좌표와 label 출력
                        # print("class: ", labels[class_id], "/ center", "x: ", centerX,"y: ", centerY)

                        # 바운딩 박스, 좌표 업데이트
                        # 클래스 ID 업데이트
                        self.boxes.append([x, y, int(width), int(height)])
                        self.confidences.append(float(confidence))
                        self.class_ids.append(class_id)
                        self.center_coord.append({"X": centerX, "Y": centerY})

            # perform the non maximum suppression given the scores defined before
            self.idxs = cv2.dnn.NMSBoxes(self.boxes, self.confidences, self.SCORE_THRESHOLD, self.IOU_THRESHOLD)

            self.center_coord_q.append(self.center_coord)  # 전 4 frame으로부터 받은 object 정보
            self.class_id_q.append(self.class_ids)  # 전 4 frame으로부터 받은 물체 id

            print("detected class ids: ", self.class_ids)  # 한 frame 에서 검출된 물체 id
            print("center coordinates: ", self.center_coord)  # 물체 center

            if len(self.center_coord_q) > 4:
                self.center_coord_q.popleft()
                print("center coord pop left")

            if len(self.class_id_q) > 4:
                self.class_id_q.popleft()
                print("center coord pop left")

            if (len(self.class_id_q) > 3):
                print("----")
                print(falldetection.detectFall(self.class_id_q, self.center_coord_q))
                # return falldetection.detectFall(self.class_id_q, self.center_coord_q)

            if len(self.idxs) > 0:
                # loop over the indexes we are keeping
                for i in self.idxs.flatten():
                    # extract the bounding box coordinates
                    x, y = self.boxes[i][0], self.boxes[i][1]
                    w, h = self.boxes[i][2], self.boxes[i][3]

                    # 박스 작성
                    color = [int(c) for c in self.colors[self.class_ids[i]]]
                    cv2.rectangle(self.image, (x, y), (x + w, y + h), color=color, thickness=self.thickness)
                    text = f"{self.labels[self.class_ids[i]]}: {self.confidences[i]:.2f}"
                    # calculate text width & height to draw the transparent boxes as background of the text
                    (text_width, text_height) = \
                        cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=self.font_scale,
                                        thickness=self.thickness)[0]
                    text_offset_x = x
                    text_offset_y = y - 5
                    box_coords = (
                        (text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height))
                    overlay = self.image.copy()
                    cv2.rectangle(overlay, box_coords[0], box_coords[1], color=color, thickness=cv2.FILLED)
                    # add opacity (transparency to the box)
                    self.image = cv2.addWeighted(overlay, 0.6, self.image, 0.4, 0)
                    # now put the text (label: confidence %)
                    cv2.putText(self.image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=self.font_scale, color=(0, 0, 0), thickness=self.thickness)

            cv2.imshow("image", self.image)
            if ord("q") == cv2.waitKey(1):
                print("break!!!!!!!!!!!------------")
                break


    def start_detection(self, image):
        self.CONFIDENCE = 0.1
        self.SCORE_THRESHOLD = 0.2
        self.IOU_THRESHOLD = 0.5

        #self.cap = cv2.VideoCapture(0)
        #self._, self.image = self.cap.read()

        h, w = image.shape[:2]
        self.blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (256, 256), swapRB=True, crop=False)
        self.net.setInput(self.blob)
        start = time.perf_counter()
        self.layer_outputs = self.net.forward(self.ln)
        time_took = time.perf_counter() - start
        #print("Time took:", time_took)
        boxes = []
        confidences = []
        class_ids = []
        center_coord = []

        # 모델 OUTPUT의 모든 class 를 확인
        for output in self.layer_outputs:

            # Output에서 나온 object를 확인
            for detection in output:
                # label 과 Confidence 추출

                scores = detection[5:]  # confidence 배열
                class_id = np.argmax(scores)  # 가장 높은 Confidence는 label이 됨
                confidence = scores[class_id]  # Confidence 저장

                # Confidence 이용해 확률 적은 물체 버림

                if confidence > self.CONFIDENCE:
                    # 바운딩 박스 좌표계

                    box = detection[:4] * np.array([w, h, w, h])
                    (centerX, centerY, width, height) = box.astype("int")

                    # center 좌표로 x, y 구함

                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # 현재 Detect 중인 Class 중심좌표와 label 출력
                    # print("class: ", labels[class_id], "/ center", "x: ", centerX,"y: ", centerY)

                    # 바운딩 박스, 좌표 업데이트
                    # 클래스 ID 업데이트
                    boxes.append([x, y, int(width), int(height)])

                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    center_coord.append({"X": centerX, "Y": centerY})

        # perform the non maximum suppression given the scores defined before
        self.idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.SCORE_THRESHOLD, self.IOU_THRESHOLD)
        #print(self.idxs)
        #print(self.idxs.flatten())
        thresh_obj = []
        if len(self.idxs) > 0:
            for i in self.idxs.flatten():
                thresh_obj.append(class_ids[i])
        #print(class_ids)
        #print(thresh_obj)

        self.center_coord_q.append(center_coord)  # 전 4 frame으로부터 받은 object 정보 queue
        self.class_id_q.append(thresh_obj)  # 전 4 frame으로부터 받은 물체 id queue

        # image manipulation
        if len(self.idxs) > 0:
            # loop over the indexes we are keeping
            for i in self.idxs.flatten():
                # extract the bounding box coordinates
                x, y = boxes[i][0], boxes[i][1]
                w, h = boxes[i][2], boxes[i][3]

                # 박스 작성
                color = [int(c) for c in self.colors[class_ids[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color=color, thickness=self.thickness)
                text = f"{self.labels[class_ids[i]]}: {confidences[i]:.2f}"
                # calculate text width & height to draw the transparent boxes as background of the text
                (text_width, text_height) = \
                    cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=self.font_scale,
                                    thickness=self.thickness)[0]
                text_offset_x = x
                text_offset_y = y - 5
                box_coords = (
                    (text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height))
                overlay = image.copy()
                cv2.rectangle(overlay, box_coords[0], box_coords[1], color=color, thickness=cv2.FILLED)
                # add opacity (transparency to the box)
                image = cv2.addWeighted(overlay, 0.6, image, 0.4, 0)
                # now put the text (label: confidence %)
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=self.font_scale, color=(0, 0, 0), thickness=self.thickness)

        #cv2.imshow("monitor", self.image)

        if len(self.center_coord_q) > 4:
            self.center_coord_q.popleft()
            #print("center coord pop left")

        if len(self.class_id_q) > 4:
            self.class_id_q.popleft()
            #print("classid pop left")

        #print(self.class_id_q)
        #print(self.center_coord_q)

        if len(self.class_id_q) > 3: # 3번째 frame 이상부터
            #print("----")
            #print(falldetection.detectFall(self.class_id_q, self.center_coord_q))
            detect, object_diff, center_coordinates = falldetection.detectFall(self.class_id_q, self.center_coord_q)

            ret_string = ""
            for obs in object_diff:
                ret_string += self.labels[obs] + " "

            print(ret_string)
            return detect, ret_string, center_coordinates, image

        return 0,0,0,0



'''
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

            # 박스 작성
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
'''

'''

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
'''