from Evol_algo import *

import matplotlib.pyplot as plt 

agent = torch.load('Elite.gameAI33_17842.0')

game = 'gym_luckyBiped:luckyBiped-v0'
env = gym.make(game, renders=True)

run1([agent], env, human=True, delaytime=0.01)