# import commands
import os, sys
from math import sqrt
from spiral import spiral, printspiral
from test_res import get_puzzle
from printtab import printtab
import heuristic as hf
import heapq

class Node:
	def __init__(self, grid):
		self.grid = grid
		self.value = 0
		self.depth = 0
		self.order = None
		self.parent = None
		self.adj_matrix = []

# mouvements possibles
def getvalue(tab, key):
	taillecarre = int(sqrt(len(tab)))
	longueur = int(len(tab))
	values = [1, -1, taillecarre, -taillecarre]
	valid = []
	for x in values:
		if 0 <= key + x < longueur:
			if x == 1 and key in range(taillecarre - 1, longueur, taillecarre):
				continue
			if x == -1 and key in range(0, longueur, taillecarre):
				continue
			valid.append(x)
	return valid

def children(current, goal, heuristic_nb):
	expands = {}
	longueur = len(current[1].grid)
	for key in range(longueur):
		expands[key] = getvalue(current[1].grid, key)
	pos = current[1].grid.index(0)
	moves = expands[pos]
	expstat = []
	children = []
	for mv in moves:
		nstate = current[1].grid[:]
		(nstate[pos + mv], nstate[pos]) = (nstate[pos], nstate[pos + mv])
		expstat.append(nstate)
		child = Node(nstate)
		child.value = heuristic(heuristic_nb, child.grid, goal)
		child.depth = current[1].depth + 1
		children.append(Node(nstate))
	return children

def	heuristic(heuristic_nb, tab, goal):
	if (int(heuristic_nb) == 1):
		return hf.manhattan(tab, goal)
	if (int(heuristic_nb) == 2):
		return hf.euclidean(tab, goal)
	if (int(heuristic_nb) == 3):
		return hf.linearConflict(tab, goal)
	if (int(heuristic_nb) == 4):
		return hf.tilesOutOfRowAndColumn(tab, goal)
	if (int(heuristic_nb) == 5):
		return hf.misplacedTiles(tab, goal)

def search_grid_in_set(grid, listset):
	for elem in listset:
		if elem.grid == grid:
			return elem.depth
	return 0

def search_grid_in_tuple(grid, listset):
	for elem in listset:
		if elem[1].grid == grid:
			return elem[1].depth
	return 0

def search_grid_in_set_and_remove(grid, listset):
	for elem in listset:
		if elem[1].grid == grid:
			listset.remove(elem)
			return elem
	newNode = Node(grid)
	return newNode

def aStar(start, goal, heuristic_nb):
	openSet = []
	openSetLen = 0
	maxNbStatesInMemoryAtTheSameTime = 0
	closedset = set()
	current = Node(start)
	current.value = heuristic(heuristic_nb , start, goal)
	current.depth = 1
	heapq.heappush(openSet, (current.value, current))
	while openSet:
		current = heapq.heappop(openSet)
		if current[1].grid == goal:
			path = []
			current = current[1]
			print(current.grid)
			print(current.parent)
			while current.parent:
				path.append(current)
				current = current.parent
				current = current[1]
			path.append(current)
			return path[::-1], maxNbStatesInMemoryAtTheSameTime
		closedset.add(current)
		for node in children(current, goal, heuristic_nb):
			if search_grid_in_tuple(node.grid, closedset) > 0:
				continue
			nodeDepth = search_grid_in_tuple(node.grid, openSet)
			if nodeDepth > 0:
				new_depth = current[1].depth + 1
				if nodeDepth > new_depth:
					nodeListed = search_grid_in_set_and_remove(node.grid, openSet)
					nodeListed[1].depth = new_depth
					nodeListed[1].parent = current
					heapq.heappush(openSet, (nodeListed[1].value, nodeListed[1]))
			else:
				node.depth = current[1].depth + 1
				node.value = heuristic(heuristic_nb , node.grid, goal)
				node.parent = current
				heapq.heappush(openSet, (node.value, node))
		openSetLen = len(openSet)
		if openSetLen > maxNbStatesInMemoryAtTheSameTime:
			maxNbStatesInMemoryAtTheSameTime = openSetLen
	raise ValueError('No Path Found')

if __name__ == '__main__':
	sys.stdout.write('N-Puzzle x ')
	if len(sys.argv) == 2 and int(sys.argv[1]) < 71 and int(sys.argv[1]) > 2:
		print(sys.argv[1])
	else:
		sys.exit("\nError - You must give a size of puzzle between 3 and 70")
	print(12 * '=')
	goal = printspiral(spiral(int(sys.argv[1])))
	start = get_puzzle(sys.argv[1], goal)
	print('The Goal State should be:')
	printtab(goal)
	print('The Starting State is:')
	printtab(start)
	heuristic_nb = raw_input("Choose your heuristic_nb: 1 (Manhattan), 2 (Euclidean), 3 (linear conflict), 4, or 5\n")
	if (1 > int(heuristic_nb) and int(heuristic_nb) > 5):
		sys.exit("\nError - You must choose a number between 1 and 5")
	print('Here it Goes:')
	path, maxNbStatesInMemoryAtTheSameTime = aStar(start, goal, heuristic_nb)
	print('Finish')
	for elem in path:
		printtab(elem.grid)
	printtab(start)

# def runNpuzzle(size, heuristic, options, puzzle = None):
# 	npuzzle = Npuzzle(size, heuristic, options, puzzle)
# 	npuzzle.resolve()
# 	npuzzle.printInfos()

# if __name__ == "__main__":
# 	options = []
# 	lenArgv = len(sys.argv)
# 	if lenArgv > 2 and lenArgv < 7:
# 		argI = 1
# 		for arg in sys.argv[1:lenArgv - 2]:
# 			if arg == "-s" or arg == "-u" or arg == "-v":
# 				options.append(arg)
# 			else:
# 				utils.printError(utils.Errors.ARGUMENTS)
# 			argI += 1
# 		if "-s" in options and "-u" in options:
# 			utils.printError(utils.Errors.SOLVABLE_AND_UNSOLVABLE)
# 		file = False
# 		try:
# 			sizeOrFile = int(sys.argv[argI])
# 		except:
# 			try:
# 				sizeOrFile = open(sys.argv[argI], "r")
# 				file = True
# 			except:
# 				utils.printError(utils.Errors.OPEN_FILE, sys.argv[argI])
# 		try:
# 			heuristic_nb = int(sys.argv[argI + 1])
# 		except:
# 			utils.printError(utils.Errors.ARGUMENTS)

# 		if heuristic_nb > 0 and heuristic_nb < 6:
# 			if file:
# 				from Parsing import Parsing
# 				parsing = Parsing(sizeOrFile)
# 				aStar(parsing.puzzle, goal, heuristic_nb)
# 				# runNpuzzle(parsing.puzzleSize, heuristic, options, parsing.puzzle)
# 			elif sizeOrFile > 2 and sizeOrFile < 71

# 				# runNpuzzle(sizeOrFile, heuristic, options)
# 			else:
# 				utils.printError(utils.Errors.ARGUMENTS)
# 		else:
# 			utils.printError(utils.Errors.ARGUMENTS)
# 		if file:
# 			try:
# 				sizeOrFile.close()
# 			except:
# 				utils.printError(utils.Errors.CLOSE_FILE, sys.argv[argI])
# 	else:
# 		utils.printError(utils.Errors.ARGUMENTS)

