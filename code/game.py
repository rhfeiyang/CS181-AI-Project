from utils import *
import time
import os
import traceback
import sys
from seller import Seller, SellerChoices
from agent import Agent
from consumer import Consumer


class Configuration:
    pass


class AgentState:
    pass


class GameState:
    def __init__(self, consumerNum: int, sellerNum: int, balance: float, dailyCost: float = 0, dailyIncome: float = 0):
        '''
        balance: at the start, all the sellers have the same balance(property)
        '''
        self.consumerNum = consumerNum
        self.sellerNum = sellerNum
        self.sellers = [Seller(i, balance) for i in range(sellerNum)]
        self.consumers = [Consumer(i) for i in range(consumerNum)]
        self.curConsumer = 0
        self.dailyCost = dailyCost
        self.dailyIncome = dailyIncome

    def getCurrentConsumer(self):
        return self.consumers[self.curConsumer]

    def getSellersFromIndex(self, sellerIdx: int) -> Seller:
        return self.sellers[sellerIdx]

    def isWin(self):
        pass

    def isLose(self):
        pass

    def getScore(self):
        pass

    def getNumAgents(self):
        pass

    def getLegalChoices(self, agentIndex):
        pass

    def copy(self):
        '''
        Copy the current GameState
        return: the copy of the current GameState
        '''
        newGameState = GameState(self.consumerNum, self.sellerNum, 0.0, self.dailyCost, self.dailyIncome)
        newGameState.consumerNum = self.consumerNum
        newGameState.sellerNum = self.sellerNum
        newGameState.sellers = [Seller(i, self.sellers[i]) for i in range(self.sellerNum)]
        newGameState.consumers = [Consumer(i) for i in range(self.consumerNum)]
        newGameState.curConsumer = self.curConsumer
        newGameState.dailyCost = self.dailyCost
        newGameState.dailyIncome = self.dailyIncome

    def getNextState(self, agentIndex: int, choice: SellerChoices):
        '''
        Returns the next GameState if the agent choose choice.
        agentIndex: the index of the agent who is going to choose
        choice: the choice of the agent
        return: the next GameState
        '''
        newGameState = self.copy()
        consumer = newGameState.getCurrentConsumer()
        eatIdx = consumer.eat(agentIndex, choice)
        newGameState.update(eatIdx, choice)
        return newGameState

    def update(self, eatIndex: int, choice: SellerChoices):
        '''
        Update the state of the game.
        eatIndex: the index of the seller who is going to be eaten
        choice: the choice of the seller
        return: None
        '''
        for seller in self.sellers:
            seller.loseMoney(self.dailyCost)
            seller.getMoney(self.dailyIncome)
        self.sellers[eatIndex].getPaid(choice)


class Game:
    def __init__(self, agents: list, consumerNum, balance, dailyCost, dailyIncome):
        self.agents = agents
        self.consumerNum = consumerNum
        self.sellerNum = len(agents)
        self.balance = balance
        self.dailyCost = dailyCost
        self.dailyIncome = dailyIncome

        self.gameOver = False
        # self.agentTimeout = False
        # import io
        # self.agentOutput = [io.StringIO() for agent in agents]
        self.gameState = None

    def run(self):
        '''
        Main control loop for game play.
        '''
        self.gameState = GameState(self.consumerNum, self.sellerNum, self.balance, self.dailyCost, self.dailyIncome)
        while not self.gameOver:
            # Fetch the next game state
            consumer = self.gameState.getCurrentConsumer()
            sellerIdx = consumer.chooseSeller(self.gameState.sellers)
            sellerAgent = self.agents[sellerIdx]
            sellerChoice = sellerAgent.getChoice(self.gameState)
            eatIdx = consumer.eat(sellerIdx, sellerChoice)
            if eatIdx != sellerIdx:
                sellerAgent = self.agents[eatIdx]
                sellerChoice = sellerAgent.getChoice(self.gameState)
            self.gameState.update(eatIdx, sellerChoice)

            self.gameOver = self.gameState.isWin() or self.gameState.isLose()
