from random import randint
from copy import deepcopy
import numpy as np

class Matrix():

    def __init__(self, lins, cols):
        self.lins = lins
        self.cols = cols
        self.matrix = np.zeros((lins,cols), dtype=int)
        self.dist = 0
        self.previous = None
        self.move = ""
        self.cost = 0
    
    def validNumbers(self, numbers):
        valid = False
        expected_count = self.lins * self.cols
        if len(numbers) == expected_count:
            ref = list(range(expected_count))
            valid = True
            for i in numbers:
                if int(i) not in ref:
                    valid = False
                else: 
                    ref.remove(int(i))
        return valid

    def buildMatrix(self, str):
        numbers = str.split(",")
        if self.validNumbers(numbers):
            i=0
            for k in range(self.lins):
                for j in range(self.cols):
                    self.matrix[k][j] = int(numbers[i])
                    i += 1

    def searchBlock(self, value):
        for k in range(self.lins):
            for j in range(self.cols):
                if self.matrix[k][j] == value:
                    return (k,j)

    def moveup(self, zero):
        self.matrix[zero[0]][zero[1]] = self.matrix[zero[0]-1][zero[1]]
        self.matrix[zero[0]-1][zero[1]] = 0
    def movedown(self, zero):
        self.matrix[zero[0]][zero[1]] = self.matrix[zero[0]+1][zero[1]]
        self.matrix[zero[0]+1][zero[1]] = 0
    def moveright(self, zero):
        self.matrix[zero[0]][zero[1]] = self.matrix[zero[0]][zero[1]+1]
        self.matrix[zero[0]][zero[1]+1] = 0
    def moveleft(self, zero):
        self.matrix[zero[0]][zero[1]] = self.matrix[zero[0]][zero[1]-1]
        self.matrix[zero[0]][zero[1]-1] = 0

    def getPossibleNodes(self, moves):
        zero = self.searchBlock(0)
        possibleNodes = []
        if zero[0] > 0:
            self.moveup(zero)
            moves.append("up")
            possibleNodes.append(deepcopy(self))
            zero = self.searchBlock(0)
            self.movedown(zero)
            zero = self.searchBlock(0)
        if zero[0] < self.lins - 1:
            self.movedown(zero)
            moves.append("down")
            possibleNodes.append(deepcopy(self))
            zero = self.searchBlock(0)
            self.moveup(zero)
            zero = self.searchBlock(0)
        if zero[1] > 0:
            self.moveleft(zero)
            moves.append("left")
            possibleNodes.append(deepcopy(self))
            zero = self.searchBlock(0)
            self.moveright(zero)
            zero = self.searchBlock(0)
        if zero[1] < self.cols - 1:
            self.moveright(zero)
            moves.append("right")
            possibleNodes.append(deepcopy(self))
            zero = self.searchBlock(0)
            self.moveleft(zero)
            zero = self.searchBlock(0)
        return possibleNodes

    def getXY(self, value, matFinal = None):
        if matFinal is None:
            # Default final state for NxN puzzle
            matFinal = np.zeros((self.lins, self.cols), dtype=int)
            for i in range(self.lins * self.cols - 1):
                matFinal[i // self.cols][i % self.cols] = i + 1
            matFinal[self.lins-1][self.cols-1] = 0
        
        for x in range(self.lins):
            for y in range(self.cols):
                if value == matFinal[x][y]:
                    return (x,y)

    
    def manhattanDist(self):
        res = 0
        for i in range(self.lins):
            for j in range(self.cols):
                if self.matrix[i][j] != 0:
                    fi, fj = self.getXY(self.matrix[i][j])
                    res += abs(fi - i) + abs(fj - j)
        self.dist = res
        return res
    
    def manhattanDistCost(self, Final):
        res = 0
        for i in range(self.lins):
            for j in range(self.cols):
                if self.matrix[i][j] != 0:
                    fi, fj = self.getXY(self.matrix[i][j], Final.matrix)
                    res += abs(fi - i) + abs(fj - j)
        return res

    def getMatrix(self):
        return self.matrix

    def isEqual(self, matrix):
        return (self.matrix == matrix).all()

    def setPrevious(self, p):
        self.previous = p

    def __cmp__(self, other):
        return self.dist == other.dist
    def __lt__(self, other):
        return self.dist < other.dist
