import copy

import utils
from people import Seller, SellerChoices, Consumer
from agents import Agent
from copy import deepcopy
from numpy import argmax
from typing import List


class Configuration:
    pass


class AgentState:
    pass


class GameState:
    def __init__(self, agents: List[Seller], sellerNum: int, consumerNum: int, nameList: list, balance: float, dailyCost: float = 0, dailyIncome: float = 0):
        '''
        balance: at the start, all the sellers have the same balance(property)
        '''
        self.sellerNum = sellerNum
        self.consumerNum = consumerNum
        self.nameList = nameList
        self.sellers: List[Seller] = agents
        for agent in agents:
            agent.setBalance(balance)
        self.consumers = [Consumer(i, nameList[i], preference=[0 for j in range(sellerNum)])
                          for i in range(consumerNum)]
        self.curConsumer = -1
        self.dailyCost = dailyCost
        self.dailyIncome = dailyIncome
        self.force = False

    def getCurrentConsumer(self):
        return self.consumers[self.curConsumer]

    def isLastConsumer(self):
        return self.curConsumer == self.consumerNum-1

    def getNextConsumer(self):
        self.curConsumer = (self.curConsumer+1) % self.consumerNum
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
        # newGameState = GameState(self.sellers.copy(),self.sellerNum, self.consumerNum, self.nameList, 0.0, self.dailyCost, self.dailyIncome)
        # newGameState.consumerNum = self.consumerNum
        # newGameState.sellerNum = self.sellerNum
        # newGameState.consumers = [Consumer(i, self.nameList[i], self.consumers[i].preference.copy()) for i in range(self.consumerNum)]
        # newGameState.curConsumer = self.curConsumer
        # newGameState.dailyCost = self.dailyCost
        # newGameState.dailyIncome = self.dailyIncome
        return deepcopy(self)

    def getNextState(self, agentIndex: int, choice: int):
        '''
        Returns the next GameState if the agent choose choice.
        agentIndex: the index of the agent who is going to choose
        choice: the choice of the agent
        return: the next GameState
        '''
        newGameState = self.copy()
        consumer = newGameState.getCurrentConsumer()
        if not self.force:
            eatIdx = consumer.decide(agentIndex, choice)
            if eatIdx != agentIndex:
                newGameState.force = True
                return newGameState
        else:
            eatIdx = agentIndex
            newGameState.force = False

        # if eatIdx != agentIndex:
        #     sellerAgent = self.sellers[eatIdx]
        #     choice = sellerAgent.getChoice(newGameState) if eatIdx != 0 else SellerChoices.SUPERLOW
        #     newGameState.updateConsumer(eatIdx, choice)

        newGameState.updateSeller(eatIdx, choice)
        if self.isLastConsumer():
            newGameState.updateDaily()
        return newGameState

    def updateDaily(self):
        for seller in self.sellers:
            seller.loseMoney(self.dailyCost)
            seller.getMoney(self.dailyIncome)
        for consumer in self.consumers:
            consumer.preference = [i*0.9 for i in consumer.preference]

    def updateConsumer(self, sellerIdx: int, choice: int):
        self.getCurrentConsumer().preferenceUpdate(sellerIdx, choice)

    def updateSeller(self, eatIndex: int, choice: int):
        '''
        Update the state of the game.
        eatIndex: the index of the seller who is going to be eaten
        choice: the choice of the seller
        return: None
        '''

        self.sellers[eatIndex].getPaid(choice)


class Game:
    def __init__(self, agents: List[Agent], consumerNum, nameList, balance, dailyCost, dailyIncome, maxDay=100):
        self.agents: List[Agent] = agents
        self.sellerNum = len(agents)
        self.consumerNum = consumerNum
        self.nameList = nameList
        self.balance = balance
        self.dailyCost = dailyCost
        self.dailyIncome = dailyIncome
        self.maxDay = maxDay

        self.gameOver = False
        self.record = []
        # self.record={"day":[],"score":[],"balance":[],"consumerVisit":[],"agentChoice":[],"consumerPreference":[]}
        # self.agentTimeout = False
        # import io
        # self.agentOutput = [io.StringIO() for agent in agents]

    def showRecord(self):
        print("----Game Start----")
        for day in range(len(self.record)):
            dayRecord = self.record[day]
            print(f"----Day {day+1} start----")
            for consumerRecord in dayRecord[0:-1]:
                print(f"Consumer {consumerRecord['comsumerName']} visit seller {consumerRecord['consumerVisit']}")
                print(f"Seller {consumerRecord['consumerVisit']} choose price {consumerRecord['sellerChoice'][0]}")
                if(consumerRecord['consumerChoice'] != consumerRecord['consumerVisit']):
                    print("Comsumer is not satisfied with the price")
                    print(
                        f"Consumer {consumerRecord['comsumerName']} decide to eat at seller {consumerRecord['consumerChoice']}")
                    print(f"Seller {consumerRecord['consumerChoice']} choose price {consumerRecord['sellerChoice'][1]}")
                else:
                    print("Comsumer is satisfied with the price")
                print(f"Consumer {consumerRecord['comsumerName']} preference {consumerRecord['consumerPreference']}")
                print(f"Seller {consumerRecord['consumerChoice']} balance {consumerRecord['sellerBalance']}")
                print(f"------------------")
            print("Current game state:")
            for consumer in dayRecord[-1]["consumer"]:
                print(f"Consumer {consumer['name']} preference {consumer['preference']}")
            for seller in dayRecord[-1]["seller"]:
                print(f"Seller {seller['name']} balance {seller['balance']}")
            print(f"----Day {day+1} End----")
        print(f"----Game Over----")
        print(f"Player score: {dayRecord[-1]['seller'][0]['balance']}")

    def run(self):
        '''
        Main control loop for game play.
        '''
        self.state = GameState(self.agents, self.sellerNum, self.consumerNum, self.nameList,
                               self.balance, self.dailyCost, self.dailyIncome)
        day = 0
        while not self.gameOver and day < self.maxDay:
            day += 1
            # print(f"----Day {day} start----")
            self.record.append([])
            # Fetch the next game state
            while True:
                consumer = self.state.getNextConsumer()
                self.record[-1].append({"comsumerName": consumer.name})
                # consumuer randomly choose one at first in each day
                sellerIdx = consumer.chooseSeller(self.state.sellerNum)
                # print(f"Consumer {consumer.name} visit seller {sellerIdx}" )
                self.record[-1][-1]["consumerVisit"] = sellerIdx
                sellerAgent = self.agents[sellerIdx]
                # The seller give his choice(price)
                sellerChoice = sellerAgent.getChoice(self.state)
                # print(f"Seller {sellerIdx} choose price {sellerChoice}")
                self.record[-1][-1]["sellerChoice"] = [sellerChoice]
                # Consumer give his decision
                eatIdx = consumer.decide(sellerIdx, sellerChoice)
                # print(f"consumer's preference: {consumer.preference}")
                # print(f"Consumer {consumer.name} decide to eat at seller {eatIdx}")
                self.record[-1][-1]["consumerChoice"] = eatIdx
                if eatIdx != sellerIdx:
                    sellerAgent = self.agents[eatIdx]
                    sellerChoice = sellerAgent.getChoice(self.state)
                    # print(f"Seller {eatIdx} choose price {sellerChoice}")
                    consumer.preferenceUpdate(eatIdx, sellerChoice)
                    self.record[-1][-1]["sellerChoice"].append(sellerChoice)

                self.state.updateSeller(eatIdx, sellerChoice)
                # print(f"consumer {consumer.name} preference:{consumer.preference}")
                self.record[-1][-1]["consumerPreference"] = consumer.preference.copy()
                # print(f"seller {sellerIdx} balance: {self.agents[sellerIdx].getBalance()}")
                self.record[-1][-1]["sellerBalance"] = self.agents[eatIdx].getBalance()
                self.gameOver = self.state.isWin() or self.state.isLose()
                # print(f"------------------")
                if self.state.isLastConsumer() or self.gameOver:
                    break
            self.state.updateDaily()
            self.gameOver = self.state.isWin() or self.state.isLose()
            # print(f"Current game state:")
            self.record[-1].append({})
            self.record[-1][-1]["consumer"] = []
            for consumer in self.state.consumers:
                # print(f"Consumer {consumer.name} preference: {consumer.preference}")
                self.record[-1][-1]["consumer"].append({"name": consumer.name,
                                                       "preference": consumer.preference.copy()})
            self.record[-1][-1]["seller"] = []
            for seller in self.agents:
                # print(f"Seller {seller.index} balance: {seller.getBalance()}")
                self.record[-1][-1]["seller"].append({"name": seller.index, "balance": seller.getBalance()})
        self.playerScore = self.agents[0].getBalance()
        scores = [agent.getBalance() for agent in self.agents]
        print(f"Final scores: {scores}, end day: {day}")
        self.isWin = self.state.isWin() if self.gameOver else argmax(scores) == 0
        # print(f"----Day {day} End----")
        # print(f"----Game Over----")

        return self.state
