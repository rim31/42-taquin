#!/usr/bin/env python

import subprocess
import commands
import sys

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
    print s.split()
    my_resolvable(s.split())
    return s.split()

if __name__ == '__main__':
    print 'N-Puzzle'
    print 8 * '_'
    # print 'getting generator'
    # resolvable([1, 2, 3, 4, 5, 6, 8, 7])
    # resolvable([5, 2, 8, 4, 1, 7, 3, 6])
    # resolvable([1, 8, 2, 0, 4, 3, 7, 6, 5])

    # print 'from generator'
    # print 'RESOLVABLE'
    # my_resolvable([5, 7, 3, 8, 0, 6, 1, 4, 2])
    # print 'PAS RESOLVABLE'
    # my_resolvable([7, 1, 8, 3, 5, 6, 0, 2, 4])
    # print 'PAS RESOLVABLE'
    # my_resolvable([ 6, 3, 11, 4, 7, 8, 1, 2, 14, 10, 12, 5, 0, 13, 9, 15])

    # getiing puzzle grid
    output = get_puzzle(4)
