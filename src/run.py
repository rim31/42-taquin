#!/usr/bin/env python

import subprocess
import commands
import os, sys
from math import sqrt
import random
from spiral import spiral, printspiral


class bcolors:
    ONE = '\033[95m'
    TWO = '\033[94m'
    THREE = '\033[92m'
    FOUR = '\033[93m'
    FIVE = '\033[91m'
    SIX = '\033[0m'
    SEVEN = '\033[1m'
    EIGHT = '\033[4m'
    NINE = '\033[96m'
    ENDC = '\033[0m'

def printtab(tab):
    largeur = int(sqrt(len(tab)))
    longueur = int(len(tab))
    # """Print the list in a Matrix Format."""
    for (index, value) in enumerate(tab):
        if value == 0:
            print bcolors.FIVE + ' %s' % value,
        elif value <= 9:
            print bcolors.ONE + ' %s' % value,
        elif value <= 19:
            print bcolors.TWO + '%s' % value,
        elif value <= 29:
            print bcolors.THREE + '%s' % value,
        else:
            print bcolors.FOUR + '%s' % value,
        if index in [x for x in range(largeur - 1, longueur, largeur)]:
            print
    print bcolors.ENDC

def my_resolvable(list):
    nb_inv = 0
    print(list)
    for i in range(0, len(list)):
        for j in range(i + 1, len(list)):
            if(list[j] > list[i] and list[j] and list[i]):
                nb_inv += 1
    if (int(sqrt(len(list))) % 2 == 0):
        if (nb_inv % 2 == 1):
            sys.stdout.write('Unsolvable')
            sys.exit()
    else:
        if (nb_inv % 2 == 0):
            sys.stdout.write('Unsolvable')
            sys.exit()
    print("solvable : " + str(nb_inv))
    return (nb_inv % 2)

def get_puzzle(nb):
    cmd = "python generator.py " + str(nb)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    ## Talk with cmd command i.e. read data from stdout and stderr. Store this info in tuple ##
    ## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached. Wait for process to terminate. The optional input argument should be a string to be sent to the child process, or None, if no data should be sent to the child.
    (output, err) = p.communicate()
    ## Wait for cmd to terminate. Get return returncode ##
    p_status = p.wait()
    # find if solvable
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
    if (my_resolvable(s.split()) == 1):
        exit
    tab = map(int, tab)
    print tab
    # my_resolvable(tab)
    return tab
# distance de manathan
def distance(tab, goal):
    dist = 0
    # taille au carre
    nsize = int(sqrt(len(tab)))
    for node in tab:
        if node != 0:
            gdist = abs(goal.index(node) - tab.index(node))
            jumps = gdist / nsize
            steps = gdist % nsize
            dist += jumps + steps
    return dist

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
def expand(tab):
    expands = {}
    longueur = len(tab)
    for key in range(longueur):
        expands[key] = getvalue(tab, key)
    pos = tab.index(0) #position du 0 'case vide'
    moves = expands[pos]
    # print moves
    expstat = []
    for mv in moves:
        nstate = tab[:]# Affiche toutes les occurences
        # print nstate
        (nstate[pos + mv], nstate[pos]) = (nstate[pos], nstate[pos + mv])
        expstat.append(nstate)
    # print expstat
    return expstat

# """Choose one of the possible states."""     # possibilite de prendre le 1er
def one_of_poss(tab):
    exp_sts = expand(tab)
    rand_st = random.choice(exp_sts)
    return rand_st
    # """Determine the Start State of the Problem."""

def start_state(tab, goal, seed = 1000):
    # goal = range(1, int((len(tab))))
    # goal.append(0)
    start_st = goal[:]
    print "+++++++++++"
    # print start_st
    for sts in range(seed):
        start_st = one_of_poss(start_st)
    return start_st

    # """Check if the Goal Reached or Not."""
def goal_reached(tab, goal):
    # goal = range(1, int((len(tab))))
    # goal.append(0)
    return tab == goal

def heuritstic(tab, goal):
    exp_sts = expand(tab)
    # print expand(tab)
    mdists = []
    for tab in exp_sts:
        mdists.append(distance(tab, goal))
    mdists.sort()
    short_path = mdists[0]
    if mdists.count(short_path) > 1:
        least_paths = [st for st in exp_sts if distance(tab, goal) == short_path]
        return random.choice(least_paths)
        # print (least_paths)
        # return least_paths[0]
    else:
        for tab in exp_sts:
            if distance(tab, goal) == short_path:
                return tab

def resolution(tab, goal):
    while not goal_reached(tab, goal):
        tab = heuritstic(tab, goal)
        printtab(tab)

if __name__ == '__main__':
    sys.stdout.write('N-Puzzle x ')
    if len(sys.argv) == 2:
        print sys.argv[1] #verifier que l'a bien un nobre superieur a 2
    print 12 * '='
    output = get_puzzle(sys.argv[1])
    # printtab(output)
    goal = printspiral(spiral(int(sys.argv[1])))
    print 'The Goal State should be:'
    printtab(goal)

    print 'The Starting State is:'
    # start = start_state(output, goal, 5)
    start = output
    printtab(output)
    # printtab(start)
    print 'Here it Goes:'
    # resolution(start, goal)
    resolution(output, goal)
