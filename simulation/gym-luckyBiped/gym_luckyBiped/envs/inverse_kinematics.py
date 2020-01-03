import pybullet as p
import pybullet_data
import time
import math
from datetime import datetime
import os
import inspect

currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
p.connect(p.GUI)

p.loadURDF(os.path.join(pybullet_data.getDataPath(), "plane.urdf"), 0, 0, 0)
kukaId = p.loadURDF(currentdir+"/urdf/luckybiped.urdf",
                    [0, 0, 1.2], flags=p.URDF_USE_SELF_COLLISION)
p.resetBasePositionAndOrientation(kukaId, [0, 0, 1.2], [0, 0, 0, 1])
kukaEndEffectorIndex = 9
numJoints = p.getNumJoints(kukaId)
# if (numJoints != 7):
#     print('------------------------------------------------------------------------------------------------------------------------------')
#     exit()

# lower limits for null space
ll = [-.967, -2, -2.96, 0.19, -2.96, -2.09, -3.05]
# upper limits for null space
ul = [.967, 2, 2.96, 2.29, 2.96, 2.09, 3.05]
# joint ranges for null space
jr = [5.8, 4, 5.8, 4, 5.8, 4, 6]
# restposes for null space
rp = [0, 0, 0, 0.5 * math.pi, 0, -math.pi * 0.5 * 0.66, 0]
# joint damping coefficents
jd = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

for i in range(numJoints):
    p.resetJointState(kukaId, i, 0)

p.setGravity(0, 0, -10)
t = 0.
prevPose = [0, 0, 0]
prevPose1 = [0, 0, 0]
prevPose2 = [0, 0, 0]
hasPrevPose = 0
useNullSpace = 0

useOrientation = 0
# If we set useSimulation=0, it sets the arm pose to be the IK result directly without using dynamic control.
# This can be used to test the IK result accuracy.
useSimulation = 1
useRealTimeSimulation = 0
ikSolver = 0
p.setRealTimeSimulation(useRealTimeSimulation)
# trailDuration is duration (in seconds) after debug lines will be removed automatically
# use 0 for no-removal
trailDuration = 15

i = 0
while 1:
    i += 1
    # p.getCameraImage(320,
    #                 200,
    #                 flags=p.ER_SEGMENTATION_MASK_OBJECT_AND_LINKINDEX,
    #                 renderer=p.ER_BULLET_HARDWARE_OPENGL)
    if (useRealTimeSimulation):
        dt = datetime.now()
        t = (dt.second / 60.) * 2. * math.pi
    else:
        t = t + 0.1

    if (useSimulation and useRealTimeSimulation == 0):
        p.stepSimulation()

    for i in range(1):
        pos = [-0.15 , 0.1 * math.cos(t), 0.2 + 0.1 * math.sin(t)]

        if (useNullSpace == 1):
            jointPoses = p.calculateInverseKinematics(kukaId,
                                                      kukaEndEffectorIndex,
                                                      pos,
                                                      lowerLimits=ll,
                                                      upperLimits=ul,
                                                      jointRanges=jr,
                                                      restPoses=rp)
        else:
            jointPoses = p.calculateInverseKinematics(kukaId,
                                                      kukaEndEffectorIndex,
                                                      pos,
                                                      solver=ikSolver)

        print(jointPoses)
        for i in range(numJoints):
            p.setJointMotorControl2(bodyIndex=kukaId,
                                    jointIndex=i,
                                    controlMode=p.POSITION_CONTROL,
                                    targetPosition=jointPoses[i],
                                    targetVelocity=0,
                                    force=500,)

    ls = p.getLinkState(kukaId, kukaEndEffectorIndex)
    if (hasPrevPose):
        p.addUserDebugLine(prevPose, pos, [0, 0, 0.3], 1, trailDuration)
        p.addUserDebugLine(prevPose1, ls[4], [
                           1, 0, 0], 1, trailDuration)  # red
        # p.addUserDebugLine(prevPose2, ls[0], [
        #                    0, 1, 0], 1, trailDuration)  # green
    prevPose = pos
    prevPose1 = ls[4]
    prevPose2 = ls[0]
    hasPrevPose = 1
p.disconnect()
