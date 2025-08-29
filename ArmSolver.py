import math

from GeneticSolver  import GeneticSolver
from Arm            import Arm

class ArmSolver():

    def __init__(self, arm1Len = 3, arm2Len = 2, arm3Len = 1, goalPoint = {'x' :1, 'y' : 1 , 'z' : 1 }):

        self.exactitudeParams = (0.05)
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
            print('Generation : {}'.format(generation))
            solution = self.existASolution( family1, family2 ) #TOOD
            if not solution:
                family1  = self.newGenerationCombined(family1, family2, familyPopulation)
                #print('Family 2 : {}'.format(family2))
                family2  = self.mutantAddition(family2, family1)
                #print('Mutation! : {}'.format(family2))
                if ( generation % 5 ) == 0 :
                    #print(' $$$$$$$$$$$$$ New generation random addition')
                    family2 = self.newIndividualsAddition(family2, familyPopulation)
            else:
                print(solution)
                return solution

    def newIndividualsAddition(self, family, familyPopulation):
        keys                = sorted(family.keys())
        preservedMembers    = int(familyPopulation / 2)
        bestResults         = keys[:preservedMembers]
        newMembers          = self.getNewGeneration(familyPopulation)
        return self.newGenerationCombined(family, newMembers, familyPopulation)



    ##Exactitude params for a satisfactory solution
    def existASolution(self, family1, family2):
        listResults     = list(family1.keys()) + list(family2.keys())
        #print(listResults)
        results         =  sorted(listResults)

        print('Aproximacion : {}'.format(results[0]))
        if results[0] < self.exactitudeParams and results[0] > self.exactitudeParams * -1:
            if results[0] in family1:
                return family1[results[0]]
            else :
                return family2[results[0]]
        return False

    #MutantAddition generates mutants by each family and only choose the
    #the most capable mutants, probably some mutants are superior of
    # current families or worst ...
    def mutantAddition(self, familyReceiber, familyColaborative):
        mutantGeneration = {}
        #print('Mutant Addition')
        #print('family Receiber : {}'.format(familyReceiber))
        #print('family Colaborative : {}'.format(familyColaborative))
        for familyMember1, familyMember2 in zip(familyReceiber, familyColaborative): ##Moving on arm evaluations
            mutant1 = {}
            mutant2 = {}
            #{'arm1' : {'gama' : <>, 'theta' : <>}}
            for armM1, armM2 in zip(familyReceiber[familyMember1][0], familyColaborative[familyMember2][0]):
                mutantArm1  = self.mutantArm(familyReceiber[familyMember1][0][armM1])
                mutantArm2  = self.mutantArm(familyColaborative[familyMember2][0][armM2])
                mutant1.update({ armM1   : mutantArm1 })
                mutant2.update({ armM2   : mutantArm2 })
            #print('mutant1 : {}'.format(mutant1))
            eval1       = self.evaluateAnglesGroup(mutant1['arm1'], mutant1['arm2'], mutant1['arm2'])
            eval2       = self.evaluateAnglesGroup(mutant2['arm1'], mutant2['arm2'], mutant2['arm2'])
            mutantGeneration.update({ eval1 : mutant1 })
            mutantGeneration.update({ eval2 : mutant2 })
        bestMutants                 = sorted(mutantGeneration.keys())
        bestFamilyOriginals         = sorted(familyReceiber.keys())
        receiberFamilyNumMembers    = len(familyReceiber.keys())
        familyPreservedMembers      = int(receiberFamilyNumMembers / 2)
        newReceptorFamily   = {}
        familyMemberIndex   = 0
        mutantElementIndex  = 0
        for member in range(0, receiberFamilyNumMembers):
            if member < familyPreservedMembers:
                #print('Best familie members {}'.format(familyReceiber[bestFamilyOriginals[familyMemberIndex]]))
                newReceptorFamily.update({bestFamilyOriginals[familyMemberIndex] : familyReceiber[bestFamilyOriginals[familyMemberIndex]]})
                familyMemberIndex       =  familyMemberIndex + 1
            else :
                #print('Best mutants : {}'.format(bestMutants))
                newReceptorFamily.update({bestMutants[mutantElementIndex] : [mutantGeneration[bestMutants[mutantElementIndex]]]})
                #print('Best Mutant additions : {}'.format({bestMutants[mutantElementIndex] : [mutantGeneration[bestMutants[mutantElementIndex]]]}))
                mutantElementIndex      = mutantElementIndex + 1
        familyReceiber  = newReceptorFamily
        return familyReceiber

    def mutantArm(self, armObject):
        nArm    = {}
        nGama   = self.gs.mutantAngle(armObject['gama'], 180)## Z angle
        nTheta  = self.gs.mutantAngle(armObject['theta'])
        nArm.update( { 'gama' : nGama , 'theta' : nTheta }  )
        return nArm

    def newGenerationCombined(self, family1, family2, familyPopulation):
        bestIndividuals = {}
        allKeys         = list(family1.keys()) + list(family2.keys())
        sortedBestKeys  = sorted(allKeys)
        familyMembers   = 0
        for bestKey in sortedBestKeys:
            if bestKey in family1:
                bestIndividuals.update( { bestKey : family1[bestKey]  } )
            else:
                bestIndividuals.update( { bestKey : family2[bestKey] } )
            if familyMembers >= familyPopulation:
                break
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
        combinedResult = {}
        for armKey in pArm:
            combinedResult[armKey] = {}
            for angleKey in pArm[armKey]:
                # { 'armX' : { 'alpha'  : <crossAngles> }  }
                combinedResult[armKey][angleKey] = self.gs.crossAngles( pArm[armKey][angleKey], cArm[armKey][angleKey] )
        return combinedResult

    def evaluateAnglesGroup(self, anglesArm1, anglesArm2, anglesArm3):
        self.arm.actualizeArm(anglesArm1, anglesArm2, anglesArm3)
        distanceToGoal = self.pointsDistance(self.goalPoint, self.arm.getArmFinalPoint())
        return distanceToGoal

    def pointsDistance(self, point1, point2):
        pointDistance = (point1['x'] - point2['x']) ** 2 + (point1['y'] - point2['y']) ** 2 + (point1['z'] - point2['z']) ** 2
        pointDistance = math.sqrt(pointDistance)
        return pointDistance

    def isAPossibleShot(self):
        pointDistance = self.goalPoint['x'] ** 2 + self.goalPoint['y'] ** 2 + self.goalPoint['z'] ** 2
        pointDistance =  math.sqrt(pointDistance)
        if pointDistance > self.arm.maximumReach :
            return False
        return True


if __name__ == '__main__' :
    goalPoint   = {'x' : 2, 'y' :  1, 'z' : 2 }
    ars         = ArmSolver(goalPoint = goalPoint)
    ars.getGeneticResult(generations = 1000)
