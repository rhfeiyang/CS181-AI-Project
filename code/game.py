import copy

import utils
from people import Seller, SellerChoices, Consumer
from agents import Agent
from copy import deepcopy
class Configuration:
    pass


class AgentState:
    pass


class GameState:
    def __init__(self,agents: list[Seller], sellerNum: int, consumerNum: int, nameList: list, balance: float, dailyCost: float = 0, dailyIncome: float = 0):
        '''
        balance: at the start, all the sellers have the same balance(property)
        '''
        self.sellerNum = sellerNum
        self.consumerNum = consumerNum
        self.nameList = nameList
        self.sellers:list[Seller] = agents
        for agent in agents:
            agent.setBalance(balance)
        self.consumers = [Consumer(i, nameList[i],preference=[-1 for j in range(sellerNum)]) for i in range(consumerNum)]
        self.curConsumer = -1
        self.dailyCost = dailyCost
        self.dailyIncome = dailyIncome

    def getCurrentConsumer(self):
        return self.consumers[self.curConsumer]
    def isLastConsumer(self):
        return self.curConsumer==self.consumerNum-1
    def getNextConsumer(self):
        self.curConsumer = (self.curConsumer+1)%self.consumerNum
        return self.consumers[self.curConsumer]

    def getSellersFromIndex(self, sellerIdx: int) -> Seller:
        return self.sellers[sellerIdx]

    def isWin(self):
        return self.sellers[0].isLive() and all([not seller.isLive() for seller in self.sellers[1:]])

    def isLose(self):
        return not self.sellers[0].isLive()

    def getScore(self):
        return self.sellers[0].getScore()

    def getNumAgents(self):
        return self.sellerNum

    def getLiveAgents(self):
        return sum([i.isLive() for i in self.sellers])

    def getLegalChoices(self, agentIndex: int):
        return [SellerChoices.HIGH, SellerChoices.MEDIUM, SellerChoices.LOW, SellerChoices.SUPERLOW]

    def copy(self):
        '''
        Copy the current GameState
        return: the copy of the current GameState
        '''
        newGameState=copy.deepcopy(self)
        # newGameState = GameState(self.sellers.copy(),self.sellerNum, self.consumerNum, self.nameList, 0.0, self.dailyCost, self.dailyIncome)
        # newGameState.consumerNum = self.consumerNum
        # newGameState.sellerNum = self.sellerNum
        # newGameState.consumers = [Consumer(i, self.nameList[i], self.consumers[i].preference.copy()) for i in range(self.consumerNum)]
        # newGameState.curConsumer = self.curConsumer
        # newGameState.dailyCost = self.dailyCost
        # newGameState.dailyIncome = self.dailyIncome
        return newGameState

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
        newGameState.updateOnce(eatIdx, choice)
        if self.isLastConsumer():
            newGameState.updateDaily()
        return newGameState

    def updateDaily(self):
        for seller in self.sellers:
            seller.loseMoney(self.dailyCost)
            seller.getMoney(self.dailyIncome)
    def updateOnce(self, eatIndex: int, choice: SellerChoices):
        '''
        Update the state of the game.
        eatIndex: the index of the seller who is going to be eaten
        choice: the choice of the seller
        return: None
        '''
        self.getCurrentConsumer().preferenceUpdate(eatIndex, choice)
        self.sellers[eatIndex].getPaid(choice)


class Game:
    def __init__(self, agents: list[Agent], consumerNum, nameList, balance, dailyCost, dailyIncome):
        self.agents:list[Agent] = agents
        self.sellerNum = len(agents)
        self.consumerNum = consumerNum
        self.nameList = nameList
        self.balance = balance
        self.dailyCost = dailyCost
        self.dailyIncome = dailyIncome

        self.gameOver = False
        # self.agentTimeout = False
        # import io
        # self.agentOutput = [io.StringIO() for agent in agents]


    def run(self):
        '''
        Main control loop for game play.
        '''
        self.gameState = GameState(self.agents,self.sellerNum, self.consumerNum, self.nameList,
                                   self.balance, self.dailyCost, self.dailyIncome)
        day=0
        while not self.gameOver:
            day+=1
            print(f"----Day {day} start----")

            # Fetch the next game state
            while True:
                consumer = self.gameState.getNextConsumer()

                # consumuer randomly choose one at first in each day
                sellerIdx = consumer.chooseSeller(self.gameState.sellerNum)
                print(f"Consumer {consumer.name} visit seller {sellerIdx}" )
                sellerAgent = self.agents[sellerIdx]
                # The seller give his choice(price)
                sellerChoice = sellerAgent.getChoice(self.gameState)
                print(f"Seller {sellerIdx} choose price {sellerChoice}")
                # Consumer give his decision
                eatIdx = consumer.eat(sellerIdx, sellerChoice)
                print(f"Consumer {consumer.name} decide to eat at seller {eatIdx}")
                if eatIdx != sellerIdx:
                    sellerAgent = self.agents[eatIdx]
                    sellerChoice = sellerAgent.getChoice(self.gameState)
                    print(f"Seller {eatIdx} choose price {sellerChoice}")

                self.gameState.updateOnce(eatIdx, sellerChoice)
                print(f"consumer {consumer.name} preference:{consumer.preference}")
                print(f"seller {sellerIdx} balance: {self.agents[sellerIdx].getBalance()}")
                self.gameOver = self.gameState.isWin() or self.gameState.isLose()
                print(f"------------------")
                if self.gameState.isLastConsumer() or self.gameOver:
                    break
            self.gameState.updateDaily()
            print(f"Current game state:")
            for consumer in self.gameState.consumers:
                print(f"Consumer {consumer.name} preference: {consumer.preference}")
            for seller in self.agents:
                print(f"Seller {seller.index} balance: {seller.getBalance()}")
            print(f"----Day {day} End----")
        print(f"----Game Over----")

        return self.gameState
