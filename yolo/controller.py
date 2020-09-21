import live_yolo_opencv as yolocv
import cv2
import tkinter as tk
import threading
from PIL import Image, ImageTk
import imutils
import socketServer
import numpy as np
import traceback

import sys


import serial



class Controller:

    def __init__(self, vs, serial, socket):
        self.yolodetect = yolocv.YoloDetection()
        self.toggle_monitor = False
        self.stopEvent = None
        self.window = tk.Tk()
        self.window.minsize(300, 100)
        self.frame = None
        self.panel = None
        self.cap = vs
        self.labels = open("data/coco.names").read().strip().split("\n")
        self.socket_server = socket

        self.s = serial
        self.btn_start = tk.Button(self.window, text="monitor!", command=self.monitor_toggle)
        self.lbl_status = tk.Label(master=self.window, text="Status : ")
        self.lbl_status_bar = tk.Label(master=self.window, text=" good ", background="green")

        self.lbl_detected_objs = tk.Label(master=self.window, text = "nothing")

        self.lbl_status_bar.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
        self.lbl_status.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
        self.lbl_detected_objs.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
        self.btn_start.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)



        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.start_monitor())
        self.thread.start()
        # set a callback to handle when the window is closed
        self.window.wm_title("Fall Detection")
        self.window.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def onClose(self):
        self.stopEvent.set()
        self.cap.release()
        cv2.destroyAllWindows()
        self.window.quit()

    def monitor_toggle(self):
        if self.toggle_monitor is False:
            self.toggle_monitor = True
            self.btn_start["text"] = "monitor is on!"
            self.panel.pack(side="right", padx=10, pady=10)

        else:
            self.toggle_monitor = False
            self.btn_start["text"] = "monitor is off"
            self.panel.pack_forget()

    def start_monitor(self):
        #try:

        #while not self.stopEvent.is_set():
        ret, frame = self.cap.read()
        detect, object_diff, center_coordinates, image = self.yolodetect.start_detection(image=frame)
        #print("detect : ", detect)
        #print("object diff : ", object_diff)
        #print("center coords : ", center_coordinates)

        if detect == 2:
            self.s.write(b'1')
            print("detect human")
            self.lbl_status_bar["text"] = "bad"
            self.lbl_status_bar.configure(background="red")
            self.lbl_detected_objs["text"] = "detected : " + object_diff
        elif detect == 1:
            print("detect object")
            self.s.write(b'2')
            self.lbl_status_bar["text"] = "warning"
            self.lbl_status_bar.configure(background="orange")
            self.lbl_detected_objs["text"] = "detected : " + object_diff

        else: # detect = 0
            self.lbl_status_bar["text"] = "good"
            self.lbl_status_bar.configure(background="green")
            self.lbl_detected_objs["text"] = "detected : nothing"
            self.s.write(b'0')

        ardu = self.s.readline()
        ardu_decode = ardu.decode("utf-8")
        ardu_decode1 = ardu.decode()

        print(ardu)
        ardu_decode = ardu_decode.replace("\r","")
        ardu_decode = ardu_decode.replace("\n","")

        if ardu_decode =="101":
            # 센서가 작동해서 에어벡 터짐
            print("send to client!!")
            socket.send_to_client(101)

        #print(self.toggle_monitor)
        if self.panel is None:
            self.panel = tk.Label()
            self.panel.pack(side="right", padx=10, pady=10)
        if self.toggle_monitor and image is not 0:
            image = imutils.resize(image, width=300)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image=image)
            self.panel.configure(image=image)
            self.panel.image = image
            #self.panel.after(1,self.start_monitor)
            '''
            cv2.imshow("hi", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("q pressed")
                break
            '''

        self.panel.after(1, self.start_monitor)
        #except:
        #    print("[runtime error during frame fetch]")
        #    print(sys.exc_info()[0])





if __name__ == "__main__":
    s = serial.Serial(port='/dev/tty.usbserial-1420', baudrate=9600, timeout=0)
    ip = "192.168.0.4"
    port = 9999
    socket = socketServer.SocketServer(ip=ip, port=port)
    socket.host_socket()
    a = s.readline()
    #cont = Controller(s)
    cap = cv2.VideoCapture(0)
    cont = Controller(vs=cap, serial=s, socket=socket)
    #cont.start_monitor()
    cont.window.mainloop()



