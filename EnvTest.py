import gym
from time import sleep
import pybullet

env = gym.make('gym_luckyBiped:luckyBiped-v0', renders=True)
observation = env.reset()
print(pybullet.getBasePositionAndOrientation(0))

for i_episode in range(100):
    print('NEW EPISODE')
    env.reset()
    for t in range(1000):
        sleep(0.01)
        action = env.action_space.sample()
        action = [0,0,0,0,0,0,0,0,0,0,0]
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()

