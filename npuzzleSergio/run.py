#!/usr/bin/python3

import sys
from Npuzzle import Npuzzle
from Npuzzle import heuristicFunctions
import utils

def runNpuzzle(size, heuristic, options, puzzle = None):
	npuzzle = Npuzzle(size, heuristic, options, puzzle)
	npuzzle.resolve()
	npuzzle.printInfos()

if __name__ == "__main__":

	options = []
	lenArgv = len(sys.argv)
	if lenArgv > 2 and lenArgv < 7:
		argI = 1
		for arg in sys.argv[1:lenArgv - 2]:
			if arg == "-s" or arg == "-u" or arg == "-v":
				options.append(arg)
			else:
				utils.printError(utils.Errors.ARGUMENTS)
			argI += 1

		if "-s" in options and "-u" in options:
			utils.printError(utils.Errors.SOLVABLE_AND_UNSOLVABLE)

		file = False
		try:
			sizeOrFile = int(sys.argv[argI])
		except:
			try:
				sizeOrFile = open(sys.argv[argI], "r")
				file = True
			except:
				utils.printError(utils.Errors.OPEN_FILE, sys.argv[argI])
		try:
			heuristic = int(sys.argv[argI + 1])
		except:
			utils.printError(utils.Errors.ARGUMENTS)

		if heuristic > -1 and heuristic < len(heuristicFunctions):
			if file:
				from Parsing import Parsing
				parsing = Parsing(sizeOrFile)
				runNpuzzle(parsing.puzzleSize, heuristic, options, parsing.puzzle)
			elif sizeOrFile > 2 and sizeOrFile < 101:
				runNpuzzle(sizeOrFile, heuristic, options)
			else:
				utils.printError(utils.Errors.ARGUMENTS)
		else:
			utils.printError(utils.Errors.ARGUMENTS)
		
		if file:
			try:
				sizeOrFile.close()
			except:
				utils.printError(utils.Errors.CLOSE_FILE, sys.argv[argI])
	else:
		utils.printError(utils.Errors.ARGUMENTS)