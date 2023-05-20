from game import SellerChoices
import random

from .sellerAgent import *

from .baseAgent import Agent
from .RL.QlearningAgent import *


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


def scoreEvaluationFunction2(currentGameState):
    scoreList = currentGameState.getAllScore()

    return scoreList[0] - scoreList[1]


def scoreEvaluationFunction3(currentGameState):
    scoreList = currentGameState.getAllScore()

    return scoreList[0] - random.gauss(scoreList[1], scoreList[1]/20)


def betterEvaluationFunction(currentGameState):
    prefers = currentGameState.getAllConsumersPreference()
    return currentGameState.getScore() + 0.5 * sum([prefers[i][0] for i in range(len(prefers))])


class ExpectimaxAgent(Agent):
    """
        Your agent for the mini-contest
    """

    def __init__(self, belief: SellerAgent, evalFn='betterEvaluationFunction', depth='2'):
        super().__init__()
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = utils.lookup(evalFn, globals())
        self.depth = int(depth)
        self.belief = belief

    def getChoice(self, gameState):
        def max_value(gameState, depth, agentIndex):
            v = -999999
            for choice in gameState.getLegalChoices(agentIndex):
                v = max(v, minimax(gameState.getNextState(
                    agentIndex, choice), depth, agentIndex + 1))
            return v

        def exp_value(gameState, depth, agentIndex):
            v = 0
            sellerB = self.belief(agentIndex)
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
            minMaxVal = minimax(gameState.getNextState(0, choice), self.depth, 1)
            if v < minMaxVal:
                v = minMaxVal
                bestChoice = choice
        return bestChoice if bestChoice else SellerChoices.NONE


class AlphaBetaAgent(Agent):
    """
        Your minimax agent with alpha-beta pruning
    """

    def __init__(self, evalFn='betterEvaluationFunction', depth='1'):
        super().__init__()
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = utils.lookup(evalFn, globals())
        self.depth = int(depth)

    def getChoice(self, gameState):
        def max_value(gameState, depth, agentIndex, alpha, beta):
            v = -999999
            for choice in gameState.getLegalChoices(agentIndex):
                v = max(v, minimax(gameState.getNextState(
                    agentIndex, choice), depth, agentIndex + 1, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(gameState, depth, agentIndex, alpha, beta):
            v = 999999
            for choice in gameState.getLegalChoices(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    v = min(v, minimax(gameState.getNextState(
                        agentIndex, choice), depth - 1, 0, alpha, beta))
                else:
                    v = min(v, minimax(gameState.getNextState(
                        agentIndex, choice), depth, agentIndex + 1, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        def minimax(gameState, depth, agentIndex, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            if agentIndex == 0:
                return max_value(gameState, depth, agentIndex, alpha, beta)
            else:
                return min_value(gameState, depth, agentIndex, alpha, beta)

        v = -999999
        bestChoice = None
        alpha, beta = -999999, 999999
        for choice in gameState.getLegalChoices(0):
            minMaxVal = minimax(
                gameState.getNextState(0, choice), self.depth, 1, alpha, beta)
            if v < minMaxVal:
                v = minMaxVal
                bestChoice = choice
            alpha = max(alpha, v)
        return bestChoice if bestChoice else SellerChoices.NONE


class NeuralNetworkAgent(Agent):
    """
        Your minimax agent with Neural Network
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='3'):
        super().__init__()
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = utils.lookup(evalFn, globals())
        self.depth = int(depth)

    def getChoice(self, gameState):
        def max_value(gameState, depth, agentIndex, alpha, beta):
            v = -999999
            for choice in gameState.getLegalChoices(agentIndex):
                v = max(v, minimax(gameState.getNextState(
                    agentIndex, choice), depth, agentIndex + 1, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(gameState, depth, agentIndex, alpha, beta):
            v = 999999
            for choice in gameState.getLegalChoices(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    v = min(v, minimax(gameState.getNextState(
                        agentIndex, choice), depth - 1, 0, alpha, beta))
                else:
                    v = min(v, minimax(gameState.getNextState(
                        agentIndex, choice), depth, agentIndex + 1, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        def minimax(gameState, depth, agentIndex, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            if agentIndex == 0:
                return max_value(gameState, depth, agentIndex, alpha, beta)
            else:
                return min_value(gameState, depth, agentIndex, alpha, beta)

        v = -999999
        bestChoice = None
        alpha, beta = -999999, 999999
        for choice in gameState.getLegalChoices(0):
            minMaxVal = minimax(
                gameState.getNextState(0, choice), self.depth, 1, alpha, beta)
            if v < minMaxVal:
                v = minMaxVal
                bestChoice = choice
            alpha = max(alpha, v)
        return bestChoice if bestChoice else SellerChoices.NONE
