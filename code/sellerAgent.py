# sellerAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import Agent
from game import SellerChoices
import random
import utils


class SellerAgent(Agent):
    def __init__(self, index):
        self.index = index

    def getAction(self, state):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return SellerChoices.NONE
        else:
            return utils.chooseFromDistribution(dist)

    def getDistribution(self, state):
        '''Returns a Counter encoding a distribution over actions from the provided state.'''
        utils.raiseNotDefined()


class RandomSeller(SellerAgent):
    '''A seller that always chooses a random action.'''

    def getDistribution(self, state):
        dist = utils.Counter()
        for a in state.getLegalActions(self.index):
            dist[a] = 1.0
        dist.normalize()
        return dist


class GreedySellerHigh(SellerAgent):
    '''A seller that always prefers to give a high price.'''

    def __init__(self, index):
        self.index = index

    def getDistribution(self, state):
        dist = utils.Counter()
        for a in state.getLegalActions(self.index):
            if a == SellerChoices.HIGH:
                dist[a] = 1.0
            else:
                dist[a] = 0.0
        dist.normalize()
        return dist


class GreedySellerLow(SellerAgent):
    '''
    A seller that prefers to give a high price if consumer prefers the seller,
    But will lower the price if the consumer is not willing to pay,
    or seller does not have risk of being bankrupt.
    '''

    def __init__(self, index):
        self.index = index

    def getDistribution(self, state):
        dist = utils.Counter()
        for a in state.getLegalActions(self.index):
            if state.getCurrentConsumer().isPrefer(self.index):
                if a == SellerChoices.HIGH:
                    dist[a] = 1.0
                else:
                    dist[a] = 0.0
            else:
                if a == SellerChoices.LOW:
                    dist[a] = 1.0
                else:
                    dist[a] = 0.0
        dist.normalize()
        return dist


class GreedySellerSuperLow(SellerAgent):
    '''
    A seller that prefers to give a high price if consumer prefers the seller,
    But will lower the price if the consumer is not willing to pay,
    or seller does not have risk of being bankrupt.
    '''

    def __init__(self, index):
        self.index = index

    def getDistribution(self, state):
        dist = utils.Counter()
        for a in state.getLegalActions(self.index):
            if state.getCurrentConsumer().isPrefer(self.index):
                if a == SellerChoices.HIGH:
                    dist[a] = 1.0
                else:
                    dist[a] = 0.0
            else:
                if a == SellerChoices.SUPERLOW:
                    dist[a] = 1.0
                else:
                    dist[a] = 0.0
        dist.normalize()
        return dist
