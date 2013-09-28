import copy
import time
import json

theoryCount = 0
before = time.time()

def makeBestMove(spots, lines, forEnemy):
    global theoryCount
    bestMove = {}
    bestMove["outcome"] = None
    bestMove["pos"] = None

    for i in range(9):
        if spots[i] == "":
            
            if forEnemy:
                spots[i] = "X"
            else:
                spots[i] = "O"

            theoryCount += 1

            if getGameOverState(spots, lines)["gameOver"]:
                thisOutcome = getGameOverState(spots, lines)["outcome"]
            else:
                thisOutcome = makeBestMove(spots, lines, not forEnemy)["outcome"]

            spots[i] = ""

            if bestMove["outcome"] == None or (not forEnemy and thisOutcome > bestMove["outcome"]) or (forEnemy and thisOutcome < bestMove["outcome"]):
                bestMove["outcome"] = thisOutcome
                bestMove["pos"] = i
    return bestMove

def getResultFromCross(team):
    if team == "X":
        return {"gameOver": True, "outcome": -1}
    else:
        return {"gameOver": True, "outcome": 1}    

def getLines():
    lines = []
    # Horizontal lines
    for rowOffset in range(3):
        lines.append(range((rowOffset*3), (rowOffset*3)+3, 1))

    # Vertical lines
    for colOffset in range(3):
        lines.append(range(colOffset, colOffset+7, 3))

    # Diagnol lines
    lines.append(range(0, 9, 4))
    lines.append(range(2, 7, 2))

    return lines

def getGameOverState(spots, lines):
    # First checks to see if someone has won:
    for team in ["X", "O"]:
        for line in getLines():
            filledSpots = 0
            for pos in line:
                if spots[pos] == team:
                    filledSpots += 1
            if filledSpots == 3:
                return getResultFromCross(team)
            
    # If no one has won, checks to see if the board is filled, and thus the game is over.
    noBlankSpotsLeft = True
    for i in range(9):
        if spots[i] == "":
           noBlankSpotsLeft = False
    if noBlankSpotsLeft:
        return {"gameOver": True, "outcome": 0}
    else:
        return {"gameOver": False, "outcome": None}


def printToes(spots):
    for y in range(3):
        for x in range(3):
            if spots[x + (y*3)] == "X":
                print "X",
            elif spots[x + (y*3)] == "O":
                print "O",
            else:
                print "_",
        print ""
    print "="

def getSolutionBranch(spots, lines):
    branch = {}
    branch["response"] = makeBestMove(spots, lines, False)["pos"]
    spots[branch["response"]] = "O"
    if not getGameOverState(spots, lines)["gameOver"]:
        for i in range(9):
            if spots[i] == "":
                spots[i] = "X"
                if not getGameOverState(spots, lines)["gameOver"]:
                    branch[i] = getSolutionBranch(spots, lines)
                spots[i] = ""
    spots[branch["response"]] = ""
    return branch
            

def getSolutionForO(spots, lines):
    solution = {}
    for i in range(9):
        spots[i] = "X"
        solution[i] = {}
        solution[i] = getSolutionBranch(spots, lines)
        spots[i] = ""
    return solution

def getSolutionForX(spots, lines):
    solution = {}
    solution = getSolutionBranch(spots, lines)
    return solution

def prettyJson(string):
    return json.dumps(string, default=lambda o: o.__dict__, sort_keys=True, indent=4, separators=(',', ': '))


lines = getLines()
spots = []
for i in range(9):
    spots.append('')

OSolution = prettyJson(getSolutionForO(spots, lines))

fo = open("TTTOSolution.json", "wb")
fo.write(OSolution);
fo.close()

XSolution = prettyJson(getSolutionForX(spots, lines))

fo = open("TTTXSolution.json", "wb")
fo.write(XSolution);
fo.close()

# print(MyBestMove(spots))
# print "Theory Count for solution: " + str(theoryCount)
# print "Time for solution: " + str(time.time() - before)
