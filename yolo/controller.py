import live_yolo_opencv as yolocv
import cv2
import serial



class Controller:

    def __init__(self):
        self.yolodetect = yolocv.YoloDetection()
        self.toggle_monitor = True

    def monitor_on(self):
        self.toggle_monitor = True

    def monitor_off(self):
        self.toggle_monitor = False

    def start_monitor(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            detect, object_diff, center_coordinates, image = self.yolodetect.start_detection(image=frame)

            print("detect : ", detect)
            #print("object diff : ", object_diff)
            #print("center coords : ", center_coordinates)

            if detect:
                s.write(b'1')
            else:
                s.write(b'0')

            #ardu = s.readline()
            #print(ardu)

            if self.toggle_monitor:
                cv2.imshow("hi", image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("q pressed")
                    break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    s = serial.Serial(port='/dev/tty.usbserial-1420', baudrate=9600, timeout=0)
    cont = Controller()
    cont.start_monitor()


