from client import *
from serial_Ard import *
from time import sleep
import re
from gait import *

min_motor_vals = [80, 70, 90, 20, 90, 70, 20, 100]
max_motor_vals = [110, 110, 150, 80, 120, 110, 80, 160]

# init_motor_vals = [59, 133, 113, 119, 136, 95, 98, 110]
init_motor_vals = [96, 90, 100, 70, 104, 80, 60, 110]
prev_pitch = 0
sum_pitch = 0
prev_roll = 0
sum_roll = 0

motor_vals = init_motor_vals.copy()


def move():
    global min_motor_vals, max_motor_vals, init_motor_vals, motor_vals

    for i in range(8):
        motor_vals[i] = min(max_motor_vals[i], motor_vals[i])
        motor_vals[i] = max(min_motor_vals[i], motor_vals[i])
    val_to_send = ''
    for i in range(8):
        val_to_send += str(motor_vals[i]) + ' '
    # print(val_to_send)
    send_to_Rpi(val_to_send)


def gait(t, steps=1):
    global motor_vals
    for i in range(int(30/steps)):
        motor_vals[2] += steps
        motor_vals[3] -= steps
        motor_vals[6] += steps
        motor_vals[7] -= steps
        rcvd = recv_from_Rpi(100)
        move()
        sleep(t)

    for i in range(int(30/steps)):
        motor_vals[2] -= steps
        motor_vals[3] += steps
        motor_vals[6] -= steps
        motor_vals[7] += steps
        rcvd = recv_from_Rpi(100)
        move()
        sleep(t)


def jump(t, steps=1):
    global motor_vals
    for i in range(int(60/steps)):
        motor_vals[2] += steps
        motor_vals[3] -= steps
        motor_vals[6] -= steps
        motor_vals[7] += steps
        rcvd = recv_from_Rpi(100)
        move()
        sleep(t)

    for i in range(int(60/steps)):
        motor_vals[2] -= steps
        motor_vals[3] += steps
        motor_vals[6] += steps
        motor_vals[7] -= steps
        rcvd = recv_from_Rpi(100)
        move()
        sleep(t)


def Arduino_control():
    rcvd = recv_from_Rpi(100)
    global motor_vals
    rcvd_list = rcv_from_Ard()

    if(rcvd_list[0] == 0):
        for i in range(4):
            motor_vals[i] += int(rcvd_list[2+i])
            # motor_vals[i+4] -= int(rcvd_list[2+i])
    elif(rcvd_list[0] == 1):
        for i in range(4):
            motor_vals[i+4] += int(rcvd_list[2+i])
            # motor_vals[i] -= int(rcvd_list[2+i])
    if(rcvd_list[1] == 1):
        motor_vals = init_motor_vals.copy()
    # for i in range(2):
    #     motor_vals[i+2] += int(rcvd_list[2+i])
    #     motor_vals[i+6] -= int(rcvd_list[4+i])
    move()


def dynamic_balance():
    rcvd = recv_from_Rpi(100)
    global motor_vals, prev_pitch, sum_pitch, prev_roll, sum_roll
    rcvd_list = [int(d) for d in re.findall(r'-?\d+', rcvd)]
    print(rcvd_list)
    roll = rcvd_list[0]
    pitch = rcvd_list[2]
    #roll += 15
    print(roll, pitch)
    Kp_pitch = 0.03
    Kd_pitch = Kp_pitch*10
    Ki_pitch = 0
    Kp_roll = 0
    Kd_roll = 0
    Ki_roll = 0
    PID_pitch = int(pitch*Kp_pitch + (pitch-prev_pitch)
                    * Kd_pitch + sum_pitch*Ki_pitch)
    PID_roll = int(roll*Kp_roll + (roll-prev_roll)*Kd_roll + sum_roll*Ki_roll)
    motor_vals[2] += PID_pitch
    motor_vals[6] -= PID_pitch
    # motor_vals[3] += PID_pitch
    # motor_vals[7] -= PID_pitch

    motor_vals[0] += PID_roll
    motor_vals[4] += PID_roll
    move()

    prev_pitch = pitch
    prev_roll = roll
    sum_pitch += pitch
    sum_roll += roll


def st_line(length, delay):
    global motor_vals
    x = -1*length
    y = 34
    X = []
    Y = []

    while x <= (length):

        # y=math.sqrt((l1+l2)*(l1+l2)-x*x)
        Y.append(-y)
        # print('x:', x, 'y:', -y)
        motor_values = Inve_kinematics(x, -y, motor_vals)
        recv_from_Rpi(100)
        move()
        X.append(x)
        x += 1
        sleep(delay)
    while x >= -1*length:
        Y.append(-y)
        # print('x:', x, 'y:', -y)
        motor_values = Inve_kinematics(x, -y, motor_vals)
        recv_from_Rpi(100)
        move()
        X.append(x)
        x -= 1
        sleep(delay)


def recvAndMove():
    recv_from_Rpi(100)
    move()
    sleep(0.04)


def check_BOT():
    global motor_vals, init_motor_vals, min_motor_vals, max_motor_vals
    for i in range(4):
        c = 1
        while(motor_vals[i] < max_motor_vals[i] and motor_vals[i+4] < max_motor_vals[i+4]):
            motor_vals[i] += c
            motor_vals[i+4] += c
            recvAndMove()
        print('TO MAX')
        while(motor_vals[i] > min_motor_vals[i] and motor_vals[i+4] > min_motor_vals[i+4]):
            motor_vals[i] -= c
            motor_vals[i+4] -= c
            recvAndMove()
        print('TO MIN')
        while(motor_vals[i] < init_motor_vals[i] and motor_vals[i+4] < init_motor_vals[i+4]):
            motor_vals[i] += c
            motor_vals[i+4] += c
            recvAndMove()
        print('MID')

while True:
    # check_BOT()

    # gait(0.05, 2)
    # jump(0.05, 2)
    # st_line(15, 0.1)
    dynamic_balance()

    # Arduino_control()
