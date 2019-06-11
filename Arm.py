from Vector import Vector
#Tis armf have 3 articulations
class Arm():
    def __init__(self, art1Len, art2Len, art3Len):
        self.vector1        =   Vector(0,0,0,art1Len,0,0)
        self.vector2        =   Vector(self.vector1.x, self.vector1.y, self.vector1.z, art2Len, 0, 0)
        self.vector3        =   Vector(self.vector2.x, self.vector2.y, self.vector2.z, art3Len, 0, 0)

        self.maximumReach   = art1Len + art2Len + art3Len

        self.armCore        = {'x' : 0, 'y' : 0, 'z' : 0}

    #Modify a simble part of articulation changinging starting point and gama and
    #tetha angles
    # ipoints  = {'x' : <xValue>, 'y' : <yValue>, 'z' : <zValue>}
    def modifyArticulation(self, vector, gama, theta, iPoints):
        vector.x0       =   iPoints['x']
        vector.y0       =   iPoints['y']
        vector.z0       =   iPoints['z']
        vector.modifyGama( gama )
        vector.modifyTheta( theta )

    #Actualizations using dictionaries
    # {'gama' : <num>, 'tetha' : <num>}
    def actualizeArm(self, vector1Act, vector2Act, vector3Act):
        self.modifyArticulation(self.vector1, vector1Act['gama'], vector1Act['theta'], self.armCore)
        self.modifyArticulation(self.vector2, vector2Act['gama'], vector2Act['theta'], self.getIPointsFromParentVector(self.vector1))
        self.modifyArticulation(self.vector3, vector3Act['gama'], vector3Act['theta'], self.getIPointsFromParentVector(self.vector2))

    def getArmFinalPoint(self):
        return (self.vector3.x , self.vector3.y, self.vector3.z)

    def getIPointsFromParentVector(self, parentVector):
        return {'x': parentVector.x, 'y' : parentVector.y, 'z' : parentVector.z}
