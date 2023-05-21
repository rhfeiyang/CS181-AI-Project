from people import Seller
import utils


class Agent(Seller):
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """

    def __init__(self, index=0, balance=0):
        super().__init__(index, balance)

    def getAction(self, state):
        utils.raiseNotDefined()

    def getBalance(self) -> float:
        raise Exception("The balance data is stored in the state(seller), not in the agent")

