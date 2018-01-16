#!/usr/bin/python
# -*- coding: utf-8 -*-
# Weijie Lin
# CISC 3415 hw2-minimax
#

import random

def main():
    gameBoard = TicTacToeBoard()
    a, b = TicTacToeAgent("o"), TicTacToeAgent("x")
    aTurn = True

    while True:
        if aTurn:
            a.move(gameBoard)
            c = "o"
        else:
            b.move(gameBoard)
            c = "x"

        if gameBoard.won(c):
            gameBoard.displayBoard()
            print "%s is the winner\n" % c
            return

        if gameBoard.isFull():
            gameBoard.displayBoard()
            print "Draw\n"
            return

        aTurn = not aTurn


class TicTacToeBoard:

    def __init__(self):
        self.board = ["_"] * 9
        self.availableMoves = [x for x in xrange(0, 9)]

    def displayBoard(self):
        print "\n %s | %s | %s " % (self.board[0], self.board[1], self.board[2])
        print " %s | %s | %s " % (self.board[3], self.board[4], self.board[5])
        print " %s | %s | %s \n" % (self.board[6], self.board[7], self.board[8])

    def isFull(self):
        return True if not self.availableMoves else False

    def won(self, c):
        winPos = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                  (0, 3, 6), (1, 4, 7), (2, 5, 8),
                  (0, 4, 8), (2, 4, 6)]
        for x, y, z in winPos:
            if c == self.board[x] == self.board[y] == self.board[z]:
                return True
        return False

    def move(self, c, pos):
        if (self.board[pos] != "_"):
            raise ValueError("Error: %d is already occupied\n" % pos)

        self.board[pos] = c
        self.availableMoves.remove(pos)


class TicTacToeAgent:

    def __init__(self, c):
        self.c = c

    def otherchr(self, c):
        return "x" if self.c == "o" else "o"

    def move(self, gameBoard):
        pos = self.miniMaxDecision(gameBoard)
        gameBoard.move(self.c, pos)
        gameBoard.displayBoard()
        print "%s move to %d" % (self.c, pos)
        print "*" * 15

    # evaluates current state of board, returns position of best move
    def miniMaxDecision(self, gameBoard):

        if len(gameBoard.availableMoves) == 9:
            return random.choice(gameBoard.availableMoves)

        bestUtil = -99999
        returnPos = None
        availableMoves = gameBoard.availableMoves[:]

        for pos in availableMoves:
            gameBoard.move(self.c, pos)
            util = self.minValue(gameBoard)
            gameBoard.board[pos] = "_"
            gameBoard.availableMoves.append(pos)
            if util > bestUtil:
                bestUtil, returnPos = util, pos

        return returnPos if returnPos is not None else random.choice(gameBoard.availableMoves)

    # evaluates maximum utility of a state
    def maxValue(self, gameBoard):
        terminalState, util = self.terminalTest(gameBoard)

        if terminalState:
            return util

        util = -99999

        availableMoves = gameBoard.availableMoves[:]
        for pos in availableMoves:
            gameBoard.move(self.c, pos)
            util = max(util, self.minValue(gameBoard))
            gameBoard.board[pos] = "_"
            gameBoard.availableMoves.append(pos)
        return util

    # evaluates minimum utility of a state
    def minValue(self, gameBoard):
        terminalState, util = self.terminalTest(gameBoard)

        if terminalState:
            return util

        util = 99999

        availableMoves = gameBoard.availableMoves[:]
        for pos in availableMoves:
            gameBoard.move(self.otherchr(self.c), pos)
            util = min(util, self.maxValue(gameBoard))
            gameBoard.board[pos] = "_"
            gameBoard.availableMoves.append(pos)
        return util

    # returns true if board is full or has three in a row
    def terminalTest(self, gameBoard):
        # return True if gameBoard.won(self.c) or gameBoard.isFull() else False
        # gameBoard.displayBoard
        if gameBoard.won(self.c):
            return (True, 1)

        if gameBoard.won(self.otherchr(self.c)):
            return (True, -1)

        if gameBoard.isFull():
            return (True, 0)

        return (False, 0)

if __name__ == "__main__":
    main()
