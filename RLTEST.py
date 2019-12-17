from RL import *

import matplotlib.pyplot as plt 

agent = torch.load('Elite.gameAI33_17842.0')

game = 'gym_luckyBiped:luckyBiped-v0'
env = gym.make(game, renders=True)

run1([agent], env, human=True, delaytime=0.01)


#----------------------------------------------------------------------------------
# x = [1,2,3] 
# # corresponding y axis values 
# y = [2,4,1] 
  
# # plotting the points  
# plt.plot(x, y) 
  
# # naming the x axis 
# plt.xlabel('x - axis') 
# # naming the y axis 
# plt.ylabel('y - axis') 
  
# # giving a title to my graph 
# plt.title('My first graph!') 
  
# # function to show the plot 
# plt.show() 