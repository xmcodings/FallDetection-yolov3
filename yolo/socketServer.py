import socket
import struct
import time

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
        self.client_sock.send(image_encoded)


    def get_from_client(self):
        data = self.client_sock.recv(4096)
        self.indata = data.encode("utf-8")

    def close_socket(self):
        self.client_sock.close()
        self.server_sock.close()


if __name__ == "__main__":
    ip = "192.168.0.4"
    port = 9999
    socket = SocketServer(ip=ip, port=port)
    socket.host_socket()
    socket.send_to_client(101)
