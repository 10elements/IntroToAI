__author__ = 'zhangtianyao'
import random
import numpy as np
M = 101
N = 101
def neighbors(cell):
    allNeighbors = []
    row = cell[0]
    column = cell[1]
    if row > 0 and row < M - 1:
        allNeighbors.append((row + 1,column))
        allNeighbors.append((row - 1,column))
        pass
    elif row == M-1:
        allNeighbors.append((row - 1,column))
    elif row == 0:
        allNeighbors.append((row + 1,column))

    if column > 0 and column < N - 1:
        allNeighbors.append((row,column + 1))
        allNeighbors.append((row,column - 1))
        pass
    elif column == N - 1:
        allNeighbors.append((row,column - 1))
    elif column == 0:
        allNeighbors.append((row,column + 1))

    return allNeighbors

def neighborAllVisited(cell,visited):
    neighborsList = neighbors(cell)
    for neighbor in neighborsList:# print neighbor[0],neighbor[1],neighbor[1]*101+neighbor[0]
        if visited[neighbor[0] * N + neighbor[1]] == 0:
            return False            
    return True

def removeVisitedNeighbors(neighbors,visited):
    delList =[]
    for neighbor in neighbors:
        if visited[neighbor[0] * N + neighbor[1]] == 1:# if visited
            delList.append(neighbor)
    for item in delList:
        neighbors.remove(item)

def randomDFS(stack,visited,gridWorld):
    random.seed()
    while len(stack) != 0:
        currentCell = stack[len(stack) - 1]
        if neighborAllVisited(currentCell,visited):# if all neighbors visited, pop
            stack.pop()
        else:
            neighborsList = neighbors(currentCell)
            removeVisitedNeighbors(neighborsList,visited)
            chosenNeighbor = neighborsList[random.randint(0,len(neighborsList) - 1)]# randomly choose an unvisited neighbor
            visited[chosenNeighbor[0] * N + chosenNeighbor[1]] = 1# mark it visited
            prob = random.random()
            if prob <= 0.3:
                gridWorld[chosenNeighbor[0]][chosenNeighbor[1]] = 1# 30% prob blocked   
            else:# 70% prob unblocked
                stack.append(chosenNeighbor)

def generate():
    envmts = []
    c = 0
    for counter in range(50):
        gridWorld = [[0 for i in range(N)] for j in range(M)]
        visited = [0 for i in range(M * N)]
        random.seed()
        startRow = random.randint(0, M - 1)
        startColumn = random.randint(0, N - 1)
        visited[startRow * N + startColumn] = 1# mark it visited
        gridWorld[startRow][startColumn] = 0# mark it unblocked
        stack = [(startRow,startColumn)]# initialize stack
        randomDFS(stack,visited,gridWorld)
        while 0 in visited:#not all cell visited y
            row = int(visited.index(0) / N)
            column = int(visited.index(0) % N)
            visited[visited.index(0)] = 1#mark it visited
            gridWorld[row][column] = 0#mark it unblocked
            stack.append((row,column))
            randomDFS(stack,visited,gridWorld)
        c = c + 1
        blockedCells = sum([ sum(gridWorld[i]) for i in range(len(gridWorld)) ])
        blockedpercent = float(blockedCells)/(M * N)
        print ((c,blockedpercent))    
        envmts.append(gridWorld)
    return envmts

def view(envmts,index):
    for row in envmts[index]:
        print (row)

def main():
    e = generate()
    counter = 0
    for world in e:
        np.save('gridWorlds/NO%dworld.npy'%counter,np.array(world))
        counter += 1

if __name__ == '__main__':
    main()
