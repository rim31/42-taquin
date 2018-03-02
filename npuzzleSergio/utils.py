#!/usr/bin/python

import math
from enum import Enum

class Errors(Enum):
	ARGUMENTS = 0
	SOLVABLE_AND_UNSOLVABLE = 1
	OPEN_FILE = 2
	CLOSE_FILE = 3
	FORMAT_FILE = 4

def printError(err, file = None):
	print("\033[91m", end="")
	if err == Errors.ARGUMENTS:
		print("\033[0musage : python3 run.py [options] [2 < size < 101 or input file] [heuristic function]\n")
		print("option :\n\t-s\tsolvable puzzle\n\t-u\tunsolvable puzzle\n\t-v\tverbose\n")
		print("heuristic function :\n\t0\tmisplaced tiles\n\t1\ttiles out of row and column\n\t2\tmanhattan distance\n\t3\tlinear conflict")
	elif err == Errors.SOLVABLE_AND_UNSOLVABLE:
		print("A puzzle can't be both solvable and unsolvable")
	elif err == Errors.OPEN_FILE:
		print("Can't open file " + file)
	elif err == Errors.CLOSE_FILE:
		print("Can't close file " + file)
	elif err == Errors.FORMAT_FILE:
		print("\033[0mFile format :\n\tcomments start with a '#' and can be at the start or at the end of a line\n\tpuzzle size in integer\n\tpuzzle squares in integers separated with spaces and newlines, squares must be present only once and be between 0 and puzzle size^2 - 1")
	print("\033[0m", end="")
	exit()

def printArray(arr, withVerbose = False):
	arrLen = len(arr)
	row = int(math.sqrt(arrLen))
	columns = arrLen
	for (i, value) in enumerate(arr):
		if value == 0:
			print("\033[92m", end="")
			if withVerbose:
				print('{:>3}'.format("■"), end=" ")
			else:
				print('{:>3}'.format(value), end=" ")
		else:
			print('{:>3}'.format(value), end=" ")
		if value == 0:
			print("\033[0m", end="")
		if i in [x for x in range(row - 1, columns, row)]:
			print("\n")
	print("\n")