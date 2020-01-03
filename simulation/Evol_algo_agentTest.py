from Evol_algo import *
import pybullet

import matplotlib.pyplot as plt 

agent = torch.load('agents/Elite.gameAI89_6.7039999999990485')

game = 'gym_luckyBiped:luckyBiped-v1'
env = gym.make(game, renders=True)

for i in range(20):
    print(run1([agent], env, human = False, no_of_steps = 80000))