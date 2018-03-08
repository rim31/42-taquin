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
    # raw_input("Press Enter to continue...")
    # if (int(sqrt(len(list))) % 2 == 0):
    #     if (nb_inv % 2 == 1):
    #         sys.stdout.write('Unsolvable')
    #         sys.exit()
    # else:
    #     if (nb_inv % 2 == 0):
    #         sys.stdout.write('Unsolvable')
    #         sys.exit()
    # print("solvable : " + str(nb_inv))
    return (nb_inv % 2)

def get_puzzle(nb):
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
    if (my_resolvable(s.split()) == 1):
        exit
    tab = map(int, tab)
    print(tab)
    # tab = [16, 9, 14, 11, 12, 7, 1, 18, 5, 20, 21, 10, 6, 17, 13, 24, 2, 19, 0, 15, 3, 22, 23, 4, 8]
    # tab = [15, 7, 11, 4, 0, 2, 12, 14, 1, 10, 3, 8, 13, 9, 5, 6]
    # tab = [4, 8, 13, 9, 11, 7, 0, 15, 1, 12, 6, 2, 10, 14, 5, 3]
    return tab