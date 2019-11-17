# Biped-Bot

Install the luckyBiped Env with `pip install -e gym-luckyBiped`.
You can create an instance of the environment with `gym.make('gym_luckyBiped:luckyBiped-v0')`

Test the environment using : ```python3 EnvTest.py ```

`sudo python3 -m pip install --user -e gym-luckyBiped`

# TO DO:

- [ ] Instead of giving angles as targetPosition in setJointMotor2, try incremental/decremental values normalized to +-0.05 in one time step.
