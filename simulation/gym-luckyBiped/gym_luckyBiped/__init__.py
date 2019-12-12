from gym.envs.registration import register

register(
    id='luckyBiped-v0',
    entry_point='gym_luckyBiped.envs:luckyBipedEnv',
)

register(
    id='luckyBiped-v1',
    entry_point='gym_luckyBiped.envs:luckyBipedEnvStaticBalance',
)