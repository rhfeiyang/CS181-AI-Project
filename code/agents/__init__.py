from .baseAgent import Agent
from .learningAgent import *
from .playerAgent import *
from .sellerAgent import *

def peopleFind(name):
    # Notice this return a class type
    player=None
    if name=='ExpectimaxAgent':
        player=ExpectimaxAgent
    elif name=='AlphaBetaAgent':
        player=AlphaBetaAgent
    elif name=='ApproximateQAgent':
        player=ApproximateQAgent
    elif name=='MCQAgent':
        player=MCQAgent
    elif name=='RandomSeller':
        player=RandomSeller
    elif name=='GreedySellerHigh':
        player=GreedySellerHigh

    elif name=='GreedySellerLow':
        player=GreedySellerLow
    elif name=='GreedySellerSuperLow':
        player=GreedySellerSuperLow
    elif name=='neuralPredictSeller':
        pass
        # player=neuralPredictSeller

    else:
        raise Exception("Unknown player type")
    return player