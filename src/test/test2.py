import commands
import os, sys
from math import sqrt
from spiral import spiral, printspiral
from test_res import get_puzzle
from printtab import printtab

import time

class Node:
	def __init__(self, grid):
		self.grid = grid
		# heuristic value
		self.value = 0
		 # search depth of current instance
		self.depth = 0
		self.order = None
		self.parent = None
		self.adj_matrix = []
		# self.H = 0
		# self.G = 0
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

# list of next possible states
def children(current, goal):
	expands = {}
	longueur = len(current.grid)
	for key in range(longueur):
		expands[key] = getvalue(current.grid, key)
	pos = current.grid.index(0) #position du 0 'case vide'
	moves = expands[pos]
	# print moves
	expstat = []
	children = []
	# print('_____Children_____')
	for mv in moves:
		nstate = current.grid[:]# Affiche toutes les occurences
		# printtab(nstate)
		(nstate[pos + mv], nstate[pos]) = (nstate[pos], nstate[pos + mv])
		expstat.append(nstate)
		child = Node(nstate)
		child.value = distance(child.grid, goal)
		child.depth = current.depth + 1
		children.append(Node(nstate))
		# printtab(child.grid)
	return children

	for mv in moves:
		nstate = current.grid[:]# Affiche toutes les occurences
		# printtab(nstate)
		(nstate[pos + mv], nstate[pos]) = (nstate[pos], nstate[pos + mv])
		expstat.append(nstate)
		child = Node(nstate)
		child.value = distance(child.grid, goal)
		child.depth = current.depth + 1
		children.append(Node(nstate))
		# printtab(child.grid)
	return children

def distance(tab, goal):
    dist = 0
    # taille au carre
    nsize = int(sqrt(len(tab)))
    for node in tab:
        if node != 0:
            gdist = abs(goal.index(node) - tab.index(node))
            jumps = gdist // nsize
            steps = gdist % nsize
            dist += jumps + steps
    mdist = sum(abs((node-1)%nsize - i%nsize) + abs((node-1)//nsize - i//nsize)
    for i, node in enumerate(tab) if node)
    # print mdist
    return mdist

def search_grid_in_set(grid, listset):
	for elem in listset:
		if elem.grid == grid:
			return True
	return False

def search_grid_in_set_and_remove(grid, listset):
	for elem in listset:
		if elem.grid == grid:
			listset.remove(elem)
			return elem
	newNode = Node(grid)
	return newNode

def aStar(start, goal):
	openset = set()
	closedset = set()
	current = Node(start)
	current.value = distance(start, goal)
	current.depth = 1
	openset.add(current)
	while openset:
		current = min(openset, key=lambda o:o.depth + o.value)
		if current.grid == goal:
			path = []
			while current.parent:
				path.append(current)
				current = current.parent
			path.append(current)
			return path[::-1]
		openset.remove(current)
		closedset.add(current)
		for node in children(current, goal):
			if search_grid_in_set(node.grid, closedset):
				continue
			nodeListed = search_grid_in_set_and_remove(node.grid, openset)
			if nodeListed.depth != 0:
				new_depth = current.depth + 1
				if nodeListed.depth > new_depth:
					nodeListed.depth = new_depth
					nodeListed.parent = current
					openset.add(nodeListed)
				else:
					openset.add(nodeListed)
			else:
				node.depth = current.depth + 1
				node.value = distance(node.grid, goal)
				node.parent = current
				openset.add(node)
		# print('openset')
		# for elem in openset:
		# 	print(str(elem.grid) + " " + str(elem.value) + " " + str(elem.depth))
		# print('closedset')
		# for elem in closedset:
		# 	print(elem.grid)
		# raw_input("Press Enter to continue...")
	raise ValueError('No Path Found')


if __name__ == '__main__':
	sys.stdout.write('N-Puzzle x ')
	if len(sys.argv) == 2:
		print sys.argv[1]
	else:
		sys.exit("\nError - You must give the size of the puzzle")
	print 12 * '='
	start = get_puzzle(sys.argv[1])
	goal = printspiral(spiral(int(sys.argv[1])))
	print 'The Goal State should be:'
	printtab(goal)
	print 'The Starting State is:'
	printtab(start)
	print 'Here it Goes:'
	# resolution(start, goal)
	path = aStar(start, goal)
	print('Finish')
	for elem in path:
		printtab(elem.grid)
	# print(path)
