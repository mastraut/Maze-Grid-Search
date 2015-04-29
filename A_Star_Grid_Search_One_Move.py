'''
Problem Statement:

In this version of "Bot saves princess", Princess Peach and bot's 
position are randomly set. Can you save the princess?

Task

Complete the function nextMove which takes in 4 parameters - an 
integer N, integers r and c indicating the row & column position of the
 bot and the character array grid - and outputs the next move the bot 
 makes to rescue the princess.

Input Format

The first line of the input is N (<100), the size of the board (NxN). 
The second line of the input contains two space separated integers, 
which is the position of the bot.

Grid is indexed using Matrix Convention

The position of the princess is indicated by the character 'p' and the 
position of the bot is indicated by the character 'm' and each cell is 
denoted by '-' (ascii value: 45).

Output Format

Output only the next move you take to rescue the princess. Valid moves 
are LEFT, RIGHT, UP or DOWN

Sample Input

5
2 3
-----
-----
p--m-
-----
-----
Sample Output

LEFT
Resultant State

-----
-----
p-m--
-----
-----
Explanation

As you can see, bot is one step closer to the princess.
'''

####################
#! A* Grid Search !#
####################

import heapq

def displayPathtoPrincess(path):
    #print all the moves here
    print path[0]

class Cell(object):
    def __init__(self, x, y, reachable):
        """
        Initialize new cell

        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

class AStar(object):
    def __init__(self):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = 100
        self.grid_width = 1000

    def init_grid(self,xS,yS, grid):
        self.grid_height = len(grid)
        self.grid_width = len(grid[0])
        Px = 0
        Py = 0
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                self.cells.append(Cell(x, y, True))
                if grid[x][y] == 'p':
                    Px = x
                    Py = y
        self.start = self.get_cell(xS, yS)
        self.end = self.get_cell(Px,Py)

    def get_heuristic(self, cell):
        """
        Compute the heuristic value H for a cell: distance between
        this cell and the ending cell multiply by 10.

        @param cell
        @returns heuristic value H
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        """
        Returns a cell from the cells list

        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        """
        Returns adjacent cells to a cell. Clockwise starting
        from the one on the right.

        @param cell get adjacent cells for this cell
        @returns adjacent cells list 
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def display_path(self):
        cell = self.end
        path = []
        while cell.parent is not self.start:
            vert = cell.parent.x - cell.x 
            horz = cell.parent.y - cell.y
            if horz > 0:
                path.append('LEFT')
            elif horz < 0:    
                path.append('RIGHT')
            if vert > 0:
                path.append('UP')
            elif vert < 0:
                path.append('DOWN')
            cell = cell.parent
        vert =  self.start.x - cell.x 
        horz = self.start.y - cell.y
        if horz > 0:
            path.append('LEFT')
        elif horz < 0:    
            path.append('RIGHT')
        if vert > 0:
            path.append('UP')
        elif vert < 0:
            path.append('DOWN')      
        return path        

    def compare(self, cell1, cell2):
        """
        Compare 2 cells F values

        @param cell1 1st cell
        @param cell2 2nd cell
        @returns -1, 0 or 1 if lower, equal or greater
        """
        if cell1.f < cell2.f:
            return -1
        elif cell1.f > cell2.f:
            return 1
        return 0
    
    def update_cell(self, adj, cell):
        """
        Update adjacent cell

        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue 
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                return self.display_path()
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))


m = input()
n = raw_input()
grid = []
for i in xrange(0, m):
    grid.append(raw_input().strip())
grid = [x.replace('-', '0') for x in grid]

for i,v in enumerate(grid):
    grid[i] = list(grid[i])
x = 0
y = 0
for i in xrange(len(grid)):
    for j in xrange(len(grid[0])):
        if grid[i][j] == 'm':
            x = i
        if grid[i][j] == 'm':
            y = j
a = AStar()
a.init_grid(x,y, grid)
path = a.process()
displayPathtoPrincess(path)