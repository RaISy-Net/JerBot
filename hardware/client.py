import socket
import random


def send_to_Rpi(msg):
    s.send(bytes(msg, 'utf-8'))


def recv_from_Rpi(msgSize):
    return s.recv(msgSize).decode('utf-8')


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(socket.gethostbyname(socket.gethostname()))
s.connect(('10.42.0.139', 2019))

# if __name__ == "__main__":
#     while True:
#         send_to_Rpi('values are '+str(random.randint(0, 180)))
#         print(recv_from_Rpi(100))
