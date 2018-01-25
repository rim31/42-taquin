def spiral(n):
    dx,dy = 1,0            # Starting increments
    x,y = 0,0              # Starting location
    myarray = [[None]* n for j in range(n)]
    for i in xrange(n**2):
        if (i + 1 == n**2):
            myarray[x][y] = 0
        else:
            myarray[x][y] = i + 1
        nx,ny = x+dx, y+dy
        if 0<=nx<n and 0<=ny<n and myarray[nx][ny] == None:
            x,y = nx,ny
        else:
            dx,dy = -dy,dx
            x,y = x+dx, y+dy
    return myarray

def printspiral(myarray):
    n = range(len(myarray))
    goal = []
    for y in n:
        for x in n:
            goal.append(myarray[x][y])
            print "%2i" % myarray[x][y],
        print
    print goal
    return goal


# printspiral(spiral(3))
