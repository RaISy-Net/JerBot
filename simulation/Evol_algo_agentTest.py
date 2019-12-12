from Evol_algo import *
import pybullet

import matplotlib.pyplot as plt 

agent = torch.load('agents/Elite.gameAI41_166.40800000003173')

game = 'gym_luckyBiped:luckyBiped-v1'
env = gym.make(game, renders=True)

pybullet.changeDynamics(1, -1, lateralFriction = 25)

for i in range(20):
    print(run1([agent], env))