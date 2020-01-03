import time
import math
import copy
import random
import numpy as np
import matplotlib.pyplot as plt
from gym.wrappers import Monitor
import torch
import torch.nn as nn
import torch.nn.functional as F
import gym
from time import sleep


class gameAI(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(game_observation, 128, bias=True),
            nn.ReLU(),
            nn.Linear(128, game_actions, bias=True),
            nn.Tanh()
        )

    def forward(self, inputs):
        x = self.fc(inputs)
        return x


def init_weights(m):

    # nn.Conv2d weights are of shape [16, 1, 3, 3] i.e. # number of filters, 1, stride, stride
    # nn.Conv2d bias is of shape [16] i.e. # number of filters

    # nn.Linear weights are of shape [32, 24336] i.e. # number of input features, number of output features
    # nn.Linear bias is of shape [32] i.e. # number of output features

    if ((type(m) == nn.Linear) | (type(m) == nn.Conv2d)):
        torch.nn.init.xavier_uniform(m.weight)
        m.bias.data.fill_(0.00)


def return_random_agents(num_agents):

    agents = []
    for _ in range(num_agents):

        agent = gameAI()

        for param in agent.parameters():
            param.requires_grad = False
        init_weights(agent)

        agents.append(agent)
    return agents


def run1(agents, envi, human=False, delaytime=1, no_of_steps = 200000):
    reward_agents = []
    for agent in agents:
        agent.eval()  # I think to set it to evaluation mode and not to training mode
        observation = envi.reset()
        rew = 0
        while True:
            if(human):
                sleep(delaytime)
            observation = torch.tensor(observation)
            inp = observation.type('torch.FloatTensor').view(1, -1)
            action = agent(inp).detach().numpy()[0]
            for i in range(len(action)):
                action[i] *= envi.action_space.high[i]
            observation, reward, done, info = envi.step(action, no_of_steps)
            rew = rew+reward
            if(done):
                break
        reward_agents.append(rew)
        # reward_agents.append(s)
    return reward_agents

# %%time
# this function divides agents into {no_of_cores sets of agents}


def run_agents(agents):
    envS = []
    for i in range(no_of_cores):
        envS.append(env)
    env.reset()

    agents = np.array(agents)
    agents = agents.reshape(no_of_cores, -1)

    result_ids = []
    for i in range(no_of_cores):
        result_ids.append(run1(agents[i], envS[i]))

    results = result_ids
    results = np.array(results, dtype=float)
    return results.reshape(agents.shape[0]*agents.shape[1], -1)


def run_agents_n_times(agents, runs):
    avg_score = np.zeros((len(agents), 1))
    for i in range(runs):
        avg_score += run_agents(agents)
    avg_score /= runs
    avg_score = avg_score.reshape(len(agents))
    return avg_score
# %time run_agents_n_times(agents, 1)


def add_elite(agents, sorted_parent_indexes, elite_index=None):
    only_consider_top_n = 20
    print('Only considering top ', only_consider_top_n, ' for elite selection.')
    candidate_elite_index = sorted_parent_indexes[:only_consider_top_n]
    if(elite_index is not None):
        candidate_elite_index = np.append([elite_index], candidate_elite_index)
    candidate_elite_index = candidate_elite_index[:only_consider_top_n]
    # [74, 105, 52, 278, 892, .., 645]

    candidate_elite_agents = []
    for i in candidate_elite_index:
        candidate_elite_agents.append(agents[i])
    candidate_elite_agents = np.array(candidate_elite_agents)
    times = 1
    rewards = run_agents_n_times(candidate_elite_agents, times)
    # [score, score, score, .., score]
    print('Running each elite candidate ', times, ' times.')

    top_score = None
    top_elite_index = None

    for i in range(len(rewards)):
        score = rewards[i]
        print("Score for elite i ", candidate_elite_index[i], " is ", score)

        if(top_score is None):
            top_score = score
            top_elite_index = candidate_elite_index[i]
        elif(score >= top_score):
            top_score = score
            top_elite_index = candidate_elite_index[i]

    print("Elite selected with index ", top_elite_index, " and score", top_score)

    child_agent = copy.deepcopy(agents[top_elite_index])
    return child_agent, top_score


def mutate_each_param(param):
    param += np.random.randn()
    return param


def mutate(agents):
    child_agents = []
    for agent in agents:
        child_agent = copy.deepcopy(agent)
        for param in child_agent.parameters():
            #         print(param.shape)
            if(len(param.shape) == 2):  # weights of linear layer
                total = param.shape[0]*param.shape[1]
                to_mutate = random.sample(
                    range(total), round(total*mutation_rate))
    #             print(len(to_mutate))
                for i in to_mutate:
                    param[i % param.shape[0]][int(i/param.shape[0])] = mutate_each_param(
                        param[i % param.shape[0]][int(i/param.shape[0])])
            elif(len(param.shape) == 1):  # biases of linear layer or conv layer
                to_mutate = random.sample(range(param.shape[0]), max(
                    round(param.shape[0]*mutation_rate), random.randint(0, 1)))
    #             print(to_mutate)
                for i in to_mutate:
                    param[i] = mutate_each_param(param[i])
        child_agents.append(child_agent)
    return child_agents


def mutate_all(agents):
    agents = np.array(agents)
    agents = agents.reshape(no_of_cores, -1)
    result_ids = []
    for i in range(no_of_cores):
        result_ids.append(mutate(agents[i]))
    child_agents = result_ids
    child_agents = np.array(child_agents)
    return child_agents.reshape(agents.shape[0]*agents.shape[1])

# %time mutate_all(agents)
# %time [mutate(agent) for agent in agents]
# print('')


def return_children(agents, sorted_parent_indexes, elite_index):

    children_agents = []

    # first take selected parents from sorted_parent_indexes and generate N-1 children
    for i in range(len(agents)):

        selected_agent_index = sorted_parent_indexes[np.random.randint(
            len(sorted_parent_indexes))]
        children_agents.append(agents[selected_agent_index])  # add mutate here
    children_agents = mutate_all(children_agents)

    # now add one elite
    children_agents = children_agents.tolist()
    children_agents.pop(0)
    elite_child, elite_score = add_elite(
        agents, sorted_parent_indexes, elite_index)
    children_agents.append(elite_child)
    elite_index = len(children_agents)-1  # it is the last one

    return children_agents, elite_index, elite_score

# %time return_children(agents, sorted_parent_indexes, elite_index)


if __name__ == "__main__":

    game = 'gym_luckyBiped:luckyBiped-v1'
    env = gym.make(game, renders=False)

    game_observation = env.observation_space.shape[0]
    game_actions = env.action_space.shape[0]

    # print(env.observation_space)
    # print(env.action_space)
    # print(env.observation_space.low, env.observation_space.high)
    # print(env.action_space.low, env.action_space.high)
    # print(env.action_space.sample())

    # disable gradients as we will not use them
    torch.set_grad_enabled(False)

    no_of_cores = 1
    # initialize N number of agents
    num_agents = 1000
    agents = return_random_agents(num_agents)

    # How many top agents to consider as parents
    top_limit = 20
    best_top_score = -10000000000000000
    mutation_rate = 0.05
    #     mutation_power = 0.02 #hyper-parameter, set from https://arxiv.org/pdf/1712.06567.pdf

    # run evolution until X generations
    generations = 100

    elite_index = None
    for generation in range(generations):
        global g
        g = generation
        # return rewards of agents
        rewards = run_agents_n_times(agents, 1)  # return average of 3 runs
        print('RAN ALL AGENTS')

        # sort by rewards
        # reverses and gives top values (argsort sorts by ascending by default) https://stackoverflow.com/questions/16486252/is-it-possible-to-use-argsort-in-descending-order
        sorted_parent_indexes = np.argsort(rewards)[::-1][:top_limit]
        # [ 92 785 321 682 342  27 946 464  41  21 867 774 893 431 628 399 997 708 820 739]

        top_rewards = []
        for best_parent in sorted_parent_indexes:
            top_rewards.append(rewards[best_parent])

        print("Generation ", generation, " | Mean rewards: ", int(np.mean(rewards)), " | Mean of top 5: ", int(
            np.mean(top_rewards[:5])), " | Mean of top ", top_limit, " : ", int(np.mean(top_rewards[:top_limit])))
        print("Top ", top_limit, " scores", sorted_parent_indexes)
        print("Rewards for top: ", np.array(top_rewards).astype(int))

        # setup an empty list for containing children agents
        children_agents, elite_index, elite_score = return_children(
            agents, sorted_parent_indexes, elite_index)

        # kill all agents, and replace them with their children
        agents = children_agents

        print(
            "------------------------------------------------------------------------------")
        print('')
        if(generation % 5 == 4):
            torch.save(agents[elite_index].fc, 'agents/Elite.gameAI'+str(generation))
        if(elite_score > best_top_score):
            best_top_score = elite_score
            torch.save(agents[elite_index].fc, 'agents/Elite.gameAI' +
                       str(generation)+'_'+str(best_top_score))

# agent = torch.load('agents/Elite.gameAI0_6.408000000000005')
# # agent2 = torch.load('agents/Elite.gameAI4')
# # agent3 = torch.load('agents/Elite.gameAI9')


# game = 'gym_luckyBiped:luckyBiped-v1'
# env = gym.make(game, renders=True)

# for i in range(20):
#     print(run1([agent], env))
