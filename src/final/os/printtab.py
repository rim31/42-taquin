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