from game import SellerChoices
import random
import utils
from .sellerAgent import SellerAgent

from .baseAgent import Agent
from .learningAgent import ReinforcementAgent


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

# def contestEvaluationFunction(currentGameState):
#     from math import sqrt

#     if currentGameState.isLose():
#         return -999999
#     if currentGameState.isWin():
#         return 999999

#     pacmanPos = currentGameState.getPacmanPosition()
#     foodList = currentGameState.getFood().asList()
#     GhostStates = currentGameState.getGhostStates()
#     ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

#     if currentGameState.hasWall(*pacmanPos):
#         return -999999

#     # minGhostsDist = min([manhattanDistance(pacmanPos, ghostDist)
#     #                      for ghostDist in currentGameState.getGhostPositions()])
#     # if minGhostsDist < 2:
#     #     return -999999

#     scaredList = []
#     notScaredList = []
#     for ghost in currentGameState.getGhostStates():
#         if ghost.scaredTimer:
#             scaredList.append(ghost)
#         else:
#             notScaredList.append(ghost)
#     minNotScaredDist = min([manhattanDistance(pacmanPos, ghost.getPosition())
#                             for ghost in notScaredList]) if notScaredList else 999999
#     avgNotScaredDist = sum([manhattanDistance(pacmanPos, ghost.getPosition())
#                             for ghost in notScaredList]) / len(notScaredList) if notScaredList else 999999
#     minScaredDist = min([manhattanDistance(pacmanPos, ghost.getPosition())
#                         for ghost in scaredList]) if scaredList else 0

#     foodDist = [manhattanDistance(pacmanPos, food) for food in foodList]
#     if not foodDist:
#         return 999999
#     minFoodDist = min(foodDist)
#     maxFoodDist = max(foodDist)

#     capsulesNum = len(currentGameState.getCapsules())
#     foodNum = len(foodList)
#     score = currentGameState.getScore()

#     # if minNotScaredDist == 0:
#     #     return -999999

#     # return -200 * capsulesNum - 40 * foodNum + 5 * score - 2 * minFoodDist + 3*sqrt(maxFoodDist) - 2 * minScaredDist - 20.0 / minNotScaredDist - 2.0 / avgNotScaredDist
#     return -200 * capsulesNum - 50 * foodNum + 5 * score - 1.8 * minFoodDist + 3*sqrt(maxFoodDist) - 2 * minScaredDist - 2.0 / max(10, minNotScaredDist)


class ExpectimaxAgent(Agent):
    """
        Your agent for the mini-contest
    """

    def __init__(self, evalFn='contestEvaluationFunction', depth='3'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = utils.lookup(evalFn, globals())
        self.depth = int(depth)

    def getChoice(self, gameState):
        def max_value(gameState, depth, agentIndex):
            v = -999999
            for choice in gameState.getLegalChoices(agentIndex):
                v = max(v, minimax(gameState.getNextState(
                    agentIndex, choice), depth, agentIndex + 1))
            return v

        def exp_value(gameState, depth, agentIndex):
            v = 0
            sellerB = SellerAgent.RandomSeller(agentIndex)
            choiceDistribution = sellerB.getDistribution(gameState)

            for choice, weight in choiceDistribution.items():
                if agentIndex == gameState.getNumAgents() - 1:
                    v += minimax(gameState.getNextState(agentIndex, choice), depth - 1, 0) * weight
                else:
                    v += minimax(gameState.getNextState(agentIndex, choice), depth, agentIndex + 1) * weight
            return v

        def minimax(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            if agentIndex == 0:
                return max_value(gameState, depth, agentIndex)
            else:
                return exp_value(gameState, depth, agentIndex)

        v = -999999
        bestChoice = None
        for choice in gameState.getLegalChoices(0):
            minMaxVal = minimax(gameState.getNextState(0, choice), self.depth, 1)
            if v < minMaxVal:
                v = minMaxVal
                bestChoice = choice
        return bestChoice if bestChoice else SellerChoices.NONE


class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """

    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        self.QValues = utils.Counter()  # A Counter is a dict with default 0

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        # return 0.0 if we have never seen a state
        return self.QValues[(state, action)] if (state, action) in self.QValues else 0.0

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        maxQValue = float("-inf")
        for action in self.getLegalActions(state):
            maxQValue = max(maxQValue, self.getQValue(state, action))
        return maxQValue if maxQValue != float("-inf") else 0.0

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        maxQValue = float("-inf")
        bestAction = None
        for action in self.getLegalActions(state):
            if self.getQValue(state, action) > maxQValue:
                maxQValue = self.getQValue(state, action)
                bestAction = action
        return bestAction if bestAction is not None else None

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use utils.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        # if there are no legal actions, which is the case at the terminal state, you should choose None as the action.
        if len(legalActions) == 0:
            return None
        # With probability self.epsilon, we should take a random action and take the best policy action otherwise.
        if utils.flipCoin(self.epsilon):
            action = random.choice(legalActions)
        else:
            action = self.getPolicy(state)
        # print("action: ", action)

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        nextQValue = self.computeValueFromQValues(nextState)
        # Q(s,a) = (1-alpha)*Q(s,a) + alpha*(r + gamma*maxQ(s',a'))
        self.QValues[(state, action)] = (1 - self.alpha) * self.getQValue(state, action) + self.alpha * (
            reward + self.discount * nextQValue)
        # print("QValues: ", self.QValues[(state, action)])

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class SellerQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)
        return action


class ApproximateQAgent(SellerQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """

    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = utils.lookup(extractor, globals())()
        SellerQAgent.__init__(self, **args)
        self.weights = utils.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        # Q(s,a) = w * featureVector
        featureVector = self.featExtractor.getFeatures(state, action)
        QValue = 0
        for feature in featureVector:
            QValue += self.weights[feature] * featureVector[feature]
        # print("QValue: ", QValue)
        return QValue

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        nextQValue = self.computeValueFromQValues(nextState)
        # Q(s,a) = (1-alpha)*Q(s,a) + alpha*(r + gamma*maxQ(s',a'))
        difference = (reward + self.discount * nextQValue) - self.getQValue(state, action)
        featureVector = self.featExtractor.getFeatures(state, action)
        for feature in featureVector:
            self.weights[feature] += self.alpha * difference * featureVector[feature]
        # print("weights: ", self.weights[feature])

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        SellerQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            pass
        # print("weights: ", self.weights)
        # print("features: ", self.featExtractor.getFeatures(state, 'Stop'))
        for feature in self.featExtractor.getFeatures(state, 'Stop'):
            print(f"{feature:35s}: weight:\t{self.weights[feature]:.8f}, \t \
                |\tfeature: \t{self.featExtractor.getFeatures(state, 'Stop')[feature]:.8f}")
        print()
