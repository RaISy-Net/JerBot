import gym


from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

#env = gym.make('CartPole-v1')
env = gym.make('gym_luckyBiped:luckyBiped-v0', renders=True)
env = DummyVecEnv([lambda: env])  # The algorithms require a vectorized environment to run

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=10000)
#model.save('test')

obs = env.reset()
from time import sleep
sleep(3)
for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()