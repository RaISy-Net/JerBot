from client import *
from serial_Ard import *

init_motor_vals = [59, 133, 113, 119, 136, 95, 98, 110]
motor_vals = init_motor_vals.copy()

while True:
    rcvd_list = rcv_from_Ard()
    
    if(rcvd_list[0]==0):
        for i in range(4):
            motor_vals[i] += int(rcvd_list[2+i])
    elif(rcvd_list[0]==1):
        for i in range(4):
            motor_vals[i+4] += int(rcvd_list[2+i])
    if(rcvd_list[1]==1):
        motor_vals = init_motor_vals.copy()

    for i in range(8):
        motor_vals[i] = min(180, motor_vals[i])
        motor_vals[i] = max(0, motor_vals[i])
    val_to_send = ''
    for i in range(8):
        val_to_send += str(motor_vals[i]) + ' '
    print(val_to_send, recv_from_Rpi(100))
    send_to_Rpi(val_to_send)
