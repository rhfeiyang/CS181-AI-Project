import utils


class SellerChoices:
    HIGH = 12
    MEDIUM = 10
    LOW = 8
    SUPERLOW = 6


class Seller:
    def __init__(self, index: int, balance: float=0, benefitRule={SellerChoices.HIGH: 1.0,
                                                                SellerChoices.MEDIUM: 0.0,
                                                                SellerChoices.LOW: -1.0,
                                                                SellerChoices.SUPERLOW: -2.0}
                 ):
        '''
        balance: at the start, all the sellers have the same balance(property)
        when balance<0, the seller go bankrupt
        '''
        self.index = index
        self._balance = balance
        # self.benefitRule = benefitRule

    def isLive(self) -> bool:
        return self._balance > 0

    def setBalance(self, balance: float):
        self._balance = balance

    def getScore(self) -> float:
        return self._balance
        # if(self.index == 0):
        #     return self._balance
        # else:
        #     raise Exception("Only the first seller can get the score")

    def getIndex(self) -> int:
        return self.index

    def loseMoney(self, money: float):
        self._balance -= money

    def getMoney(self, price: float):
        self._balance += price

    def getPaid(self, choice: int):
        # seller get the benefit: choice-cost (average)
        self._balance += (choice-SellerChoices.MEDIUM)

    def getAction(self, state):
        utils.raiseNotDefined()

    def getChoice(self, state):
        utils.raiseNotDefined()
