import os, sys
from math import sqrt
from spiral import spiral, printspiral
from test_res import get_puzzle, my_resolvable
from printtab import printtab, writtetab
import heuristic as hf
import heapq
from parsing import Parsing
import argparse

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
	maxNbStatesInOpenAtTheSameTime = 0
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
			while current.parent:
				path.append(current)
				current = current.parent
				current = current[1]
			path.append(current)
			return path[::-1], maxNbStatesInMemoryAtTheSameTime, maxNbStatesInOpenAtTheSameTime
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
		openSetTot = len(openSet) + len(closedset)
		if openSetLen > maxNbStatesInOpenAtTheSameTime:
			maxNbStatesInOpenAtTheSameTime = openSetLen
		if openSetTot > maxNbStatesInMemoryAtTheSameTime:
			maxNbStatesInMemoryAtTheSameTime = openSetTot
	raise ValueError('No Path Found')

def parse_argument(arg):
	parser = argparse.ArgumentParser()
	group1 = parser.add_mutually_exclusive_group()
	group1.add_argument('-l', '--length', default='3', type=int, help='Choose the size of your puzzle between 3 and 70')
	group1.add_argument('-f', '--file', type=str, help='Name of your file, if this option is selected, ignore: -s/u')
	group2 = parser.add_mutually_exclusive_group()
	group2.add_argument('-s', '--solvable', action='store_true', help='Generate only solvable puzzle')
	group2.add_argument('-u', '--unsolvable', action='store_false', help='Generate only unsolvable puzzle')
	parser.add_argument('-a', '--anim', action='store_true' , help='Launch an animation of the resolution of the puzzle')
	return parser.parse_args(arg)

if __name__ == '__main__':
	arg = parse_argument(sys.argv[1:])

	if (arg.file):
		try:
			fd = open(arg.file, "r")
			parsing = Parsing(fd)
		except:
			sys.exit("Error - Openning error")
		start = parsing.puzzle
		goal = printspiral(spiral(int(sqrt(len(start)))))
		if (my_resolvable(parsing, start, goal) == 1):
			exit

	else:
		if arg.length < 71 and arg.length > 2:
			goal = printspiral(spiral(arg.length))
			solvable = None
			if (arg.solvable == True):
				solvable = True
			elif (arg.unsolvable == False):
				solvable = False
			start = get_puzzle(arg.length, goal, solvable)
		else:
			sys.exit('Wrong size')

	print('The Goal State should be:')
	printtab(goal)
	print('The Starting State is:')
	printtab(start)
	heuristic_nb = raw_input("Choose your heuristic_nb: 1 (Manhattan), 2 (Euclidean), 3 (linear conflict), 4 (tiles out of row and column), or 5 (misplaced tiles)\n")
	try:
		heuristic_nb = int(heuristic_nb)
	except:
		sys.exit("Error - wrong input")
	if (1 > int(heuristic_nb) or int(heuristic_nb) > 5):
		sys.exit("Error - You must choose a number between 1 and 5")
	print('Here it Goes: ...')
	path, maxInMemory, maxInOpen = aStar(start, goal, heuristic_nb)

	if (arg.anim):
		for elem in path:
			for i in range(1, 8000000):
				pass
			os.system('clear')
			printtab(elem.grid)
	else:
		for elem in path:
			printtab(elem.grid)
	
	print("Complexity in size: " + str(maxInMemory))
	print("Complexity in time: " + str(maxInOpen))
	print("Number of step: " + str(len(path)))