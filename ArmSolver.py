import math

from GeneticSolver  import GeneticSolver as gs
from Arm            import Arm

class ArmSolver():

    def __init__(self, arm1Len = 3, arm2Len = 2, arm3Len = 1, goalPoint):
        self.arm        =  Arm(arm1Len, arm2Len, arm3Len)
        self.goalPoint  =  goalPoint
        if not isAPossibleShot():
            print('Goal point is too far ')


    def getNewGeneration(self, generationZise = 10):
        nGenerationAnglesL1 = gs.generateNewGenGeneration(generationZise)
        nGenerationAnglesL2 = gs.generateNewGenGeneration(generationZise)
        nGenerationAnglesL3 = gs.generateNewGenGeneration(generationZise)



    def isAPossibleShot(self):
        pointDistance = goalPoint['x'] ** 2 + goalPoint['y'] ** 2 + goalPoint['z'] ** 2
        pointDistance =  math.sqrt(pointDistance)
        if pointDistance > self.arm.maximumReach :
            return False
        return True
