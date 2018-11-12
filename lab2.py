from math import pi
import numpy as np
from matplotlib import pyplot as plt


class Hurricane(object):
    def __init__(self, x=0.0, y=0.0, gamma=1.0):
        self.x = x
        self.y = y
        self.gamma = gamma

    def getX(self):
        return self.x

    def getY(self):

        return self.y

    def getGamma(self):

        return self.gamma

    def setX(self, n):

        self.x = n

    def setY(self, n):

        self.y = n

    def setGamma(self, n):

        self.gamma = n

    def __repr__(self):
        return "<__main__.Hurricane: x = " + str(self.x) + "; y = " + str(
            self.y) + "; gamma = " + str(self.gamma) + ">"


class HurricaneList():
    def __init__(self, delta_r = 0.1, arr_t = []):
        self.delta_r = delta_r
        self.arr_t = arr_t

    def singleVelocity(self, h, x, y):
        rx = x - float(h.getX())
        ry = y - float(h.getY())
        r = rx * rx + ry * ry + self.delta_r * self.delta_r
        coef = (0.5 * float(h.getGamma())) / (pi * r)
        vx = coef * (float(h.getY()) - y)
        vy = coef * (x - float(h.getX()))
        return vx, vy

    def generalVelocity(self, objs, x, y ):
        vx = 0.0
        vy = 0.0
        for h in objs:
            val = self.singleVelocity(h, x, y)
            vx = vx + val[0]
            vy = vy + val[1]
        return vx, vy

    def nextEuler(self, objs, x, y):
        nextV = self.generalVelocity(objs, x, y)
        rx = x + nextV[0]*0.8
        ry = y + nextV[1]*0.8
        return rx, ry

    def dictEuler(self, objs, x_start, y_start):
        self.arr_t.append((x_start, y_start))
        check_para = x_start, y_start
        for i in range(100):
            check_para = self.nextEuler(objs, check_para[0], check_para[1])
            self.arr_t.append(check_para)
        # print(self.arr_t)
        return (self.arr_t)

    def nextAdams(self, objs, x, y, prevV):
        nextV = self.generalVelocity(objs, x, y)
        rx = x + (3 * nextV[0] - prevV[0]) / 2
        ry = y + (3 * nextV[1] - prevV[1]) / 2
        return rx, ry

    def dictAdams(self, objs, x_start, y_start):
        self.arr_t.append((x_start, y_start))
        prevV = 0, 0
        check_para = x_start, y_start
        for i in range(10):
            temp = self.generalVelocity(objs, check_para[0], check_para[1])
            check_para = self.nextAdams(objs, check_para[0], check_para[1], prevV)
            self.arr_t.append(check_para)
            prevV = temp
        return (self.arr_t)


number = int(input("Enter the number of hurricane: "))
method = int(input("Enter 1 to choose Euler, enter 2 to choose  Adams: "))
start_x = float(input("Enter x-start coordinate: "))
start_y = float(input("Enter y-start coordinate: "))

objs = list()
for i in range(number):
    x_inp = float(input("Enter x coordinate for hurricane %i :" % (i+1)))
    y_inp = float(input("Enter y coordinate for hurricane %i :" % (i+1)))
    gamma_inp = float(input("Enter gamma coordinate for hurricane %i :" %(i+1)))
    hur = Hurricane()
    hur.setX(x_inp)
    hur.setY(y_inp)
    hur.setGamma(gamma_inp)
    s = i + 1
    print("Hurricane №%d" % s, "\nX coordinate: ", hur.getX(), "\nY coordinate: ", hur.getY(), "\nGamma: ", hur.getGamma())
    objs.append(hur)


hurricane_list = HurricaneList()
hurricane_list.singleVelocity(objs[0], start_x, start_y)
hurricane_list.generalVelocity(objs, start_x, start_y)

arr_x_y = []
data = None
for i in range(len(objs)):
    arr_x_y.append((objs[i].getX(), objs[i].getY()))
if method == 1:
    data = np.array(hurricane_list.dictEuler(objs, start_x, start_y))
elif method == 2:
    data = np.array(hurricane_list.dictAdams(objs, start_x, start_y))
data1 = np.array(arr_x_y)

x, y = data.T
x2, y2 = data1.T
fig, ax = plt.subplots()
plt.axes().set_aspect('equal', adjustable='datalim')
plt.plot(x, y)
plt.scatter(x2, y2, c='r')
plt.show()

