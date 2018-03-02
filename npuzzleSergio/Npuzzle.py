#!/usr/bin/python3

import subprocess
import utils
import os
import heuristics

heuristicFunctions = [heuristics.misplacedTiles, heuristics.tilesOutOfRowAndColumn, heuristics.manhattanDistance, heuristics.linearConflict]

class Npuzzle:

	UP = 0
	DOWN = 1
	LEFT = 2
	RIGHT = 3

	def __init__(self, size, heuristic, options, customPuzzle = None):
		self.options = options
		self.chosenHeuristic = heuristic
		self.rowSize = size
		self.totalSize = self.rowSize * self.rowSize
		# self.goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
		self.setGoal()
		# self.setCustomPuzzle([8, 1, 0, 7, 5, 4, 2, 3, 6])
		# self.setCustomPuzzle([5, 6, 4, 1, 2, 3, 7, 8, 0])
		# self.setCustomPuzzle([6, 7, 4, 1, 3, 5, 0, 2, 8])
		# self.setCustomPuzzle([15, 4, 9, 13, 0, 7, 8, 1, 3, 5, 11, 6, 10, 2, 14, 12])
		# self.setCustomPuzzle([33, 34, 6, 16, 30, 14, 8, 22, 18, 21, 20, 5, 13, 19, 17, 11, 12, 28, 4, 27, 0, 23, 3, 35, 2, 31, 9, 7, 29, 25, 26, 15, 1, 10, 32, 24])
		# self.setCustomPuzzle([23, 19, 16, 4, 14, 10, 12, 22, 0, 20, 15, 2, 7, 1, 3, 24, 17, 5, 21, 13, 6, 18, 8, 11, 9])
		# self.setCustomPuzzle([9, 3, 12, 19, 20, 13, 21, 23, 18, 14, 16, 8, 4, 7, 22, 2, 1, 15, 24, 17, 11, 6, 0, 5, 10])
		# self.setCustomPuzzle([1, 8, 3, 5, 0, 2, 7, 6, 4])
		# customPuzzle = [24, 44, 4, 32, 7, 43, 12, 1, 47, 2, 13, 38, 36, 48, 3, 27, 37, 22, 45, 42, 39, 35, 14, 21, 0, 19, 17, 25, 10, 28, 31, 29, 33, 23, 18, 40, 15, 30, 16, 41, 11, 5, 9, 34, 46, 20, 26, 6, 8]
		# self.setCustomPuzzle([0, 12, 2, 4, 8, 16, 15, 23, 20, 10, 5, 6, 24, 13, 9, 21, 3, 7, 1, 19, 14, 17, 11, 18, 22])
		if customPuzzle is None:
			self.generate()
		else:
			self.puzzle = customPuzzle
		utils.printArray(self.puzzle)
		self.checkIfPuzzleIsSolvable()
		self.zeroSquare = self.puzzle.index(0)
		self.chosenHeuristicDistance = self.calculateHeuristicDistance(self.puzzle)
		# if (self.isSolvable == self.isSolvable2):
		# 	print("\033[92mYES")
		# else:
		# 	print("\033[91mNO")
		if not self.isSolvable:
			print("GOAL")
			utils.printArray(self.goal)
			print("PUZZLE")
			utils.printArray(self.puzzle)
			print("This puzzle is unsolvable")
			exit()
		# print("This puzzle is solvable\n" + "Estimated heuristic distance : " + str(self.chosenHeuristicDistance))


	def generate(self):
		optionsLine = ""
		if "-s" in self.options:
			optionsLine += " -s"
		if "-u" in self.options:
			optionsLine += " -u"
		p = subprocess.Popen("python generator.py" + optionsLine + " " + str(self.rowSize), stdout=subprocess.PIPE, shell=True)
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
			# if count == 1:
			# 	self.isSolvable2 = line == "# This puzzle is solvable"
			# 	print(line)
			if (count > 2):
				s += str(line) + " "
		self.puzzle = [int(x) for x in s.split()]
		# print(self.puzzle)


	# @profile
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

		# print("nb inv : " + str(nbInv))

		heuristicDistance = heuristics.manhattanDistanceForSolvability(self.puzzle, self.goal)
		self.isSolvable = heuristicDistance % 2 == 0 and nbInv % 2 == 0 or heuristicDistance % 2 != 0 and nbInv != 0


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
	

	# @profile
	def calculateHeuristicDistance(self, puzzle):
		return heuristicFunctions[self.chosenHeuristic](puzzle, self.goal)
	
	# @profile
	def moveSquare(self, direction):
		tmpPuzzle = self.currentPuzzle.copy()
		if direction == self.UP and self.zeroSquare - self.rowSize > -1:
			tmpPuzzle[self.zeroSquare], tmpPuzzle[self.zeroSquare - self.rowSize] = tmpPuzzle[self.zeroSquare - self.rowSize], tmpPuzzle[self.zeroSquare]
		elif direction == self.DOWN and self.zeroSquare + self.rowSize < self.totalSize:
			tmpPuzzle[self.zeroSquare], tmpPuzzle[self.zeroSquare + self.rowSize] = tmpPuzzle[self.zeroSquare + self.rowSize], tmpPuzzle[self.zeroSquare]
		elif direction == self.LEFT and (self.zeroSquare - 1) // self.rowSize == self.zeroSquare // self.rowSize :
			tmpPuzzle[self.zeroSquare], tmpPuzzle[self.zeroSquare - 1] = tmpPuzzle[self.zeroSquare - 1], tmpPuzzle[self.zeroSquare]
		elif direction == self.RIGHT and (self.zeroSquare + 1) // self.rowSize == self.zeroSquare // self.rowSize:
			tmpPuzzle[self.zeroSquare], tmpPuzzle[self.zeroSquare + 1] = tmpPuzzle[self.zeroSquare + 1], tmpPuzzle[self.zeroSquare]
		else:
			return None
		return tmpPuzzle

	# @profile
	def resolve(self):
		from operator import itemgetter
		tupleF = tuple
		listF = list
		puzzleTuple = tupleF(self.puzzle)
		closedSet = set()
		openSet = {puzzleTuple: self.chosenHeuristicDistance}
		cameFrom = {}
		gScore = {puzzleTuple: 0}
		self.nbStatesOpenSet = 0
		self.maxNbStatesInMemoryAtTheSameTime = 0
		# self.currentPuzzle = self.puzzle

		while openSet is not None:

			b = dict(map(lambda item: (item[1], item[0]), openSet.items()))
			self.currentPuzzle = listF(b[min(b.keys())])

			self.zeroSquare = self.currentPuzzle.index(0)

			if self.currentPuzzle == self.goal:
				totalPath = [self.currentPuzzle]
				currentTuple = tupleF(self.currentPuzzle)
				while currentTuple in cameFrom.keys():
					currentTuple = tupleF(cameFrom[currentTuple])
					totalPath.append(listF(currentTuple))
				self.totalPath = totalPath
				return

			if tupleF(self.currentPuzzle) in openSet.keys():
				del openSet[tupleF(self.currentPuzzle)]
			closedSet.add(tupleF(self.currentPuzzle))

			possiblePuzzles = [self.moveSquare(self.UP), self.moveSquare(self.DOWN), self.moveSquare(self.LEFT), self.moveSquare(self.RIGHT)]

			for puzzle in possiblePuzzles:
				if puzzle is None or tupleF(puzzle) in closedSet:
					continue
				
				possiblePuzzleTuple = tupleF(puzzle)

				tentative_gScore = 1
				if possiblePuzzleTuple in gScore.keys():
					tentative_gScore += gScore[tupleF(self.currentPuzzle)]
					if tentative_gScore >= gScore[possiblePuzzleTuple]:
						continue

				cameFrom[possiblePuzzleTuple] = self.currentPuzzle
				gScore[possiblePuzzleTuple] = tentative_gScore

				if possiblePuzzleTuple not in openSet.keys():
					openSet[possiblePuzzleTuple] = tentative_gScore + self.calculateHeuristicDistance(puzzle)
					self.nbStatesOpenSet += 1
			
			openSetLen = len(openSet)
			if openSetLen > self.maxNbStatesInMemoryAtTheSameTime:
				self.maxNbStatesInMemoryAtTheSameTime = openSetLen
	
	def printInfos(self):
		verbose = False
		if "-v" in self.options:
			verbose = True
		for puzzle in reversed(self.totalPath):
			if verbose:
				for i in range(1, 8000000):
					pass
				os.system('clear')
			utils.printArray(puzzle, verbose)
		print("Complexity time : " + str(self.nbStatesOpenSet))
		print("Complexity size : " + str(self.maxNbStatesInMemoryAtTheSameTime))
		print("Number of moves : " + str(len(self.totalPath)))