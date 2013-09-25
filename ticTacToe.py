import copy
import time

theoryCount = 0
before = time.time()
after = 0
pruning = False

def MyBestMove(base):
    global theoryCount, before, after
    bestMove = {}
    bestMove["outcome"] = None
    bestMove["pos"] = None

    for i in range(9):
        if base["spots"][i]["state"] == "":
            base[i] = {}
            base[i]["spots"] = {}
            base[i]["spots"] = copy.deepcopy(base["spots"])            
            base[i]["spots"][i]["state"] = "O"

            theoryCount += 1

            if getGameOverState(base[i]["spots"])["gameOver"]:
                thisOutcome = getGameOverState(base[i]["spots"])["outcome"]
            else:
                # thisPos = EnemyBestMove(base[i])["pos"]
                thisOutcome = EnemyBestMove(base[i])["outcome"]

            if bestMove["outcome"] == None or thisOutcome > bestMove["outcome"]:
                bestMove["outcome"] = thisOutcome
                bestMove["pos"] = i

    return bestMove

def EnemyBestMove(base):
    global theoryCount, before
    bestMove = {}
    bestMove["outcome"] = None
    bestMove["pos"] = None

    for i in range(9):
        
        if base["spots"][i]["state"] == "":
            base[i] = {}
            base[i]["spots"] = {}
            base[i]["spots"] = copy.deepcopy(base["spots"])                        
            base[i]["spots"][i]["state"] = "X"

            theoryCount += 1
            
            if getGameOverState(base[i]["spots"])["gameOver"]:
                thisOutcome = getGameOverState(base[i]["spots"])["outcome"]
            else:
                # thisPos = MyBestMove(base[i])["pos"]
                thisOutcome = MyBestMove(base[i])["outcome"]

            if bestMove["outcome"] == None or thisOutcome < bestMove["outcome"]:
                bestMove["outcome"] = thisOutcome
                bestMove["pos"] = i

    return bestMove

def getGameOverState(spots):
    for team in ["X", "O"]:
        for x in range(3):
            filledSpots = 0
            for spot in spots:
                if spot["col"] == x:
                    if spot["state"] == team:
                        filledSpots += 1
            if filledSpots == 3:
                if team == "X":
                    return {"gameOver": True, "draw": False, "outcome": -1}
                else:
                    return {"gameOver": True, "draw": False, "outcome": 1}
                
        for y in range(3):
            filledSpots = 0
            for spot in spots:
                if spot["row"] == y:
                    if spot["state"] == team:
                        filledSpots += 1
            if filledSpots == 3:
                if team == "X":
                    return {"gameOver": True, "draw": False, "outcome": -1}
                else:
                    return {"gameOver": True, "draw": False, "outcome": 1}

    noBlankSpotsLeft = True
    for i in range(9):
        if spots[i]["state"] == "":
           noBlankSpotsLeft = False
    if noBlankSpotsLeft:
        return {"gameOver": True, "draw": True, "outcome": 0}
    else:
        return {"gameOver": False, "draw": False, "outcome": "TEST!"}


def printToes(spots):
    for y in range(3):
        for x in range(3):
            if spots[x + (y*3)]["state"] == "X":
                print "X",
            elif spots[x + (y*3)]["state"] == "O":
                print "O",
            else:
                print "_",
        print ""
    print "="

def won(spots):
    for team in ["X", "O"]:
        for x in range(3):
            filledSpots = 0
            for spot in spots:
                if spot["col"] == x:
                    if spot["state"] == team:
                        filledSpots += 1
            if filledSpots == 3:
                return team

        for y in range(3):
            filledSpots = 0
            for spot in spots:
                if spot["row"] == y:
                    if spot["state"] == team:
                        filledSpots += 1
            if filledSpots == 3:
                return team
    return False


spots = []
for x in range(3):
    for y in range(3):
        spots.append({"row": x, "col": y, "state": ''})

spots[0]["state"] = "X"

base = {}
base["spots"] = spots
printToes(base["spots"])

print(MyBestMove(base))
print "Theory Count for solution: " + str(theoryCount)
print "Time for solution: " + str(time.time() - before)
