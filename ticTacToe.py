import copy
import time
import json

theoryCount = 0
before = time.time()
after = 0
pruning = False

def MyBestMove(spots):
    global theoryCount, before
    bestMove = {}
    bestMove["outcome"] = None
    bestMove["pos"] = None

    for i in range(9):
        if spots[i]["state"] == "":
            spots[i]["state"] = "O"

            theoryCount += 1

            if getGameOverState(spots)["gameOver"]:
                thisOutcome = getGameOverState(spots)["outcome"]
            else:
                # enemyMove = EnemyBestMove(spots)
                # thisPos = enemyMove["pos"]
                thisOutcome = EnemyBestMove(spots)["outcome"]

            spots[i]["state"] = ""

            if bestMove["outcome"] == None or thisOutcome > bestMove["outcome"]:
                bestMove["outcome"] = thisOutcome
                bestMove["pos"] = i

    return bestMove

def EnemyBestMove(spots):
    global theoryCount, before
    bestMove = {}
    bestMove["outcome"] = None
    bestMove["pos"] = None

    for i in range(9):
        
        if spots[i]["state"] == "":
            spots[i]["state"] = "X"

            theoryCount += 1
            
            if getGameOverState(spots)["gameOver"]:
                thisOutcome = getGameOverState(spots)["outcome"]
            else:
                # thisPos = MyBestMove(base[i])["pos"]
                thisOutcome = MyBestMove(spots)["outcome"]

            spots[i]["state"] = ""

            if bestMove["outcome"] == None or thisOutcome < bestMove["outcome"]:
                bestMove["outcome"] = thisOutcome
                bestMove["pos"] = i

    return bestMove

def getResultFromCross(team):
    if team == "X":
        return {"gameOver": True, "draw": False, "outcome": -1}
    else:
        return {"gameOver": True, "draw": False, "outcome": 1}    

def getGameOverState(spots):
    for team in ["X", "O"]:
        for x in range(3):
            filledSpots = 0
            for spot in spots:
                if spot["col"] == x:
                    if spot["state"] == team:
                        filledSpots += 1
            if filledSpots == 3:
                return getResultFromCross(team)
        for y in range(3):
            filledSpots = 0
            for spot in spots:
                if spot["row"] == y:
                    if spot["state"] == team:
                        filledSpots += 1
            if filledSpots == 3:
                return getResultFromCross(team)

        filledSpots = 0
        for spot in spots:
            if spot["row"] == spot["col"]:
                if spot["state"] == team:
                    filledSpots += 1
        if filledSpots == 3:
            return getResultFromCross(team)

        filledSpots = 0
        for spot in spots:
            if spot["row"] == 2 - spot["col"]:
                if spot["state"] == team:
                    filledSpots += 1
        if filledSpots == 3:
            return getResultFromCross(team)

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

def getSolutionBranch(spots):
    branch = {}
    branch["response"] = MyBestMove(spots)["pos"]
    spots[branch["response"]]["state"] = "O"
    if not getGameOverState(spots)["gameOver"]:
        for i in range(9):
            if spots[i]["state"] == "":
                spots[i]["state"] = "X"
                if not getGameOverState(spots)["gameOver"]:
                    branch[i] = getSolutionBranch(spots)
                spots[i]["state"] = ""
    spots[branch["response"]]["state"] = ""
    return branch
            

def getSolution(spots):
    solution = {}
    for i in range(9):
        spots[i]["state"] = "X"
        solution[i] = {}
        # solution[i]["response"] = MyBestMove(spots)["pos"]
        solution[i] = getSolutionBranch(spots)
        spots[i]["state"] = ""
    return solution

spots = []
for x in range(3):
    for y in range(3):
        spots.append({"row": x, "col": y, "state": ''})

solution = getSolution(spots)
JsonSolution = json.dumps(solution, default=lambda o: o.__dict__, sort_keys=True, indent=4, separators=(',', ': ') )
print JsonSolution

# print(MyBestMove(spots))
# print "Theory Count for solution: " + str(theoryCount)
# print "Time for solution: " + str(time.time() - before)
