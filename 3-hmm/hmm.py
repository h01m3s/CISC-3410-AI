#!/usr/bin/python
# -*- coding: utf-8 -*-
# Weijie Lin
# CISC 3415 hw2-minimax
#

# typedef std::vector<std::string> Observations
# typedef std::map<std::string, float> Distribution;
# HMM::Distribution pprobs;
# std::map<std::string, HMM::Distribution> oprobs, tprobs;
# std::vector<std::string> states, observations;

import sys
import os
import numpy as np

class HMM(object):

    def __init__(self, fname):
        # self.states = self.observations = []
        # self.oprobs = self.tprobs = self.pprobs = {}
        self.states = []; self.observations = []; self.observed = []
        # pprobs: {observation: prob}
        # tprobs: {state: {state: prob}}, oprobs: {observation: {state:prob}}
        self.oprobs = {}; self.tprobs = {}; self.pprobs = {}
        self.loadDataFromFile(fname)
        self.printAllData()

    def normalize(self, pprobDict):
        # probArr has to be np.array() in order to use sum() function
        probSum = sum(pprobDict.itervalues())

        if not probSum:
            print 'Error: all probabilities are zero\n'
            raise

        for state, prob in pprobDict.iteritems():
            pprobDict[state] = round(prob/probSum, 2)

        return pprobDict

    def normalizeArr(self, arr):
        arr = np.array(arr)
        return [round(prob/arr.sum(), 2) for prob in arr]

    def printAllData(self):
        print '*' * 35
        print 'states: {}'.format(self.states)
        print 'observations: {}'.format(self.observations)
        print 'pprobs: {}'.format(self.pprobs)
        print 'oprobs: {}'.format(self.oprobs)
        print 'tprobs: {}'.format(self.tprobs)
        print 'observed: {}'.format(self.observed)
        print '*' * 35

    def loadDataFromFile(self, fname):
        # Load data file under current fonder
        fullPath = os.path.join(sys.path[0], fname)
        with open(fullPath, 'r') as dataFile:
            # load possible states and observations
            self.states = [state.strip() for state in dataFile.readline().split(' ')]

            self.observations = [observation.strip() for observation in dataFile.readline().split(' ')]

            # load prior probabilities
            dataFile.readline()
            if dataFile.readline().strip() == '# PRIOR':
                probs = [float(prob.strip()) for prob in dataFile.readline().split(' ')]
                self.pprobs = dict(zip(self.states, probs))

            # load observation probabilities
            dataFile.readline()
            if dataFile.readline().strip() == '# OBSERVATION':
                for _, observation in enumerate(self.observations):
                    probs = [float(prob.strip()) for prob in dataFile.readline().split(' ')]
                    self.oprobs[observation] = dict(zip(self.states, probs))

            # load transition probabilities
            dataFile.readline()
            if dataFile.readline().strip() == '# TRANSITION':
                for _, state in enumerate(self.states):
                    probs = [float(prob.strip()) for prob in dataFile.readline().split(' ')]
                    self.tprobs[state] = dict(zip(self.states, probs))

            # load observations
            dataFile.readline()
            if dataFile.readline().strip() == '# OBSERVATIONS':
                self.observed = [observe.strip() for observe in dataFile.readline().split(' ')]

    def filter(self):
        # TODO: Filtering: Given a list of T observations, return the
        # posterior probability distribution over the most recent state
        # (Given the observations, what is the probability the
        # most recent state has each of the possible values)
        # (In this case, sunny, rainy, or foggy)
        yestProbs = self.pprobs
        for observation in self.observed:
            todayProbs = {}
            for state in self.states:
                oprob = self.oprobs[observation][state]
                tprob = 0
                for pState, prob in yestProbs.iteritems():
                    tprob += (prob * self.tprobs[pState][state])
                todayProbs[state] = oprob * tprob
            yestProbs = self.normalize(todayProbs)
            print 'todayProbs: {}'.format(todayProbs)


    def viterbi(self):
        # TODO: Viterbi: Given a list of T observations, return the most
        # likely sequence of states (e.g. { "sunny", "rainy", "foggy" ... }
        bp = {}
        yestProbs = self.pprobs
        for observation in self.observed:
            bestYestStates = {}; todayProbs = {}
            for state in self.states:
                bestprob = -float('inf')
                for pState, prob in yestProbs.iteritems():
                    tprob = prob * self.tprobs[pState][state]
                    print 'tprob: {}'.format(tprob)
                    if tprob > bestprob:
                        bestprob = tprob
                        bestYestStates[pState] = tprob
            print 'bestprob: {}'.format(bestprob)
            print 'bestYestStates: {}'.format(bestYestStates)
        # for state in self.states:
        #     bestprob = -float('inf')
        #     for pState, prob in yestProbs.iteritems():
        #         bestYestStates = {}
        #         tprob = prob * self.tprobs[pState][state]
        #         if tprob > bestprob:
        #             bestprob = tprob
        #             bestYestStates[pState] = tprob
        # print 'bestYestStates: {}'.format(bestYestStates)



def main():
    try:
        # fname = sys.argv[1] + '.data'
        fname = 'weather.data'
        hmm = HMM(fname)
        hmm.filter()
    except Exception as e:
        print '\nUSAGE: python hmm.py PROBLEMNAME\n'
        exit(1)

if __name__ == '__main__':
    fname = 'weather.data'
    hmm = HMM(fname)
    hmm.filter()
    # hmm.viterbi()
    # print hmm.normalizeArr([0.015, 0.0225, 0.0375])
    # main()
