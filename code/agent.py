# multiAgents.py
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


from utils import manhattanDistance
from game import SellerChoices
import random
import utils
import sellerAgent

from seller import Agent


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class ExpectimaxAgent(Agent):
    """
        Your agent for the mini-contest
    """

    def __init__(self, evalFn='contestEvaluationFunction', depth='3'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = utils.lookup(evalFn, globals())
        self.depth = int(depth)

    def getChoice(self, gameState):
        def max_value(gameState, depth, agentIndex):
            v = -999999
            for choice in gameState.getLegalChoices(agentIndex):
                v = max(v, minimax(gameState.getNextState(
                    agentIndex, choice), depth, agentIndex + 1))
            return v

        def exp_value(gameState, depth, agentIndex):
            v = 0
            sellerB = sellerAgent.RandomSeller(agentIndex)
            choiceDistribution = sellerB.getDistribution(gameState)

            for choice, weight in choiceDistribution.items():
                if agentIndex == gameState.getNumAgents() - 1:
                    v += minimax(gameState.getNextState(agentIndex, choice), depth - 1, 0) * weight
                else:
                    v += minimax(gameState.getNextState(agentIndex, choice), depth, agentIndex + 1) * weight
            return v

        def minimax(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            if agentIndex == 0:
                return max_value(gameState, depth, agentIndex)
            else:
                return exp_value(gameState, depth, agentIndex)

        v = -999999
        bestChoice = None
        for choice in gameState.getLegalChoices(0):
            minMaxVal = minimax(
                gameState.getNextState(0, choice), self.depth, 1)
            if v < minMaxVal:
                v = minMaxVal
                bestChoice = choice
        return bestChoice if bestChoice else SellerChoices.NONE
