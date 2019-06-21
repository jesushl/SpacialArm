import math
def RECM(pr, ar):
    ecm = 0
    for prValue, arValue in zip(pr, ar):
        ecm = ecm  + ( ( prValue - arValue ) ** 2)
    ecm = ecm / len (pr)
    return math.sqrt(ecm)


if __name__ == "__main__":
    #pr = [1.3,1.5,2.6,4.2,4.8]
    #ar = [1,2,3,4,5]
    average = []
    for i in range(0,16):
        average.append(4.5)


    print(RECM(pr, ar))
#   A    D   B  C
