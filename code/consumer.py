import random
from seller import Seller, SellerChoices


class Consumer:
    def __init__(self, index: int, name: str, preference: int):
        """
        index: the index of the consumer
        name: the name of the consumer
        preference: the preference of the consumer
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
        return: the id of seller chosen, the price seller given
        """

        # TODO: from sellers, choose the one with the lowest price

        return random.randint(0, n-1)
        # raise NotImplementedError

    def eat(self, index: int, choice: SellerChoices):
        """
        eat the food
        price: the price of the food
        return: the index of the seller chosen to eat in
        """
        eatIdx = None
        if choice == SellerChoices.HIGH:
            eatIdx = index
            print(f"{self.name} is eating in restaurant {eatIdx} with high price")
        elif choice == SellerChoices.MEDIUM:
            eatIdx = index
            print(f"{self.name} is eating in restaurant {eatIdx} with medium price")
        elif choice == SellerChoices.LOW:
            eatIdx = self.preference
            print(f"{self.name} is eating in restaurant {eatIdx} with low price")
        elif choice == SellerChoices.SUPERLOW:
            eatIdx = self.preference
            print(f"{self.name} is eating in restaurant {eatIdx} with superlow price")
        else:
            print(f"error: {self.name} is eating in restaurant {index} with unknown price")
        return eatIdx
