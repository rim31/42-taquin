#!/usr/bin/env python

import subprocess
import commands
import sys
from math import sqrt

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
    """Print the list in a Matrix Format."""
    for (index, value) in enumerate(tab):
        print bcolors.ONE + ' %s ' % value,
        if index in [x for x in range(largeur - 1, longueur, largeur)]:
            print
    print bcolors.ENDC
# def resolvable(list):
#     nb_inv = 0
#     print(list)
#     for i in range(0, len(list)):
#         for j in range(i + 1, len(list)):
#             if(list[j] > list[i] and list[j] and list[i]):
#                 nb_inv += 1
#     if (nb_inv % 2 == 1):
#         sys.stdout.write('Un')
#     print("solvable : nb d'inversion " + str(nb_inv))
# //alogo pour savoir sion on a bien un nombre pair de permutation pour savoir si c'est resolvable
def my_resolvable(list):
    nb_inv = 0
    print(list)
    for i in range(0, len(list)):
        for j in range(i + 1, len(list)):
            if(list[j] > list[i] and list[j] and list[i]):
                nb_inv += 1
    if (nb_inv % 2 == 1):
        sys.stdout.write('Un')
    print("solvable : " + str(nb_inv))

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
    my_resolvable(s.split())
    tab = map(int, tab)
    print tab
    # my_resolvable(tab)
    return tab

# distance de manathan
def distance(table):
    dist = 0
    # tableau a changer par rapport a la normal n-puzzle
    goal = range(1, int((len(table))))
    goal.append(0)
    print goal
    printtab(goal)
    # taille du table
    nsize = int(sqrt(len(table)))
    # taille au carre

    for node in table:
        if node != 0:
            gdist = abs(goal.index(node) - table.index(node))
            jumps = gdist / nsize
            steps = gdist % nsize
            dist += jumps + steps
    return dist

# mouvements possibles
def getvalue(tab, key):
    nsize = int(sqrt(len(tab)))
    tsize = int(len(tab))
    values = [1, -1, nsize, -nsize]
    valid = []
    for x in values:
        if 0 <= key + x < tsize:
            if x == 1 and key in range(nsize - 1, tsize, nsize):
                continue
            if x == -1 and key in range(0, tsize, nsize):
                continue
            valid.append(x)
    return valid

# list of next possible state
def expand(tab):
    expands = {}
    for key in range(len(tab)):
        expands[key] = getvalue(tab, key)
    pos = tab.index(0)
    moves = expands[pos]
    expstat = []
    for mv in moves:
        nstate = tab[:]# Affiche toutes les occurences
        print nstate
        (nstate[pos + mv], nstate[pos]) = (nstate[pos], nstate[pos + mv])
        expstat.append(nstate)
    return expstat

# def heuritstic(tab, dist)
#     exp_sts = self.expand(st)
#     mdists = []
#     for st in exp_sts:
#         mdists.append(self.manhattan_distance(st))
#     mdists.sort()
#     short_path = mdists[0]
#     if mdists.count(short_path) > 1:
#         least_paths = [st for st in exp_sts if self.manhattan_distance(st) == short_path]
#         return random.choice(least_paths)
#     else:
#         for st in exp_sts:
#             if self.manhattan_distance(st) == short_path:
#                 return st


if __name__ == '__main__':
    print 'N-Puzzle\n' + 8 * '_'
    # getiing puzzle grid
    output = get_puzzle(3)
    distance(output)
    printtab(output)
    expand(output)
