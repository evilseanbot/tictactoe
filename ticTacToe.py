import copy
import time
import json

theoryCount = 0
before = time.time()

# This generates an ideal move to make given the current spots.
# forEnemy is a boolean determines whether the AI is making a move for itself, or its enemy (theoretical human player playing with the same intelligence)
# makeBest Move returns an object containing the best outcome if it plays perfectly(1 for win, 0 for draw, -1 for lose) and the position (pos) (index on the spot array) of its next move.

def makeBestMove(spots, lines, forEnemy):
    global theoryCount
    bestMove = {}
    bestMove["outcome"] = None
    bestMove["pos"] = None

    for i in range(9):
        if spots[i] == "":

            # The enemy's (Or theoretical ideal human opponent) marks are listed as "E", and the AIs marks are listed as "A"
            if forEnemy:
                spots[i] = "E"
            else:
                spots[i] = "A"
                
            # This keeps a running total of how many theoretical moves the AI looks into, used for testing purposes.
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

# Returns the results from a line being filled out.
# -1 is a loss.
# 1 is a win.

def getResultFromCross(team):
    if team == "E":
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
    for team in ["E", "A"]:
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

# Prints out the current results in a grid (Used for testing purposes)

def printToes(spots):
    for y in range(3):
        for x in range(3):
            if spots[x + (y*3)] == "E":
                print "E",
            elif spots[x + (y*3)] == "A":
                print "A",
            else:
                print "_",
        print ""
    print "="

# Creates a "Solution Branch", An ideal  response as well as a list of possible opponent moves that could follow the response, which will have 

def getSolutionBranch(spots, lines):
    branch = {}
    branch["response"] = makeBestMove(spots, lines, False)["pos"]
    spots[branch["response"]] = "A"
    if not getGameOverState(spots, lines)["gameOver"]:
        for i in range(9):
            if spots[i] == "":
                spots[i] = "E"
                if not getGameOverState(spots, lines)["gameOver"]:
                    branch[i] = getSolutionBranch(spots, lines)
                spots[i] = ""
    spots[branch["response"]] = ""
    return branch

# Creates a starting solution base for players who are starting second, which does not have a starting "Response" assumed in getSolution Branch.

def getSolutionForO(spots, lines):
    solution = {}
    for i in range(9):
        spots[i] = "E"
        solution[i] = {}
        solution[i] = getSolutionBranch(spots, lines)
        spots[i] = ""
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

XSolution = prettyJson(getSolutionBranch(spots, lines))

fo = open("TTTXSolution.json", "wb")
fo.write(XSolution);
fo.close()
