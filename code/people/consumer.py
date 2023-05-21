import random
from .seller import Seller, SellerChoices
from utils import flipCoin
import numpy as np
from typing import List


class Consumer:
    def __init__(self, index: int, name: str, preference: List[int] = None):
        """
        index: the index of the consumer
        name: the name of the consumer
        preference: the preference of the consumer. -1: no preference, 0: prefer seller 0, 1: prefer seller 1, etc.
        """
        self.index: int = index
        self.name: str = name
        self.preference: List[int] = preference
        # self.belief: float = SellerChoices.MEDIUM

    def __str__(self):
        return f"Consumer {self.index} {self.name} {self.preference}"

    def isPrefer(self, seller: int) -> bool:
        """
        seller: the id of seller asking
        return: if the seller is the one that the consumer has the highest preference
        """
        return np.argmax(self.preference) == seller

    def hasPreference(self) -> bool:
        # if not all value in preference list is -1, then has preference
        return not all([x == 0 for x in self.preference])

    def getPreference(self) -> int:
        return np.argmax(self.preference)

    def preferenceUpdate(self, seller: int, price: int):
        """
        update the preference of the consumer
        """
        # self.belief = 0.9 * self.belief + 0.1 * price
        self.preference[seller] += SellerChoices.MEDIUM - price

    def chooseSeller(self, n: int) -> int:
        """
        n: the number of sellers
        return: the id of seller chosen(randomly)
        """
        return random.randint(0, n - 1)

    def decide(self, index: int, sellerChoice: int):
        """
        eat the food
        index: the index of the seller
        choice: the choice of the price of the food that seller offers
        return: the index of the seller chosen to eat
        """
        # TODO: What if there are multiple sellers?
        # if sellerChoice == SellerChoices.NONE:
        #     print(f"{self.name} is eating in restaurant {index} with superlow price")
        #     return None

        eatIdx = None
        if self.hasPreference():  # has preference
            if self.isPrefer(index):
                eatIdx = index
            else:
                if sellerChoice == SellerChoices.HIGH:
                    eatIdx = self.getPreference()
                elif sellerChoice == SellerChoices.MEDIUM:
                    eatIdx = self.getPreference()
                elif sellerChoice == SellerChoices.LOW:
                    eatIdx = index
                elif sellerChoice == SellerChoices.SUPERLOW:
                    eatIdx = index
        else:  # no preference
            # eat here, but with preference changed
            eatIdx = index

        # else:  # no preference
        #     # Multiple sellers
        #     eatIdx = index
        #     if choice == SellerChoices.MEDIUM:
        #         self.preference = index if flipCoin(0.5) else -1
        #     elif choice == SellerChoices.LOW or choice == SellerChoices.SUPERLOW:
        #         self.preference = index

        # print(f"{self.name} is eating in restaurant {eatIdx} with superlow price")
        self.preferenceUpdate(index, sellerChoice)
        return eatIdx
