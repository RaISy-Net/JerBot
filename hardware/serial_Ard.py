import serial
import re
from time import sleep
ser = serial.Serial("/dev/ttyUSB0", 9600)
sleep(2)
print("connection Est")

def rcv_from_Ard():
    ser.write(str.encode('0\n'))
    rcvd = ser.readline().decode('utf-8')  # b'0 0 0 0 0 0\n'
    rcvd_list = [int(d) for d in re.findall(r'-?\d+', rcvd)]
    return rcvd_list

if __name__ == '__main__':
    while True:
        print(rcv_from_Ard())

