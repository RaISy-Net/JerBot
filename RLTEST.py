from RL import *

agent = torch.load('Elite.gameAI49')

game = 'gym_luckyBiped:luckyBiped-v0'
env = gym.make(game, renders=True)

run1([agent], env, human=True, delaytime=0.1)
