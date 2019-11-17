import pybullet_data
import pybullet
import time
import numpy as np
from gym.utils import seeding
from gym import spaces
import gym
import math
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)


class luckyBipedEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, renders=False):
        self.renders = renders
        if (renders):
            pybullet.connect(pybullet.GUI)
        else:
            pybullet.connect(pybullet.DIRECT)
        # observation_high = np.array([
        #     np.finfo(np.float32).max,
        #     np.finfo(np.float32).max,
        #     np.finfo(np.float32).max,
        #     np.finfo(np.float32).max])
        action_high = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

        self.action_space = spaces.Box(low=-action_high, high=action_high)
        self.observation_space = spaces.Box(low=-2, high=2, shape=(20,))

        self.seed()

        self.dog = pybullet.loadURDF(
            currentdir+"/urdf/luckybiped.urdf", [0, 0, 1.09], flags=pybullet.URDF_USE_SELF_COLLISION)
        self.plane = pybullet.loadURDF(os.path.join(
            pybullet_data.getDataPath(), "plane.urdf"), 0, 0, 0)
        self.numJoints = pybullet.getNumJoints(self.dog)
        self.timeStep = 1.0/240
        self.currentSimTime = 0.0
        #pybullet.setJointMotorControl2(self.cartpole, 1, pybullet.VELOCITY_CONTROL, force=0)
        pybullet.setGravity(0, 0, -10)
        # pybullet.setTimeStep(self.timeStep)
        pybullet.setRealTimeSimulation(0)
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def computeState(self):
        bodyState = pybullet.getLinkState(self.dog, 0)
        bodypos = bodyState[0]
        bodyquat = bodyState[1]
        pos, rot = pybullet.getBasePositionAndOrientation(self.dog)
        rotmat = pybullet.getMatrixFromQuaternion(rot)
        self.state = {"JointPosition": [pybullet.getJointState(self.dog, i)[0] for i in range(self.numJoints)],
                      "JointVelocity":  [pybullet.getJointState(self.dog, i)[1] for i in range(self.numJoints)],
                      "bodyRot": rotmat,
                      "bodyPos": bodypos,
                      "bodyquat": bodyquat}
        self.stateToReturn = np.array(
            [self.state['JointPosition'], self.state['JointVelocity']]).flatten()

    def step(self, action):
        pybullet.stepSimulation()
        self.currentSimTime += self.timeStep

        self.computeState()

        jp = self.state["JointPosition"]
        #jv = self.state["JointVelocity"]

        bodyx = self.state["bodyPos"][0]
        #print( bodypos[0] )
        # There are multiple possible choice of motor control, for the moment we settle on relative continuous position control
        # We chose this because it explores less so it should be faster to learn provided that we stay close to a path to the solution
        # jp[i]+
        for i in range(self.numJoints):
            pybullet.setJointMotorControl2(
                self.dog, i, pybullet.POSITION_CONTROL, targetPosition=action[i], force=500)
            #pybullet.setJointMotorControl2(self.dog, i, pybullet.VELOCITY_CONTROL, targetVelocity=jv[i]+deltav, force=500)

        hasFallen = self.state["bodyPos"][2] < 0.2
        #print( self.state["bodyPos"][2])
        pos, rot = pybullet.getBasePositionAndOrientation(self.dog)

        rotmat = pybullet.getMatrixFromQuaternion(rot)
        # or the transpose : pybullet.getMatrixFromQuaternion(rot)[6:9]
        upv = np.array([rotmat[2], rotmat[5], rotmat[8]])
        hasFallenOrient = False
        # we compute the dot product of 0 0 1 with upv
        # the angle between the global z axis and the z axis of the base is the arccos of this dotproduct
        # 0.95 ~ cos( 18.5° )
        if(upv[2] < 0.9):
            hasFallenOrient = True

        done = self.currentSimTime > 1000.0 or hasFallen or hasFallenOrient or np.isnan(
            bodyx)

        Wvel = 2.0
        We = 0.05*0
        delX = np.nan_to_num(pos[0]-self.previousPos[0])
        delE = 0
        for i in range(self.numJoints):
            delE += pybullet.getJointState(self.dog, i)[3]
        reward = Wvel*np.sign(delX)*max(abs(delX), 0.1)-We*delE
        # reward = 1

        if hasFallen or hasFallenOrient:
            reward = reward - 500.0

        self.previousPos = pos

        return self.stateToReturn, reward, done, {}

    def reset(self):
        self.currentSimTime = 0.0
        pybullet.resetBasePositionAndOrientation(
            self.dog, [0, 0, 1.09], [0, 0, 0.707, 0.707])
        for i in range(self.numJoints):
            pybullet.resetJointState(self.dog, i, 0, 0)

        pos, rot = pybullet.getBasePositionAndOrientation(self.dog)
        self.previousPos = pos
        #initialCartPos = self.np_random.uniform(low=-0.5, high=0.5, size=(1,))
        #initialAngle = self.np_random.uniform(low=-0.5, high=0.5, size=(1,))
        #pybullet.resetJointState(self.cartpole, 1, initialAngle)
        #pybullet.resetJointState(self.cartpole, 0, initialCartPos)

        #self.state = pybullet.getJointState(self.cartpole, 1)[0:2] + pybullet.getJointState(self.cartpole, 0)[0:2]
        self.state = {}
        self.computeState()

        return self.stateToReturn

    def render(self, mode='human', close=False):
        # time.sleep(0.01)
        return

    def close(self):
        if(self.renders):
            pybullet.resetSimulation()
