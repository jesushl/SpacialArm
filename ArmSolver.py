import math

from GeneticSolver  import GeneticSolver
from Arm            import Arm

class ArmSolver():

    def __init__(self, arm1Len = 3, arm2Len = 2, arm3Len = 1, goalPoint = {'x' :1, 'y' : 1 , 'z' : 1 }):
        self.arm        =  Arm(arm1Len, arm2Len, arm3Len)
        self.goalPoint  =  goalPoint
        self.gs         =  GeneticSolver(arm1Len, arm2Len, arm3Len, goalPoint)
        if not self.isAPossibleShot():
            print('Goal point is too far ')

    # This is the method that creates all population and try to get a result
    #Family1 have a bias
    def getGeneticResult(self, generations, familyPopulation = 10):
        family1 = self.getNewGeneration(familyPopulation)
        family2 = self.getNewGeneration(familyPopulation)
        #New generation combined can have mutations in a grade of 10% of cases
        for generation in range(generations):
            solution = existASolution( family1, family2 )
            if not solution:
                family1  = self.newGenerationCombined(family1, family2)
                family2  = self.mutantAddition(family1, family2)
                if ( generation % 5 ) == 0 :
                    family2 = self.newIndividualsAddition()
            else:
                return solution

    def mutantAddition(self, family1, family2):
        nGeneration     = self.getNewGeneration()
        b

    def newGenerationCombined(self, family1, family2):
        bestIndividuals = {}
        allKeys         = list(family1.keys()) + list(family2.keys())
        sortedBestKeys  = sorted(allKeys)[:-10]
        for bestKey in sortedBestKeys:
            if bestKey in family1:
                bestIndividuals.update( { bestKey : family1[bestKey]  } )
            else:
                bestIndividuals.update( { bestKey : family2[bestKey] } )
        return bestIndividuals


    def getPossibleSolution(self, family):
        bestFamilySolution = sorted(family.keys())[1]
        if bestFamilySolution == 0 :
            return family[bestFamilySolution]
        else:
            return False


    #generationColl {<evaluation> : [{'arm1': {'gama' :<gamaAngle>, 'theta' : <theta> }, 'arm2' : ...}]}
    def getNewGeneration(self, generationZise = 10):
        nGenerationAnglesL1 = self.gs.generateNewGenGeneration(generationZise)
        nGenerationAnglesL2 = self.gs.generateNewGenGeneration(generationZise)
        nGenerationAnglesL3 = self.gs.generateNewGenGeneration(generationZise)
        generationColl      = {}
        for anglesArm1, anglesArm2, anglesArm3 in zip(nGenerationAnglesL1, nGenerationAnglesL2, nGenerationAnglesL3):
            evaluation = self.evaluateAnglesGroup(anglesArm1, anglesArm2, anglesArm3)
            angles  = {'arm1' : anglesArm1, 'arm2' : anglesArm2, 'arm3' : anglesArm3}
            if evaluation in generationColl:
                generationColl[evaluation].append(angles)
            else:
                generationColl.update( { evaluation : [angles] } )
        return generationColl

    def getCrosses(self, generationColl, generationColl2):
        bestGen1    = sorted(generationColl.keys())
        bestGen2    = sorted(generationColl2.keys())
        nChilds     = {}
        for parent, child in bestGen1, bestGen2:
            for pArm, cArm in bestGen1[parent], bestGen2[child]:
                nArm        = self.combineArmStatus(pArm, cArm)
                evaluation  = self.evaluateAnglesGroup(nArm['arm1'], nArm['arm2'], nArm['arm3'])
                if evaluation in nChilds:
                    nChilds[evaluation].append(nArm)
                else:
                    nChilds.update({evaluation : [nArm] } )
        return nChilds

    # pArm  {'arm1' : {'alpha' : <alpha>, 'theta' : <theta> }, 'arm2' : {'alpha' : <alpha>, 'theta' : <theta> } , 'arm3' : {'alpha' : <alpha>, 'theta' : <theta> } }
    def combineArmStatus(self, pArm, cArm):
        combinedResult      = {}
        for armKey in pArm:
            for angleKey in pArm[pKeys]:
                # { 'armX' : { 'alpha'  : <crossAngles> }  }
                combinedResult.update( { armKey : { angleKey :  gs.crossAngles( pArm[armKey][angleKey], pArm[armKey][angleKey] ) } } )
        return combinedResult

    def evaluateAnglesGroup(self, anglesArm1, anglesArm2, anglesArm3):
        self.arm.actualizeArm(anglesArm1, anglesArm2, anglesArm3)
        distanceToGoal = self.pointsDistance(self.goalPoint, self.arm.getArmFinalPoint())
        return distanceToGoal

    def pointsDistance(self, point1, point2):
        pointDistance = (point1['x'] - point2['x']) ** 2 + (point1['y'] + point2['y']) ** 2 + (point1['z'] + point2['z']) ** 2
        pointDistance = math.sqrt(pointDistance)
        return pointDistance

    def isAPossibleShot(self):
        pointDistance = self.goalPoint['x'] ** 2 + self.goalPoint['y'] ** 2 + self.goalPoint['z'] ** 2
        pointDistance =  math.sqrt(pointDistance)
        if pointDistance > self.arm.maximumReach :
            return False
        return True


if __name__ == '__main__' :
    ars =  ArmSolver()
    gen1 = ars.getNewGeneration()
    print('gen1 : {}'.format(gen1.keys()))
    gen2 = ars.getNewGeneration()
    print('gen2 : {}'.format(gen2.keys()))
    #print( ars.newGenerationCombined( gen1, gen2 ) )
    print('Combinatory : {}'.format(ars.newGenerationCombined( gen1, gen2 ).keys()))
