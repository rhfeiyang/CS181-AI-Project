
class SellerChoices:
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'
    SUPERLOW = 'superlow'
    NONE = 'none'


class Seller:
    def __init__(self, index: int, balance: float, benefitRule={SellerChoices.HIGH: 1.0,
                                                                SellerChoices.MEDIUM: 0.0,
                                                                SellerChoices.LOW: -1.0,
                                                                SellerChoices.SUPERLOW: -2.0}
                 ):
        '''
        balance: at the start, all the sellers have the same balance(property)
        when balance<0, the seller go bankrupt
        '''
        self.index = index
        self.balance = balance
        self.benefitRule = benefitRule

    def isLive(self) -> bool:
        return self.balance > 0

    def getBalance(self) -> float:
        return self.balance

    def getIndex(self) -> int:
        return self.index

    def loseMoney(self, money: float):
        self.balance -= money

    def getMoney(self, price: float):
        self.balance += price

    def getPaid(self, choice: SellerChoices):
        self.balance += self.benefitRule[choice]
