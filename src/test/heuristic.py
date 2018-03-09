from math import sqrt

def manhattan(tab, goal):
	dist = 0
	nsize = int(sqrt(len(tab)))
	for node in tab:
		if node != 0 and goal.index(node) != tab.index(node):
			xGoal = goal.index(node) // nsize
			yGoal =	goal.index(node) % nsize
			xTab = tab.index(node) // nsize
			yTab = tab.index(node) % nsize
			dist += abs(xGoal - xTab) + abs(yGoal - yTab)
	return dist

def euclidean(tab, goal):
	dist = 0
	nsize = int(sqrt(len(tab)))
	node = 0
	for node in tab:
		if node != 0 and goal.index(node) != tab.index(node):
			xGoal = goal.index(node) // nsize
			yGoal =	goal.index(node) % nsize
			xTab = tab.index(node) // nsize
			yTab = tab.index(node) % nsize
			dist += sqrt(pow((xGoal - xTab), 2) + pow((yGoal - yTab), 2))
	return dist

def linearConflict(puzzle, goal):
	puzzleRowSize = int(sqrt(len(puzzle)))
	nbLinearConflict = 0
	for square in puzzle:
		if square != 0 and puzzle.index(square) != goal.index(square):
			goalSquareI = goal.index(square)
			puzzleSquareI = puzzle.index(square)
			if puzzleSquareI // puzzleRowSize == goalSquareI // puzzleRowSize:
				puzzleSquareRow = puzzleSquareI // puzzleRowSize
				for puzzleNextSquareI in range(puzzleRowSize * puzzleSquareRow, puzzleSquareI + (puzzleRowSize * (puzzleSquareRow + 1) - puzzleSquareI) - 1):
					if puzzleNextSquareI != 0 and puzzleNextSquareI != puzzleSquareI and puzzleNextSquareI // puzzleRowSize == goal.index(puzzle[puzzleNextSquareI]) // puzzleRowSize:
						goalNextSquareI = goal.index(puzzle[puzzleNextSquareI])
						if (puzzleNextSquareI > puzzleSquareI and goalNextSquareI < goalSquareI) or (puzzleNextSquareI < puzzleSquareI and goalNextSquareI > goalSquareI):
							nbLinearConflict += 1
			if puzzleSquareI % puzzleRowSize == goalSquareI % puzzleRowSize:
				for puzzleNextSquareI in range(puzzleSquareI, len(puzzle) - 1, puzzleRowSize):
					if puzzleNextSquareI != 0 and puzzleNextSquareI != puzzleSquareI and puzzleNextSquareI % puzzleRowSize == goal.index(puzzle[puzzleNextSquareI]) % puzzleRowSize:
						goalNextSquareI = goal.index(puzzle[puzzleNextSquareI])
						if (puzzleNextSquareI > puzzleSquareI and goalNextSquareI < goalSquareI) or (puzzleNextSquareI < puzzleSquareI and goalNextSquareI > goalSquareI):
							nbLinearConflict += 1
	return manhattan(puzzle, goal) + nbLinearConflict

def tilesOutOfRowAndColumn(puzzle, goal):
	puzzleRowSize = int(sqrt(len(puzzle)))
	nbTilesOutOfRowAndColumn = 0
	for square in puzzle:
		if square != 0 and puzzle.index(square) != goal.index(square):
			goalSquareI = goal.index(square)
			puzzleSquareI = puzzle.index(square)
			if puzzleSquareI // puzzleRowSize != goalSquareI // puzzleRowSize:
				nbTilesOutOfRowAndColumn += 1
			if puzzleSquareI % puzzleRowSize != goalSquareI % puzzleRowSize:
				nbTilesOutOfRowAndColumn += 1
	return nbTilesOutOfRowAndColumn


def misplacedTiles(puzzle, goal):
	nbMisplacedTiles = 0
	for square in puzzle:
		if square != 0 and puzzle.index(square) != goal.index(square):
			nbMisplacedTiles += 1
	return nbMisplacedTiles