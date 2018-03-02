#!/usr/bin/python3

from math import sqrt

def manhattanDistanceForSolvability(puzzle, goal):
	heuristic = 0
	puzzleRowSize = int(sqrt(len(puzzle)))
	for square in goal:
		goalSquareI = goal.index(square)
		puzzleSquareI = puzzle.index(square)
		heuristic += abs(puzzleSquareI % puzzleRowSize - goalSquareI % puzzleRowSize) + abs(puzzleSquareI // puzzleRowSize - goalSquareI // puzzleRowSize)
	return heuristic

# @profile
def manhattanDistance(puzzle, goal):
	heuristic = 0
	puzzleRowSize = int(sqrt(len(puzzle)))
	for square in goal:
		if square != 0 and puzzle.index(square) != goal.index(square):
			goalSquareI = goal.index(square)
			puzzleSquareI = puzzle.index(square)
			heuristic += abs(goalSquareI % puzzleRowSize - puzzleSquareI % puzzleRowSize) + abs(goalSquareI // puzzleRowSize - puzzleSquareI // puzzleRowSize)
	return heuristic

def linearConflictLoopConditions(puzzleNextSquareI, puzzleSquareI, puzzleRowSize, puzzle, nbLinearConflict, goalSquareI, division, goal):
	
	return nbLinearConflict

# @profile
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
	
	# print(manhattanDistance(puzzle, goal, withZero) + nbLinearConflict)

	return manhattanDistance(puzzle, goal) + nbLinearConflict

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