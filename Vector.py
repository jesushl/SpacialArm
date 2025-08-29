import numpy as np
import math

class Vector():
    def __init__(self, x0, y0, z0, lenght, theta, gama):
        self.x0     = x0
        self.y0     = y0
        self.z0     = z0
        self.lenght = lenght
        self.theta  = theta
        self.gama   = gama
        self.getVectorPointByComponents(self.theta, self.gama, self.lenght)

    def getVectorComponents(self):
        args = [self.x0, self.y0, self.z0, self.x, self.y, self.z]
        return args

    #theta is the angle in XY plane, gama is from XY to X
    def getVectorPointByComponents(self,theta, gama, vectorLenght):
        self.x      =   self.lenght  * math.cos(theta)  + self.x0
        self.y      =   self.lenght  * math.sin(theta)  + self.y0
        self.z      =   self.lenght  * math.cos(gama)   + self.z0


    def getPointsDistance(self, x0, y0, z0, x, y , z):
        distance   =   math.sqrt(((x - x0) ** 2) + ((y - y0) ** 2) + ((z - z0) ** 2))
        return distance

    def modifyTheta(self, theta):
        self.x      =   self.lenght  * math.cos(theta)  + self.x0
        self.y      =   self.lenght  * math.sin(theta)  + self.y0

    def modifyGama(self, gama):
        self.z      =   self.lenght  * math.cos(gama)   + self.z0
