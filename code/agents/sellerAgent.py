from .baseAgent import Agent
from people.seller import SellerChoices
import utils


class SellerAgent(Agent):
    def __init__(self, index):
        self.index = index

    def getChoice(self, state):
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
        for a in state.getLegalChoices(self.index):
            dist[a] = 1.0
        dist.normalize()
        return dist


class GreedySellerHigh(SellerAgent):
    '''A seller that always prefers to give a high price.'''

    def __init__(self, index):
        self.index = index

    def getDistribution(self, state):
        dist = utils.Counter()
        for a in state.getLegalChoices(self.index):
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
        for a in state.getLegalChoices(self.index):
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
        for a in state.getLegalChoices(self.index):
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
