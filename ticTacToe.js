angular.module('ticTacToe', []);

function Ctrl($scope, $http) {			
    $scope.endState = function(message) {
		$scope.outcomeText = message;
		$scope.messageVisible= true;
		$scope.gameOver = true;	    
	}
	
	// AI marks a space and checks endgame conditions.
	
	$scope.aiMove = function(playerMove, computerTeam) {
		$scope.spots[$scope.solution[playerMove].response].state = computerTeam;
		$scope.solution = $scope.solution[playerMove];
		if ($scope.won($scope.spots)) {
			$scope.endState("Computer won");
		} else if ($scope.draw($scope.spots)) {
			$scope.endState("Draw");
		}	
	}

	// If game is still continuing, marks the space for player and checks endgame conditions.
	
	$scope.fillIn = function(spot) {
	    if ($scope.team == 'X') {
		    var computerTeam = "O";
		} else {
		    var computerTeam = "X";
	    }
		
	    if (!$scope.gameOver) {
			if (spot.state == "") {
				spot.state = $scope.team;
										
				if ($scope.won($scope.spots)) {
				    // Unused code :)
				    $scope.endState("You won");
				} else if ($scope.draw($scope.spots)) {
				    $scope.endState("Draw");
                } else {						
				    $scope.aiMove(spot.id, computerTeam);
				}
			}
		}
	}
	
	// Checks to see if the game is a draw.
	
	$scope.draw = function(spots) {
	    var filledSpots = 0;
	    for (i = 0; i < spots.length; i++) {
		    if (spots[i]["state"] != '') {
			    filledSpots++;
			}
		}
		
		if (filledSpots == 9) {
		    return true;
		} else {
		    return false;
		}
	}
	
	// Checks to see if the game has been won by either party.
	
	$scope.getLines = function() {
	    return [[0, 1, 2],
		        [3, 4, 5],
				[6, 7, 8],
				[0, 3, 6],
				[1, 4, 7],
				[2, 5, 8],
				[0, 4, 8],
				[2, 4, 6]];
	}
	
	$scope.won = function(spots) {
	    var teams = ["O", "X"];
		var lines = $scope.getLines();
	    for (var team = 0; team < 2; team++) {
		    for (var line = 0; line < lines.length; line++) {
			    var filledSpots = 0;
				for (var pos = 0; pos < lines[line].length; pos++) {
					if (spots[lines[line][pos]].state == teams[team]) {
						filledSpots++;
					}
				}
				if (filledSpots == 3) {
				    return true;
				}				
			}
		}
		return false;		
	};	
	
	$scope.getSolution = function() {
	    if ($scope.team == 'X') {
		    solutionFile = 'TTTOSolution.json';
		} else {
		    solutionFile = 'TTTXSolution.json';
		}
	
	    $http.get(solutionFile).success( function(solutionData) {
		    $scope.solution = solutionData;
			if ($scope.team == "O") {
				$scope.spots[$scope.solution["response"]].state = "X";
			}
			$scope.messageVisible = false;			
			$scope.gameOver = false;
		});
	
	}
	
	// Creates the tic tac toe grid.
	
	$scope.getSpots = function() {
        var spots = [];		
		for (var y = 0; y < 3; y++) {
			for (var x = 0; x < 3; x++) {
				spots.push({row: x, col: y, state: "", id: x+(y*3), classes: []});
				
				var cssClasses = [];
				
				if (y == 0) {
				    cssClasses.push("topSpot");
				} else if (y == 1) {
				    cssClasses.push("midYSpot");
				} else {
				    cssClasses.push("bottomSpot");
				}

				if (x == 0) {
				    cssClasses.push("leftSpot");
				} else if (x == 1) {
				    cssClasses.push("midXSpot");
				} else {
				    cssClasses.push("rightSpot");
				}
				
				spots[spots.length-1].classes = cssClasses;
				
			}
	    }
		return spots;
	
	}
	
	$scope.startGame = function() {
		$scope.endState("Loading...");
		
		$scope.getSolution();
		$scope.spots = $scope.getSpots();		
	}
	
	$scope.team = "X";
	$scope.startGame();
	$scope.gameOver = true;
}

// Function taken from Stack Overflow user ConroyP
// http://stackoverflow.com/questions/122102/most-efficient-way-to-clone-an-object

function clone(obj){
    if(obj == null || typeof(obj) != 'object')
        return obj;

    var temp = obj.constructor(); // changed

    for(var key in obj)
        temp[key] = clone(obj[key]);
    return temp;
}
