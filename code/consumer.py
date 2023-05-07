import random
from seller import Seller, SellerChoices
from utils import flipCoin


class Consumer:
    def __init__(self, index: int, name: str, preference: int):
        """
        index: the index of the consumer
        name: the name of the consumer
        preference: the preference of the consumer. -1: no preference, 0: prefer seller 0, 1: prefer seller 1, etc.
        """
        self.index: int = index
        self.name: str = name
        self.preference: int = preference

    def __str__(self):
        return f"Consumer {self.index} {self.name} {self.preference}"

    def isPrefer(self, seller: int) -> bool:
        """
        seller: the id of seller asking
        return: True: willing to pay, False: not willing to pay
        """
        return seller == self.preference

    def getPreference(self) -> int:
        return self.preference

    def chooseSeller(self, n: int) -> int:
        """
        go around restaurants and choose the one with the lowest price
        n: the number of sellers
        return: the id of seller chosen
        """

        return random.randint(0, n-1)

    def eat(self, index: int, choice: SellerChoices):
        """
        eat the food
        index: the index of the seller
        choice: the choice of the price of the food that seller offers
        return: the index of the seller chosen to eat
        """
        if choice == SellerChoices.SUPERLOW:
            print(f"{self.name} is eating in restaurant {index} with superlow price")
            return None

        eatIdx = None
        if self.preference != -1:  # has preference
            if index == self.preference:
                eatIdx = index
            else:
                if choice == SellerChoices.HIGH:
                    eatIdx = self.preference
                elif choice == SellerChoices.MEDIUM:
                    eatIdx = self.preference
                elif choice == SellerChoices.LOW:
                    eatIdx = index
                elif choice == SellerChoices.SUPERLOW:
                    eatIdx = index
        else:  # no preference
            # Two sellers
            eatIdx = index
            if choice == SellerChoices.HIGH:
                self.preference = 0 if index == 1 else 1
            elif choice == SellerChoices.LOW or choice == SellerChoices.SUPERLOW:
                self.preference = index

        # else:  # no preference
        #     # Multiple sellers
        #     eatIdx = index
        #     if choice == SellerChoices.MEDIUM:
        #         self.preference = index if flipCoin(0.5) else -1
        #     elif choice == SellerChoices.LOW or choice == SellerChoices.SUPERLOW:
        #         self.preference = index

        print(f"{self.name} is eating in restaurant {eatIdx} with superlow price")
        return eatIdx
