import math
import matplotlib.pyplot as plt

l1 = 19.0
l2 = 19.0


def Inve_kinematics(tx, ty, motor_values):
    d = math.sqrt(tx**2+ty**2)

    if tx == 0:
        theta1 = -1.57079632679 - math.acos((d**2+l1**2-l2**2)/(2*d*l1))
    else:
        theta1 = math.atan2(ty, tx) - math.acos((d**2+l1**2-l2**2)/(2*d*l1))
    # print((-tx**2-ty**2+l1**2+l2**2)/(2*l1*l2))
    theta2 = 3.141-math.acos((l1**2+l2**2 - d**2)/(2*l1*l2))
    t1 = int(math.degrees(theta1))
    t2 = int(math.degrees(theta2))

    motor_values[2] = -1*t1
    motor_values[3] = 90 - t2

    return motor_values

if __name__ == '__main__':
    x = 0
    y = 34
    X = []
    Y = []

    while x <= (15):

        # y=math.sqrt((l1+l2)*(l1+l2)-x*x)
        Y.append(-y)
        print('x:', x, 'y:', -y)
        print(Inve_kinematics(x, -y))
        X.append(x)
        x += 1
    while x >= -15:
        Y.append(-y)
        print('x:', x, 'y:', -y)
        print(Inve_kinematics(x, -y))
        X.append(x)
        x -= 1

    plt.plot(X, Y)
    plt.show()
