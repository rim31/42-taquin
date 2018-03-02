#!/usr/bin/python3

import subprocess
import sys
import utils
from random import randint
import heuristics

class Npuzzle:
	def __init__(self, size):
		self.rowSize = size
		self.totalSize = pow(self.rowSize, 2)
		self.setGoal()
		self.setCustomPuzzle([2, 8, 3, 1, 6, 4, 7, 0, 5])
		# self.generate()
		self.checkIfPuzzleIsSolvable()
		self.calculateHeuristicDistance()
		# print("Goal :")
		# utils.printArray(self.goal)
		# print("Puzzle :")
		# utils.printArray(self.puzzle)
		# if (self.isSolvable == self.isSolvable2):
		# 	print("\033[92mYES")
		# else:
		# 	print("\033[91mNO")
		if not self.isSolvable:
			print("This puzzle is unsolvable")
			exit()
		print("This puzzle is solvable\n" + "Estimated heuristic distance : " + str(self.heuristicDistance))


	def generate(self):
		p = subprocess.Popen("python generator.py " + str(self.rowSize), stdout=subprocess.PIPE, shell=True)
		## Talk with cmd command i.e. read data from stdout and stderr. Store this info in tuple ##
		## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached. Wait for process to terminate. The optional input argument should be a string to be sent to the child process, or None, if no data should be sent to the child.
		(output, err) = p.communicate()
		output = output.decode("utf-8")
		## Wait for cmd to terminate. Get return returncode ##
		p_status = p.wait()

		count = 0
		s = ""
		for line in output.splitlines():
			count += 1
			if count == 1:
				self.isSolvable2 = line == "# This puzzle is solvable"
				print(line)
			if (count > 2):
				s += str(line) + " "
		self.puzzle = [int(x) for x in s.split()]
		# print(self.puzzle)


	def checkIfPuzzleIsSolvable(self):
		nbInv = 0
		alreadyTestedValues = set()
		for iGoal in range(0, len(self.goal) - 1):
			# print(iGoal, end=" : ")
			for iPuzzle in range(0, self.puzzle.index(self.goal[iGoal])):
				if self.puzzle[iPuzzle] not in alreadyTestedValues:
					# print(self.puzzle[iPuzzle], end=" ")
					nbInv += 1
			# print()
			alreadyTestedValues.add(self.goal[iGoal])

		print("nb inv : " + str(nbInv))
		manDistance = heuristics.manhattanDistance(self.puzzle, self.goal, 0)
		self.isSolvable = manDistance % 2 == 0 and nbInv % 2 == 0 or manDistance % 2 != 0 and nbInv != 0


	def setGoal(self):
		self.goal = [[0] * self.rowSize for i in range(self.rowSize)]
		dx, dy = [0, 1, 0, -1], [1, 0, -1, 0]
		x, y, c = 0, -1, 1
		for i in range(self.rowSize + self.rowSize - 1):
			for j in range((self.rowSize + self.rowSize - i) // 2):
				x += dx[i % 4]
				y += dy[i % 4]
				self.goal[x][y] = c
				c += 1
		halfRowSize = self.rowSize // 2
		self.goal[halfRowSize][halfRowSize - (1 if self.rowSize % 2 == 0 else 0)] = 0		# a if condition else b -> ternaire

		s = ""
		for (i, value) in enumerate(self.goal):
			for (i2, value2) in enumerate(value):
				s += str(value2) + " "
		self.goal = [int(x) for x in s.split()]


	def setCustomPuzzle(self, customPuzzle):
		self.puzzle = customPuzzle

	def calculateHeuristicDistance(self):
		self.heuristicDistance = 0
		for square in self.goal:
			if square != 0:
				self.heuristicDistance += heuristics.manhattanDistance(self.puzzle, self.goal, square)

	# def resolve(self):
	# 	closedSet = dict()

	# 	openSet = dict()
	# 	openSet[0] = self.puzzle

	# 	cameFrom = dict()
	# 	gScore = {0}
	# 	fScore = dict()
	# 	fScore[0] = self.heuristicDistance

	# 	while openSet is not None:
	# 		current = fScore.keys()[min(fScore)]
	# 		# current = openSet[fScore.keys()[min(fScore)]]
	# 		if current == self.goal:
	# 			return reconstructPath(cameFrom, current)

	# 		openSet.remove(current)
	# 		closedSet.add(current)

	# 		for neighbor in current:
	# 			if neighbor in closedSet:
	# 				continue

	# 			if neighbor not in openSet:
	# 				openSet.add(neighbor)

	# 			tentative_gScore = gScore[current] + heuristics.manhattanDistance(current, neighbor)
	# 			if tentative_gScore >= gScore[neighbor]:
	# 				continue

	# 			cameFrom[neighbor] = current
	# 			gScore[neighbor] = tentative_gScore
	# 			fscore[neighbor] = gScore[neighbor] + heuristics.manhattanDistance(neighbor, goal)
	# 	return None


	# def reconstructPath(cameFrom, current):
	# 	totalPath = [current]
	# 	while current in cameFrom.keys():
	# 		current = cameFrom[current]
	# 		totalPath.append(current)
	# 	return totalPath
