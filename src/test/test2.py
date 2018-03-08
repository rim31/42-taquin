# import commands
import os, sys
from math import sqrt
from spiral import spiral, printspiral
from test_res import get_puzzle
from printtab import printtab
import heapq


import time

class Node:
	def __init__(self, grid):
		# self.dimension = sqrt(len(grid))
		self.grid = grid
		# heuristic_nb value
		self.value = 0
		 # search depth of current instance
		self.depth = 0
		self.order = None
		self.parent = None
		self.adj_matrix = []
	# def move_cost(self, other):
	#     return 0 if self.value == '.' else 1

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
	# print valid
	return valid

def children(current, goal, heuristic_nb):
	expands = {}
	longueur = len(current[1].grid)
	for key in range(longueur):
		expands[key] = getvalue(current[1].grid, key)
	pos = current[1].grid.index(0)
	moves = expands[pos]
	# print moves
	expstat = []
	children = []
	# print('_____Children_____')
	for mv in moves:
		nstate = current[1].grid[:]# Affiche toutes les occurences
		# printtab(nstate)
		(nstate[pos + mv], nstate[pos]) = (nstate[pos], nstate[pos + mv])
		expstat.append(nstate)
		child = Node(nstate)
		child.value = heuristic(heuristic_nb, child.grid, goal)
		child.depth = current[1].depth + 1
		children.append(Node(nstate))
		# printtab(child.grid)
	return children

	for mv in moves:
		nstate = current[1].grid[:]# Affiche toutes les occurences
		# printtab(nstate)
		(nstate[pos + mv], nstate[pos]) = (nstate[pos], nstate[pos + mv])
		expstat.append(nstate)
		child = Node(nstate)
		child.value = distance(child.grid, goal)
		child.depth = current.depth + 1
		children.append(Node(nstate))
		# printtab(child.grid)
	return children

def manhattan(tab, goal):
	dist = 0
	# taille au carre
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
	# taille au carre
	nsize = int(sqrt(len(tab)))
	node = 0
	for node in tab:
		# print(node)
		if node != 0 and goal.index(node) != tab.index(node):
			xGoal = goal.index(node) // nsize
			yGoal =	goal.index(node) % nsize
			xTab = tab.index(node) // nsize
			yTab = tab.index(node) % nsize
			dist += sqrt(pow((xGoal - xTab), 2) + pow((yGoal - yTab), 2))
	return dist

def linear_conflict(tab, goal):
	size = int(sqrt(len(tab)))
	heuristic_val = manhattan(tab, goal)
	def linear_vertical_conflict():
		linearConflict = 0
		for row in range(size - 1):
			maxVal = -1
			for col in range(size - 1):
				cellValue = tab[(size * col) + row]
				if cellValue != 0 and (cellValue - 1) / size == row:
					if cellValue > maxVal:
						maxVal = cellValue
					else:
						linearConflict += 2
		return linearConflict

	def linear_horizontal_conflict():
		linearConflict = 0
		for row in range(size - 1):
			maxVal = -1
			for col in range(size - 1):
				cellValue = tab[(size * col) + row]
				if cellValue != 0 and cellValue % size == col + 1:
					if cellValue > maxVal:
						maxVal = cellValue
					else:
						linearConflict += 2
		return linearConflict
	
	heuristic_val += linear_vertical_conflict()
	heuristic_val += linear_horizontal_conflict()
	return heuristic_val

def	heuristic(heuristic_nb, tab, goal):
	if (int(heuristic_nb) == 1):
		return manhattan(tab, goal)
	if (int(heuristic_nb) == 2):
		return euclidean(tab, goal)
	if (int(heuristic_nb) == 3):
		return linear_conflict(tab, goal)
	

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
	openset = []
	closedset = set()
	current = Node(start)
	current.value = heuristic(heuristic_nb , start, goal)
	current.depth = 1
	heapq.heappush(openset, (current.value, current))
	while openset:
		current = heapq.heappop(openset)
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
			return path[::-1]
		closedset.add(current)
		for node in children(current, goal, heuristic_nb):
			if search_grid_in_tuple(node.grid, closedset) > 0:
				continue
			nodeDepth = search_grid_in_tuple(node.grid, openset)
			if nodeDepth > 0:
				new_depth = current[1].depth + 1
				if nodeDepth > new_depth:
					nodeListed = search_grid_in_set_and_remove(node.grid, openset)
					nodeListed[1].depth = new_depth
					nodeListed[1].parent = current
					heapq.heappush(openset, (nodeListed[1].value, nodeListed[1]))
			else:
				node.depth = current[1].depth + 1
				node.value = heuristic(heuristic_nb , node.grid, goal)
				node.parent = current
				heapq.heappush(openset, (node.value, node))
		# print('closedset')
		# for elem in closedset:
		# 	print(elem[1].grid)
		# print('openset')
		# for elem in openset:
		# 	print(str(elem[1].grid) + " " + str(elem[1].value) + " " + str(elem[1].depth))
		# raw_input("Press Enter to continue...")
	raise ValueError('No Path Found')


if __name__ == '__main__':
	sys.stdout.write('N-Puzzle x ')
	if len(sys.argv) == 2:
		print(sys.argv[1])
	else:
		sys.exit("\nError - You must give the size of the puzzle")
	print(12 * '=')
	start = get_puzzle(sys.argv[1])
	goal = printspiral(spiral(int(sys.argv[1])))
	print('The Goal State should be:')
	printtab(goal)
	print('The Starting State is:')
	printtab(start)
	heuristic_nb = raw_input("Choose your heuristic_nb: 1 (Manhattan), 2 (Euclidean), 3 ()\n")
	print('Here it Goes:')
	# resolution(start, goal)
	path = aStar(start, goal, heuristic_nb)
	print('Finish')
	for elem in path:
		printtab(elem.grid)
	printtab(start)