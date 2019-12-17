from client import *
from serial_Ard import *
from time import sleep
import re

min_motor_vals = [80, 90, 90, 20, 80, 90, 40, 100]
max_motor_vals = [110, 90, 130, 80, 110, 90, 80, 160]

# init_motor_vals = [59, 133, 113, 119, 136, 95, 98, 110]
init_motor_vals = [90, 90, 90, 80, 90, 90, 80, 100]


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
    for i in range(int(60/steps)):
        motor_vals[2] += steps
        motor_vals[3] -= steps
        motor_vals[6] += steps
        motor_vals[7] -= steps
        move()
        sleep(t)

    for i in range(int(60/steps)):
        motor_vals[2] -= steps
        motor_vals[3] += steps
        motor_vals[6] -= steps
        motor_vals[7] += steps
        move()
        sleep(t)

def jump(t, steps=1):
    global motor_vals
    for i in range(int(60/steps)):
        motor_vals[2] += steps
        motor_vals[3] -= steps
        motor_vals[6] -= steps
        motor_vals[7] += steps
        move()
        sleep(t)

    for i in range(int(60/steps)):
        motor_vals[2] -= steps
        motor_vals[3] += steps
        motor_vals[6] += steps
        motor_vals[7] -= steps
        move()
        sleep(t)

def Arduino_control():
    global motor_vals
    rcvd_list = rcv_from_Ard()

    if(rcvd_list[0]==0):
        for i in range(4):
            motor_vals[i] += int(rcvd_list[2+i])
            # motor_vals[i+4] -= int(rcvd_list[2+i])
    elif(rcvd_list[0]==1):
        for i in range(4):
            motor_vals[i+4] += int(rcvd_list[2+i])
            # motor_vals[i] -= int(rcvd_list[2+i])
    if(rcvd_list[1]==1):
        motor_vals = init_motor_vals.copy()
    # for i in range(2):
    #     motor_vals[i+2] += int(rcvd_list[2+i])
    #     motor_vals[i+6] -= int(rcvd_list[4+i])
    move()

def pitch_balance(rcvd):
    global motor_vals
    rcvd_list = [int(d) for d in re.findall(r'-?\d+', rcvd)]
    print(rcvd_list)
    roll = rcvd_list[0]
    pitch = rcvd_list[2]
    print(roll, pitch)
    Kp_pitch = 0.1
    Kp_roll = 0.1
    motor_vals[2] += int(pitch*Kp_pitch)
    motor_vals[6] -= int(pitch*Kp_pitch)

    motor_vals[0] += int(roll*Kp_roll)
    motor_vals[4] += int(roll*Kp_roll)
    move()


while True:
    rcvd = recv_from_Rpi(100)
    # Arduino_control()

    # gait(0.05, 2)
    # jump(0.05, 1)
    pitch_balance(rcvd)
