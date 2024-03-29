#Python
import random
#Internal
from Arm import Arm


##Exactitud limintada a grados enteros de precicion en etapa 1
class GeneticSolver():
    #This solver works with an arm with 3 articulations
    def __init__(self, art1Len, art2Len, art3Len, goalPoint):
        self.arm            =   Arm(art1Len, art2Len, art3Len)
        self.goalPoint      =   goalPoint

    def generateRandomAngle(self, topAngle = 360, minAngle = 0):
        return random.randint(minAngle, topAngle)

    # Radiactive mutations random, at least 2 mutations shlould ocour
    def mutantAngle(self, angle, topAngle = 360, minAngle = 0):
        mutations       = random.randint(2,8)
        mutantAngle     = self.generateRandomAngle()
        return self.crossAngles(angle, mutantAngle, mutations, False)


    def crossAngles(self, angleP, angleM, modifications, replacement = True):
        modifiedGens = set()
        anglePL = list('{0:09b}'.format(angleP))
        angleML = list('{0:09b}'.format(angleM))
        #print('angle Parent {2} :  {0}   ange Mother {3} : {1}'.format(anglePL, angleML, angleP, angleM))
        for modificationCicle in range (modifications):
            randomGenModification = random.randint(0, len(anglePL) - 1)
            if not replacement:
                if randomGenModification in modifiedGens:
                    while randomGenModification in modifiedGens:
                        randomGenModification = random.randint(0, len(anglePStr)- 1)
                    modifiedGens.add(randomGenModification)
            anglePL[randomGenModification] =  angleML[randomGenModification]
        return int( ''.join( anglePL ), 2 )

    def makeAChild( self, angleP, angleM ):
        return self.crossAngles( angleP, angleM, 4, False )

    #Litter is a number of new individuals
    def generateNewGenGeneration(self, newIndividualsNum):
        litter      = []
        for element in range(newIndividualsNum):
            theta = self.generateRandomAngle()
            gama  = self.generateRandomAngle(topAngle = 180, minAngle = 0)
            litter.append( {'theta' : theta, 'gama' :  gama } )
        return litter

    def mixBestSpecimens(self, groupA, groupB):
        childGeneration = []
        for elementInA, elementInB in groupA, groupB:
            nElementTheta = self.crossAngles( elementInA['theta'], elementInB['theta'], 4)
            nElementGama  = self.crossAngles( elementInA['gama'],  elementInB['gama'],  4)
            childGeneration.append((nElementTheta, nElementGama))
        return childGeneration



if __name__ == "__main__":
    gs = GeneticSolver(1,1,1,1)
    #print(gs.makeAChild(30, 120))
    #print(gs.mutantAngle(24))
    element1a   = {'theta' : 10,    'gama' : 125 }
    element2a   = {'theta' : 25,    'gama' : 69}
    element1b   = {'theta' : 280,   'gama' : 52}
    element2b   = {'theta' : 19,    'gama' : 158}
    element1    = [element1a, element2a]
    element2    = [element2a, element2b]
    print(gs.mixBestSpecimens(element1, element2))
