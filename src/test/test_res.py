import subprocess
import os, sys
from math import sqrt


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
	print (list)
	for indexGoal in (range(0, len(goal) - 1)):
		for indexPuzzle in (range(0, tab.index(goal[indexGoal]))):
			if (tab[indexPuzzle] not in testDone):
				nb_inv += 1
		testDone.add(goal[indexGoal])
	dist = manhattan(tab, goal)
	# print("nombre d'inversion : ", nb_inv)
	# print("distance manhattan : ", dist)
	if ((dist % 2 == 0 and nb_inv % 2 == 0) or (dist % 2 != 0 and nb_inv != 0)):
		print("SOLVABLE")
		return (1)
	else:
		print("UNSOLVABLE")
		sys.exit()
	return (0)

def get_puzzle(nb, goal):
    cmd = "python generator.py " + str(nb)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    count = 0
    s = ""
    for line in output.splitlines():
        count = count + 1
        if (count == 1):
            sys.stdout.write(line)
        if (count > 2):
            s += str(line) + " "
    tab = []
    tab = s.split()
    tab = map(int, tab)
    if (my_resolvable(s.split(), tab, goal) == 1):
        exit
    # print(tab)
    # tab = [16, 9, 14, 11, 12, 7, 1, 18, 5, 20, 21, 10, 6, 17, 13, 24, 2, 19, 0, 15, 3, 22, 23, 4, 8]
    return tab
