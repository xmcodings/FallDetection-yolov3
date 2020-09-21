import socket
import struct
import time
import imutils
import numpy as np
from PIL import Image


import cv2

class SocketServer:

    def __init__(self, ip, port):
        self.host = ip
        self.port = port
        self.client_sock = None
        self.addr = None
        self.indata = None
        self.outdata = None
        self.server_sock = None


    def host_socket(self):
        self.server_sock = socket.socket(socket.AF_INET)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(1)
        print("기다리는 중")
        self.client_sock, self.addr = self.server_sock.accept()
        print('Connected by', self.addr)

    def send_to_client(self, data):
        #size = len(data)
        #size = len(data)
        #print(size)
        encode_byte_data = data.to_bytes(4, byteorder='little')
        #data = data.encode('utf-8')
        print(data)
        #self.client_sock.sendall(data)
        self.client_sock.send(encode_byte_data)

    def send_image(self, image_encoded):
        self.client_sock.sendall(image_encoded)


    def get_from_client(self):
        data = self.client_sock.recv(4096)
        self.indata = data.encode("utf-8")

    def close_socket(self):
        self.client_sock.close()
        self.server_sock.close()


if __name__ == "__main__":
    ip = "10.210.60.100"
    port = 9999

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    image = imutils.resize(frame, width=300)
    print(image)
    print("===========")

    cap.release()
    bmp_img = cv2.imencode(".bmp", image)
    print(bmp_img)
    b = bytearray(image)
    #print(b)
    print("===========")
    result, data= np.array(bmp_img)
    data = data.tobytes()
    print(data)
    print(len(data))

    testsocket = SocketServer(ip=ip, port=port)


    testsocket.host_socket()

    testsocket.send_to_client(101)

    testsocket.send_image(data)
