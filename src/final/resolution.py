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
def mouvement(tab, goal, key):
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
