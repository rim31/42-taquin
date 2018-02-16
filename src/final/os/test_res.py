import subprocess
import os, sys
from math import sqrt

def my_resolvable(list):
    nb_inv = 0
    print(list)
    for i in range(0, len(list)):
        for j in range(i + 1, len(list)):
            if (list[j] > list[i] and list[j] and list[i]):
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
    # cmd = "python generator.py " + str(nb)
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # (output, err) = p.communicate()
    # p_status = p.wait()
    # count = 0
    # s = ""
    # for line in output.splitlines():
    #     count = count + 1
    #     if (count == 1):
    #         sys.stdout.write(line)
    #     if (count > 2):
    #         s += str(line) + " "
    # tab = []
    # tab = s.split()
    # if (my_resolvable(s.split()) == 1):
    #     exit
    # tab = map(int, tab)
    tab = [1, 3, 4, 6, 7, 8, 0, 5, 2]
    # tab = [7, 0, 14, 5, 2, 4, 6, 12, 8, 15, 13, 11, 9, 10, 3, 1]
    # tab = [10, 0, 9, 4, 5, 8, 1, 12, 13, 3, 2, 15, 11, 14, 6, 7]
    print tab
    return tab
