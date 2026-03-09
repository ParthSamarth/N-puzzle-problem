from random import randint
from matrix import Matrix
from queue import PriorityQueue, Queue
import random
import pygame
import colors
import numpy as np
import time

class Puzzle:
    
    def __init__(self, x, y, width, height, lastSolveTime, move, cost, matrix,  blocks = [], final_state = "1,2,3,4,5,6,7,8,0", grid_size = 3):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lastSolveTime = lastSolveTime
        self.move = move
        self.cost = cost
        self.matrix = matrix
        self.blocks = blocks
        self.final_state = final_state
        self.grid_size = grid_size

    @staticmethod
    def new(x, y, width, height, grid_size=3):
        return Puzzle(x, y, width, height, 0, [], 0, Matrix(grid_size, grid_size), [], grid_size=grid_size)

    def validNumbers(self, numbers):
        valid = False
        expected_count = self.grid_size * self.grid_size
        if len(numbers) == expected_count:
            ref = list(range(expected_count))
            valid = True
            for i in numbers:
                if int(i) not in ref:
                    valid = False
                else: 
                    ref.remove(int(i))
        return valid
    
    def randomBlocks(self): 
        n = randint(30,40)
        for i in range(n):
            zero = self.matrix.searchBlock(0)
            possibleMoves = []
            #move up
            if zero[0] > 0:
                possibleMoves.append(self.matrix.moveup)
            if zero[0] < self.grid_size - 1:
                possibleMoves.append(self.matrix.movedown)
            if zero[1] > 0:
                possibleMoves.append(self.matrix.moveleft)
            if zero[1] < self.grid_size - 1:
                possibleMoves.append(self.matrix.moveright)
            random.choice(possibleMoves)(zero)
        self.setBlocksMatrix()

    def setBlocksMatrix(self):
        blocks = []
        block_x=self.x
        block_y=self.y
        block_w = self.width/self.grid_size
        block_h = self.height/self.grid_size

        m = self.matrix.getMatrix()
        i=0
        for k in range(self.grid_size):
            for j in range(self.grid_size):
                blocks.append({'rect':pygame.Rect(block_x, block_y, block_w, block_h),'color':colors.BABY_PINK,'block':m[k][j]})
                block_x += block_w+1 
                i+=1
            block_y += block_h+1
            block_x = self.x
        self.blocks = blocks

    def setBlocks(self, string):
        numbers = string.split(",")
        blocks = []
        if self.validNumbers(numbers) :
            block_x=self.x
            block_y=self.y

            block_w = self.width/self.grid_size
            block_h = self.height/self.grid_size
            self.matrix.buildMatrix(string)
            i=0
            for k in range(self.grid_size):
                for j in range(self.grid_size):
                    blocks.append({'rect':pygame.Rect(block_x, block_y, block_w, block_h),'color':colors.BABY_PINK,'block':int(numbers[i])})
                    block_x += block_w+1 #right
                    i+=1
                block_y += block_h+1 #down
                block_x = self.x
            self.blocks = blocks
            return True
        return False

    def generateDefaultFinalState(self):
        """Generate default final state for current grid size"""
        numbers = []
        for i in range(1, self.grid_size * self.grid_size):
            numbers.append(str(i))
        numbers.append("0")  # Empty space at the end
        return ",".join(numbers)

    def initialize(self):
        if self.final_state == "1,2,3,4,5,6,7,8,0" and self.grid_size != 3:
            # Generate appropriate final state for non-3x3 grids
            self.final_state = self.generateDefaultFinalState()
        blocks = self.final_state
        self.setBlocks(blocks)

    def existsIn(self,elem, list = []):
        for item in list:
            if item.isEqual(elem):
                return True
        return False

    def getCost(self,actual):
        while(actual > 0):
            return 1

    def isSolvable(self):
        """Check if the current puzzle state is solvable"""
        try:
            # For now, assume all puzzles are solvable
            # In a more complete implementation, you would check inversion count
            return True
        except Exception as e:
            print(f"Error checking solvability: {e}")
            return False


    def bestFirst(self):
        #função de avaliação por busca em largura
        inicio = time.time()
        node = self.matrix
        Mfinal = Matrix(self.grid_size, self.grid_size)
        Mfinal.buildMatrix(self.final_state)
        final = Mfinal.getMatrix()
        queue = PriorityQueue()
        queue.put(node)
        visitedNodes = []
        n = 1
        
        while(not node.isEqual(final) and not queue.empty()):
            node = queue.get()
            visitedNodes.append(node)
            moves = []
            childNodes = node.getPossibleNodes(moves)
            for i in range(len(childNodes)):
                if not self.existsIn(childNodes[i].getMatrix(),visitedNodes):
                    childNodes[i].move = moves[i]
                    childNodes[i].manhattanDist()
                    childNodes[i].setPrevious(node)
                    queue._put(childNodes[i])
            n += 1
        moves = []
        self.cost = n
        if(node.isEqual(final)):
            moves.append(node.move)
            nd = node.previous
            while nd != None:
                if nd.move != '':
                    moves.append(nd.move)
                nd = nd.previous
        fim = time.time()
        self.lastSolveTime = fim-inicio
        print("## Best-First ##\n")
        print("Tempo gasto {temp: .5f}:".format(temp = fim-inicio))
        print("Tós visitados:",n,"\n")
        return moves[::-1]
    
    def a_star(self):
        # iniciando timer
        inicio = time.time()
        node = self.matrix
        Mfinal = Matrix(self.grid_size, self.grid_size)
        Mfinal.buildMatrix(self.final_state)
        final = Mfinal.getMatrix()
        queue = PriorityQueue()
        queue.put(node)
        visitedNodes = []
        indexSelected = 0
        n = 1        
        while (not node.isEqual(final) and not queue.empty()):
            node = queue.get()
            visitedNodes.append(node)
            moves = []
            childNodes = node.getPossibleNodes(moves)
            for i in range(len(childNodes)):
                if not self.existsIn(childNodes[i].getMatrix(), visitedNodes):
                    childNodes[i].move = moves[i]
                    childNodes[i].manhattanDist()
                    childNodes[i].setPrevious(node)
                    # Cumulating the cost function
                    childNodes[i].cost = node.cost + node.manhattanDistCost(childNodes[i])
                    childNodes[i].dist += childNodes[i].cost
                    queue._put(childNodes[i])
            n += 1
            auxCost = 0
            
        moves = []
        self.cost = n
        if(node.isEqual(final)):
            moves.append(node.move)
            nd = node.previous
            while nd != None:
                if nd.move != '':
                    moves.append(nd.move)
                nd = nd.previous
                
        fim = time.time()
        self.lastSolveTime = fim-inicio
        print("## A* ##\n")
        print("Tempo gasto {temp: .5f}:".format(temp = fim-inicio))
        print("Nós visitados:",n,"\n")
        
        return moves[::-1]