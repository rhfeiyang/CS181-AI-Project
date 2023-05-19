import utils
from ..learningAgent import ReinforcementAgent
import random

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
        - self.getLegalChoices(state)
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
        if len(self.getLegalChoices(self.index))==0:
            return 0.0

        return max([self.getQValue(state,action) for action in self.getLegalChoices(state)])

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        if len(state.getLegalChoices(self.index))==0:
            return None
        q_values = utils.Counter()

        for action in state.getLegalChoices(state):
            q_values[action] = self.getQValue(state, action)

        return q_values.argMax()

    def getChoice(self, state):
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
        legalActions = state.getLegalChoices(self.index)
        action = None
        "*** YOUR CODE HERE ***"
        if utils.flipCoin(self.epsilon):
            return random.choice(legalActions)
        else:
            return self.getPolicy(state)

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        self.values[(state,action)]= \
            (1-self.alpha)*self.getQValue(state,action)+self.alpha*(reward+self.discount*self.getValue(nextState))

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

    def __init__(self, weights=None, **args):
        self.featExtractor = Extractor()
        SellerQAgent.__init__(self, **args)
        if weights is None:
            self.weights = utils.Counter()
        else:
            self.weights=weights

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

class Extractor:
    def getFeatures(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        # raise NotImplemented
        features = utils.Counter()
        features["bias"] = 1.0
        features["balance"] = state.getScore()/50
        features["dailyCost"]=state.dailyCost/20
        features["dailyIncome"]=state.dailyIncome/10
        for i in range(state.consumerNum):
            for j in range(state.sellerNum):
                features[f"consumer{i}_{j}"]=state.consumers[i].preference[j]/10
        features["liveAgents"]=state.getLiveAgents()/state.sellerNum
        features.divideAll(10.0)
        return features













