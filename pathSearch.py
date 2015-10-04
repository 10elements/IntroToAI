__author__ = 'zhangtianyao'
from heapq import *
import random
import matplotlib.pyplot as plt
import priority_queue
import numpy as np

R = 101
C = 101

class state:
    """docstring for state"""

    def __init__(self, gValue, search, tree, blocked, row, column):
        self.gValue = gValue
        self.gValue = gValue
        self.search = search
        self.tree = tree
        self.blocked = blocked
        self.row = row
        self.column = column


def initStates():
    states = [[state(None, 0, None, False, j, i) for i in range(C)] for j in range(R)]
    return states


def blockageStatus(state, stateSpace, gridWorld):
    neighborsList = neighbors(state)
    for neighbor in neighborsList:
        if gridWorld[neighbor[0]][neighbor[1]] == 1:  # blocked
            stateSpace[neighbor[0]][neighbor[1]].blocked = True


def neighbors(state):  # return row and column of neighbors
    neighborsList = []
    row = state.row
    column = state.column
    if row > 0 and row < R - 1:
        neighborsList.append((row - 1, column))
        neighborsList.append((row + 1, column))
    elif row == R - 1:
        neighborsList.append((row - 1, column))
    elif row == 0:
        neighborsList.append((row + 1, column))

    if column > 0 and column < C - 1:
        neighborsList.append((row, column + 1))
        neighborsList.append((row, column - 1))
    elif column == C - 1:
        neighborsList.append((row, column - 1))
    elif column == 0:
        neighborsList.append((row, column + 1))
    return neighborsList


def removeVisitedNeighbors(neighbors, visited):
    delList = []
    for neighbor in neighbors:
        if visited[neighbor[0] * C + neighbor[1]] == 1:  # visited
            delList.append(neighbor)
    for delItem in delList:
        neighbors.remove(delItem)

def removeBlockedNeighbors(neighbors, stateSpace):
    delList = []
    for neighbor in neighbors:
        if stateSpace[neighbor[0]][neighbor[1]].blocked:
            delList.append(neighbor)
    for delItem in delList:
        neighbors.remove(delItem)

def cost(state):
    if state.blocked:  # if blocked, increase the cost to infinity
        return float('inf')
    else:
        return 1


def searchPath(stateSpace, gridWorld, start, goal, counter):
    # breaks tie in favor of small gValue, use -gValue infavor of big gValue
    frontier = priority_queue.PriorityQueue()
    frontier.put((start.gValue + abs(start.row - goal.row) + abs(start.column - goal.column), start.gValue), start)
    # visited = [0 for i in range(R * C)]
    visited = np.zeros(R * C, dtype = np.int)
    while not frontier.is_empty():
        print ('in outerloop')
        # print ('currentState:',frontier[0])
        currentState = frontier.pop()  # pop state with least f(s),if f(s) equals, with least g(s)
        if currentState == goal:  # reach goal state
            print ('reeeeeeeeeeeeeach')
            return True
        visited[currentState.row * C + currentState.column] = 1  # mark it visited
        neighborStates = neighbors(currentState)
        print ('neighbors:', neighborStates)
        removeVisitedNeighbors(neighborStates, visited)
        print ('unvisited neighbors:', neighborStates)
        removeBlockedNeighbors(neighborStates, stateSpace)
        print ('unvisited unblocked neighbors:', neighborStates)
        if len(neighborStates) != 0:
            for state in neighborStates:  # for each unvisited unblocked neighbor
                print ('in innerloop')
                temp = stateSpace[state[0]][state[1]]
                if temp.search < counter:  # whether first generated in counter'th search, avoid initializing gValue of all states before each search.
                    temp.gValue = float('inf')  # initialize gvalue to infinity
                    temp.search = counter  # mark it as generated in counter'th search
                if currentState.gValue + 1 < temp.gValue:  # if a shorter path to a generating state found, update it
                    temp.gValue = currentState.gValue + 1
                    temp.tree = currentState
                    frontier.put((temp.gValue + abs(temp.row - goal.row) + abs(temp.column - goal.column), temp.gValue), temp)
    return False


def markTrace(path, gridWorld):
    for move in path:
        gridWorld[move[0]][move[1]] = 3


def repeatedSearch(stateSpace, gridWorld, start, goal):
    initialStart = start
    finalPath = [(start.row,start.column)]
    counter = 0
    blockageStatus(start, stateSpace, gridWorld)
    while start != goal:
        counter = counter + 1  # counter'th search
        start.gValue = 0
        goal.gValue = float('inf')
        if not searchPath(stateSpace, gridWorld, start, goal, counter):  # can not reach the goal
            return False
        pointer = goal
        path = []
        while pointer != start:  # follow the tree from goal to start
            print('traversing path')
            path.append((pointer.row,pointer.column))
            pointer = pointer.tree
        path.append((start.row,start.column))
        path.reverse()
        for i in range(len(path)):
            subPath = []
            blockageStatus(stateSpace[path[i][0]][path[i][1]], stateSpace, gridWorld)  # each move check neighors' blockage status
            if stateSpace[path[i][0]][path[i][1]] == goal:  # reach the goal
                p = goal
                while p != start:
                    subPath.insert(0,(p.row, p.column))
                    p = p.tree
                finalPath += subPath
                markTrace(finalPath, gridWorld)
                return True
            if stateSpace[path[i + 1][0]][path[i + 1][1]].blocked:
                print('search path again')
                p = stateSpace[path[i][0]][path[i][1]]
                while p != start:
                    subPath.insert(0,(p.row, p.column))
                    p = p.tree
                finalPath += subPath# add subPath to finalPath
                start = stateSpace[path[i][0]][path[i][1]]  # set start to current move
                break

def display(gridWorld):
    ax = plt.axes()
    ax.imshow(gridWorld, cmap=plt.cm.gray, interpolation='none')
    ax.grid(True)
    plt.show()

def main():
    mapName = input('choose gridWorld: ')
    gridWorld = np.load('gridWorlds/'+mapName)
    display(gridWorld)
    
if __name__ == '__main__':
    main()
# stateSpace = initStates()
# gridWorld = [[0 for i in range(20)] for j in range(20)]
# gridWorld = e[3]
# testWorld = np.array(gridWorld)
# generateEnvmt.view(e, 3)
# np.save('testWorld.npy',testWorld)
# gridWorld = np.load('testWorld.npy')
# print(gridWorld)
# startRow = int(input('input startRow: '))
# startCol = int(input('inout startCol: '))
# goalRow = int(input('input goalRow: '))
# goalCol = int(input('input goalCol: '))
# start = stateSpace[startRow][startCol]
# # start.blocked = False
# # start.gValue = 0
# goal = stateSpace[goalRow][goalCol]
# # goal.blocked = False
# # goal.gValue = float('inf')
# if repeatedSearch(stateSpace, gridWorld, start, goal):
#     for r in gridWorld:
#         print(r)
# else:
#     print('can not reach the goal')
