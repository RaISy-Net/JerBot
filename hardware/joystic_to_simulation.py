from serial_Ard import *
import gym
from time import sleep
import pybullet
import matplotlib.pyplot as plt

init_motor_vals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
motor_vals = init_motor_vals.copy()

env = gym.make('gym_luckyBiped:luckyBiped-v1', renders=True)
observation = env.reset()


def joystick():
    global motor_vals, init_motor_vals
    rcvd_list = rcv_from_Ard()

    if(rcvd_list[0] == 0):
        for i in range(4):
            motor_vals[i] = int(rcvd_list[2+i])
    elif(rcvd_list[0] == 1):
        for i in range(4):
            motor_vals[i+4] = int(rcvd_list[2+i])
    if(rcvd_list[1] == 1):
        motor_vals = init_motor_vals.copy()
        env.reset()

    for i in range(8):
        motor_vals[i] = min(1, motor_vals[i])
        motor_vals[i] = max(-1, motor_vals[i])
    return motor_vals

while True:
    for i_episode in range(1000):
        print('NEW EPISODE')
        env.reset()
        r = 0
        for t in range(3000):
            # sleep(0.01)
            action = joystick()
            observation, reward, done, info = env.step(action, 1000)

            # print(action, [int(i*100)/100 for i in observation])
            
            r += reward
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break
        plt.scatter(i_episode, r)
        plt.pause(0.001)
    plt.show()
    env.close()
