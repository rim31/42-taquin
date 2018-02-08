import commands
import os, sys
from math import sqrt
from spiral import spiral, printspiral
from test_res import get_puzzle
from printtab import printtab

class Node:
	def __init__(self, grid):
		self.grid = grid
		# heuristic value
		self.value = 0
		 # search depth of current instance
		self.depth = 0
		self.order = None
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
	for mv in moves:
		nstate = current.grid[:]# Affiche toutes les occurences
		# print nstate
		(nstate[pos + mv], nstate[pos]) = (nstate[pos], nstate[pos + mv])
		expstat.append(nstate)
	children = []
	for elem in expstat:
		child = Node(elem)
		child.value = distance(child.grid, goal)
		child.depth = current.depth + 1
		children.append(Node(elem))
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

def aStar(start, goal):
	openset = set()
	closedset = set()
	current = Node(start)
	current.value = distance(start, goal)
	current.depth = 1
	openset.add(current)
	while openset:
		current = min(openset, key=lambda o:o.depth + o.value)
		print('current')
		print(current.grid)
		print('depth ' + str(current.depth))
		print('value ' + str(current.value))
		print('sum ' + str(current.depth + current.value))
		if current.grid == goal:
			path = []
			while current.parent:
				path.append(current)
				current = current.parent
			path.append(current)
			return path[::-1]
		openset.remove(current)
		closedset.add(current)
		# print(children(current, goal))
		for node in children(current, goal):
			print('---')
			print(node.grid)
			print('---')
			if node in closedset:
				print('closedset')
				continue
			if node in openset:
				print('Correct the depth')
				new_depth = current.depth + 1
				if node.depth > new_depth:
					node.depth = new_depth
					node.parent = current
			else:
				print('else')
				node.depth = current.depth + 1
				node.value = distance(current.grid, goal)
				node.parent = current
				openset.add(node)
		print('openset')
		for elem in openset:
			print(elem.grid)
		print('closedset')
		for elem in closedset:
			print(elem.grid)
		raw_input("Press Enter to continue...")
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