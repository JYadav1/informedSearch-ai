import queue

def readGrid(filename):
    #print('In readGrid')
    grid = []
    with open(filename) as f:
        for l in f.readlines():
            grid.append([int(x) for x in l.split()])
    
    f.close()
    #print 'Exiting readGrid'
    return grid
 
def outputGrid(grid, start, goal, path):
    #print('In outputGrid')
    filenameStr = 'path.txt'
 
    # Open filename
    f = open(filenameStr, 'w')
 
    # Mark the start and goal points
    grid[start[0]][start[1]] = 'S'
    grid[goal[0]][goal[1]] = 'G'
 
    # Mark intermediate points with *
    for i, p in enumerate(path):
        if i > 0 and i < len(path)-1:
            grid[p[0]][p[1]] = '*'
 
    # Write the grid to a file
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            
            # Don't add a ' ' at the end of a line
            if c < len(row)-1:
                f.write(str(col)+' ')
            else:
                f.write(str(col))
 
        # Don't add a '\n' after the last line
        if r < len(grid)-1:
            f.write("\n")
 
    # Close file
    f.close()
    #print('Exiting outputGrid')

def main():
    grid = readGrid("grid.txt")
    alg = input("Greedy or A*?: ")
    x_start = int(input("Enter x value for Start: "))
    y_start = int(input("Enter y value for Start: "))
    x_goal = int(input("Enter x value for Goal: "))
    y_goal = int(input("Enter y value for Goal: "))
    start = [x_start,y_start]
    goal = [x_goal,y_goal]
    path, nodesExpanded = informedSearch(grid, start, goal, alg)
    pathCost = 0
    for p in path:
        pathCost += int(grid[p[0]][p[1]])

    outputGrid(grid, start, goal, path)
    print("Nodes Expanded:", len(path))
    print("Path cost:", pathCost)
    print("Path written to file path.txt")
  

class Node:
    def __init__(self, value, parent, h, g):
        self.value = value
        self.parent = parent
        self.h = h
        self.g = g
        self.f = self.h + self.g


    def __lt__(self, other):
        if (self.f < other.f):
            return True
        else:
            return False

def getNeighbors(location, grid):
    adjacent_locations = []
    r = location[0]
    c = location[1]
    
    if (r > 0):
        if (grid[r - 1][c] != 0):
            adjacent_locations.append([r - 1,c])
    
    if (c > 0):
        if (grid[r][c - 1] != 0):
            adjacent_locations.append([r,c - 1])

    if (r < len(grid) - 1):
        if (grid[r + 1][c] != 0):
            adjacent_locations.append([r + 1,c])

    if (c < len(grid[0]) - 1):
        if (grid[r][c + 1] != 0):
            adjacent_locations.append([r,c + 1])
    
    return adjacent_locations

def expandNode(open_list, closed_list, grid, current, goal, alg):
    children = getNeighbors(current.value, grid)
    
    open_list_locations = []
    closed_list_locations = []

    open_list_temp = list(open_list.queue)

    for node in open_list_temp:
        open_list_locations.append(node.value)
    for node in closed_list:
        closed_list_locations.append(node.value)

    for child in children:
        if (child not in open_list_locations and child not in closed_list_locations):
            if (alg == 'Greedy'):
                open_list.put(Node(child, current, h(child, goal), 0))
            else:
                open_list.put(Node(child, current, h(child, goal), current.g + grid[child[0]][child[1]]))

    return open_list

def informedSearch(grid, start, goal, alg):
    
    counter = 0
    current = Node(start, None, h(start, goal), 0)
 
    open_list = queue.PriorityQueue()
    closed_list = []
    open_list.put(current)

    while True:
        if (open_list.empty()):
            return False
    
        current = open_list.get()

        if (current.value == goal):
            path =  setPath(current,[])
            return path, counter

        closed_list.append(current)
        open_list = expandNode(open_list, closed_list, grid, current, goal, alg)
        counter += 1
    
  

def setPath(current,path):
    while (current != None):
        path.append(current.value)
        current = current.parent

    path.reverse()
    return path


def h(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


main()