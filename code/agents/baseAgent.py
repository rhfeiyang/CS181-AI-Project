from people import Seller
import utils
class Agent(Seller):
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """

    def __init__(self, index=0):
        super().__init__(self,index)

    def getAction(self, state):
        utils.raiseNotDefined()

    def getBalance(self) -> float:
        return self._balance