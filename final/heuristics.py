#!/usr/bin/python3

from math import sqrt

def manhattanDistance(arr, goal, square):
	dist = 0
	arrRowSize = int(sqrt(len(arr)))
	return abs(goal.index(square) % arrRowSize - arr.index(square) % arrRowSize) + abs(goal.index(square) // arrRowSize - arr.index(square) // arrRowSize)
