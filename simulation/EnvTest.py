import gym
from time import sleep
import pybullet
import matplotlib.pyplot as plt

env = gym.make('gym_luckyBiped:luckyBiped-v0', renders = True, realWorld = 0)
observation = env.reset()

for i_episode in range(1000):
    print('NEW EPISODE')
    env.reset()
    r = 0
    for t in range(3000):
        # sleep(0.1)
        action = env.action_space.sample()
        action = [1,1,1,1,-1,-1,1,1]
        action = [0,0,0,0,0,0,0,0]
        observation, reward, done, info = env.step(action, 800)
        r+=reward
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            print('reward: '+str(r))
            break
    plt.scatter(i_episode, r)
    plt.pause(0.001)
plt.show()
env.close()

