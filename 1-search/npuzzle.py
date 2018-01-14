#!/usr/bin/python
# -*- coding: utf-8 -*-
# Weijie Lin
# CISC 3415 hw1-search

import sys
import time

lineSize = 0

def main():

    startTime = time.time()

    try:
        puzzleFile = sys.argv[1]
        algorithmType = sys.argv[2]
    except:
        print "Usage: python npuzzle.py <FILENAME> <SEARCHTYPE>"
        print "<FILENAME> should be a text file where each line contains a puzzle."
        print "<SEARCHTYPE> should be 'd' for depth-first search, 'b' for breadth-first search, 'a' for A*"
        sys.exit(1)

    inFile = open(puzzleFile, "r")
    outFile = open("mySolution.txt", "w")

    for i in xrange(0, 4):
        global currentSolution
        currentSolution = []
        board = [int(x) for x in inFile.readline().rstrip().split(" ")]

        node = Node(board, None)

        puzzleSolver(node, algorithmType)
        result =  " ".join(currentSolution) + "\n"
        outFile.write(result)


    endTime = time.time()
    print "\nRun Time: ", endTime - startTime
    inFile.close()
    outFile.close()


def getSolution(node):
    global currentSolution

    if node.parent == None:
        # print "START",
        currentSolution.append("START")
        return

    getSolution(node.parent)
    currentSolution.append(node.move)
    # print node.move,

    return


def misplacedTile(node):
    heuristicCost = 0
    for i in xrange(len(node.board)):
        if node.board.index(i) != i:
            heuristicCost += 1
    return heuristicCost


def manhattanDistance(node):
    heuristicCost = 0
    for i in xrange(len(node.board)):
        if node.board.index(i) != i:
            colDistance = abs(node.board.index(i) % lineSize - i % lineSize)
            rowDistance = abs(node.board.index(i) // lineSize - i // lineSize)
            heuristicCost += colDistance + rowDistance
    return heuristicCost


def puzzleSolver(node, algorithm):

    if not isValidBoard(node.board):
        print "Not a Valid Board."
        sys.exit(1)

    if not isSolvable(node.board):
        print "Puzlle Is Not Solable!"
        sys.exit(1)

    queue = [node]
    closed = [node.board]
    count = 0

    while 1:
        # Sort queue by heuristicCost if Use A Star Algorithm
        if algorithm == "a":
            queue = sorted(queue, key=lambda x:x.heuristicCost)

        count += 1
        checkNode = queue[-1] if algorithm == "d" else queue[0]

        # print "queue length: ", len(queue)
        # print "count: ", count
        # print "heuristic Cost: ", checkNode.heuristicCost
        # checkNode.printBoard()

        if isGoalState(checkNode.board):
            getSolution(checkNode)
            print
            # print "\nDepth Searched: ", checkNode.depth
            return

        # Last In First Out for Depth-First Search
        # Otherwise Pop First node
        if algorithm == "d":
            queue.pop()
        else:
            queue.pop(0)

        expandList = expand(checkNode)

        for tmpNode in expandList:

            if tmpNode.board not in closed:
                tmpNode.depth = checkNode.depth + 1
                # Use Manhattan Distance or MisplacedTile as heuristicCost
                tmpNode.heuristicCost = manhattanDistance(tmpNode) if algorithm == "a" else None
                # tmpNode.heuristicCost = misplacedTile(tmpNode) if algorithm == "a" else None
                closed.append(tmpNode.board)
                queue.append(tmpNode)

def isSolvable(board):
    # Check if game is solvable by checking inversion count
    inversionCount = 0
    tmpBoard = [x for x in board if x != 0]
    length = len(tmpBoard)

    if length == 3:
        return True

    for i in xrange(length):
        for j in xrange(i + 1, length):
            if tmpBoard[i] > tmpBoard[j]:
                inversionCount += 1

    return True if (inversionCount % 2 == 0) else False


def isValidBoard(board):
    # Check if board is valid
    global lineSize

    if len(set(board)) != len(board):
        return False
    lineSize = int(len(board)**(0.5))

    return True if (lineSize * lineSize) == len(board) else False


def isGoalState(board):
    return sorted(board) == board


def expand(node):
    global lineSize
    expandList = []
    indexOfZero = node.board.index(0)

    # Move Left
    if indexOfZero % lineSize == 0:
        pass
    else:
        tmpBoard = node.board[:]
        tmpBoard[indexOfZero], tmpBoard[indexOfZero -
                                        1] = tmpBoard[indexOfZero - 1], tmpBoard[indexOfZero]
        tmpNode = Node(tmpBoard, node)
        tmpNode.move = "left"
        expandList.append(tmpNode)

    # Move Right
    if (indexOfZero + 1) % lineSize == 0:
        pass
    else:
        tmpBoard = node.board[:]
        tmpBoard[indexOfZero], tmpBoard[indexOfZero +
                                        1] = tmpBoard[indexOfZero + 1], tmpBoard[indexOfZero]
        tmpNode = Node(tmpBoard, node)
        tmpNode.move = "right"
        expandList.append(tmpNode)

    # Move Up
    if indexOfZero < lineSize:
        pass
    else:
        # Not copy reference of original board
        tmpBoard = node.board[:]
        tmpBoard[indexOfZero], tmpBoard[indexOfZero -
                                        lineSize] = tmpBoard[indexOfZero - lineSize], tmpBoard[indexOfZero]
        tmpNode = Node(tmpBoard, node)
        tmpNode.move = "up"
        expandList.append(tmpNode)

    # Move Down
    if indexOfZero >= (len(node.board) - lineSize):
        pass
    else:
        tmpBoard = node.board[:]
        tmpBoard[indexOfZero], tmpBoard[indexOfZero +
                                        lineSize] = tmpBoard[indexOfZero + lineSize], tmpBoard[indexOfZero]
        tmpNode = Node(tmpBoard, node)
        tmpNode.move = "down"
        expandList.append(tmpNode)

    # Return Expanded List
    return expandList


class Node:

    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.move = None
        self.heuristicCost = 999
        self.depth = 0

    def printBoard(self):
        print "*" * 35, "\n"

        for i in xrange(len(self.board)):
            if (self.board[i]) == 0:
                print " ",
            else:
                print self.board[i],
            if (i + 1) % lineSize == 0:
                print "\n"

        print "*" * 35, "\n"


if __name__ == "__main__":
    main()
