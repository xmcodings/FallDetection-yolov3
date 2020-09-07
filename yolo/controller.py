import live_yolo_opencv as yolocv
import cv2

yolodetect = yolocv.YoloDetection()



cap = cv2.VideoCapture(0)
monitor = False
while True:
    ret, frame = cap.read()

    detect, object_diff, center_coordinates, image = yolodetect.start_detection(image=frame)

    print("detect : ", detect)
    print("object diff : ", object_diff)
    print("center coords : ", center_coordinates)


    if monitor:
        cv2.imshow("hi", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("q pressed")
            break

cap.release()
cv2.destroyAllWindows()