import subprocess
import os
import sys
from math import sqrt
from printtab import printtab

def manhattan(tab, goal):
	dist = 0
	nsize = int(sqrt(len(tab)))
	for node in tab:
		if node != 0 and goal.index(node) != tab.index(node):
			xGoal = goal.index(node) // nsize
			yGoal =	goal.index(node) % nsize
			xTab = tab.index(node) // nsize
			yTab = tab.index(node) % nsize
			dist += abs(xGoal - xTab) + abs(yGoal - yTab)
	return dist

def my_resolvable(list, tab, goal):
	nb_inv = 0
	testDone = set()
	for indexGoal in (range(0, len(goal) - 1)):
		for indexPuzzle in (range(0, tab.index(goal[indexGoal]))):
			if (tab[indexPuzzle] not in testDone):
				nb_inv += 1
		testDone.add(goal[indexGoal])
	dist = manhattan(tab, goal)
	if (dist % 2 == 0 and nb_inv % 2 == 0 or dist % 2 != 0 and nb_inv % 2 != 0):
		print("SOLVABLE")
		return (1)
	else:
		print('The Starting State is:')
		printtab(tab)
		print("UNSOLVABLE")
		sys.exit()
	return (0)

def get_puzzle(nb, goal, s):
	if (s==None):
		cmd = "python generator.py " + str(nb)
	if (s == True):
		cmd = "python generator.py -s " + str(nb)
	if (s == False):
		cmd = "python generator.py -u " + str(nb)
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	p_status = p.wait()
	count = 0
	s = ""
	for line in output.splitlines():
		if count == 0:
			print(line)
		count = count + 1
		if (count > 2):
			s += str(line) + " "
	tab = []
	tab = s.split()
	tab = map(int, tab)

	if (my_resolvable(s.split(), tab, goal) == 1):
		exit
	return tab