class RoundPull:
    def __init__(self,blocks,color):
        self.blocks = blocks
        self.color = color

#f = open("Day2TestInputPt1.txt")
f = open("Day2Input.txt")

roundId = 1
sumPossibleGames = 0
roundPowerSum = 0

#Each line is a game
for l in f:
    pulls = []
    gamePossible = True

    rlist = l.split(":")
    rlistSplit = rlist [1]

    #Have list of pulls in a game after this
    rlistSplit = rlistSplit.split(";")

    for p in rlistSplit:
        #Separate a pull into its constituent colors
        pullColors = p.split(",")  

        for pC in pullColors:
            rp = RoundPull(pC.split()[0], pC.split()[1])    
            pulls.append(rp)

    #At this point, pulls has a list of #blocks / color pairs and we are within the context of a game
    
    #Crux of PT 1 solve
    for pair in pulls:
        if (pair.color=="blue" and int(pair.blocks) > 14):
            gamePossible = False
        elif (pair.color=="red" and int(pair.blocks)  > 12):
            gamePossible = False
        elif (pair.color=="green" and int(pair.blocks)  > 13):
            gamePossible = False
    
    if gamePossible == True:
        sumPossibleGames = sumPossibleGames + roundId

    #Crux of PT 2 solvefor pair in pulls:
    bluePulls = []
    redPulls = []
    greenPulls = []
   
    for pair in pulls:
        if (pair.color=="blue"):
            bluePulls.append(int(pair.blocks))
        elif (pair.color=="red"):
            redPulls.append(int(pair.blocks))
        elif (pair.color=="green"):
            greenPulls.append(int(pair.blocks))

    maxBlue = int(max(bluePulls))
    maxRed = int(max(redPulls))
    maxGreen = int(max(greenPulls))

    roundPowerSum = roundPowerSum + (maxBlue*maxGreen*maxRed)
    roundId = roundId + 1

print("Pt. 1 Solution Sum of Possible Games = " + str(sumPossibleGames))
print("Pt. 2 Solution Sum of Min Color Powers = " + str(roundPowerSum))


