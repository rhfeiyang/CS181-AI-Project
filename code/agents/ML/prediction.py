import numpy as np
from copy import deepcopy
import agents.ML.nn as nn
import agents 
import people
from people.seller import SellerChoices


class neuralNetworkPredictionModel():
        def __init__(self, consumerNum, sellerNum, sellerId):
                self.consumerNum = consumerNum
                self.sellerId = sellerId
                                
                self.w0 = nn.Parameter(sellerNum + 1,50)
                self.b0 = nn.Parameter(1,50)

                self.w1 = nn.Parameter(50,50)
                self.b1 = nn.Parameter(1,50)

                self.w2 = nn.Parameter(50,5)
                self.b2 = nn.Parameter(1,5)

                self.learningRate = -0.05
                self.loss:nn.Node = None
                self.trained = False

                self.data = []
                self.labels = []

        def run(self, x) -> nn.Node:
                # example
                # y = nn.ReLU(nn.AddBias(nn.Linear(x, self.w0), self.b0))
                # y = nn.ReLU(nn.AddBias(nn.Linear(y, self.w1), self.b1))
                # y = nn.ReLU(nn.AddBias(nn.Linear(y, self.w2), self.b2))
                # y = nn.AddBias(nn.Linear(y, self.w3), self.b3)
                x = np.array(x)
                x = nn.Constant(x)
                y = nn.ReLU(nn.AddBias(nn.Linear(x, self.w0), self.b0))
                y = nn.ReLU(nn.AddBias(nn.Linear(y, self.w1), self.b1))
                y = nn.AddBias(nn.Linear(y, self.w2), self.b2)
                return y

        def get_loss(self,x,y):
                # convert x,y to nn.Node. y is label. Please use Constant
                x = np.array(x)
                y = np.array(y)
                x = nn.Constant(x)
                y = nn.Constant(y)
                y_hat = self.run(x)
                self.loss = nn.SoftmaxLoss(y_hat, y)
                # debug("get_loss loss")
                return self.loss
        
        def train(self):
                iter = 0
                while True:
                        iter += 1
                        sum = 0
                        for id,x in enumerate(self.data):
                                y = self.labels[id]
                                self.loss = self.get_loss(x,y)
                                nn.gradients(self.loss,[self.w0,self.b0,self.w1,self.b1,self.w2,self.b2])
                                self.w0.update(self.learningRate)
                                self.b0.update(self.learningRate)
                                self.w1.update(self.learningRate)
                                self.b1.update(self.learningRate)
                                self.w2.update(self.learningRate)
                                self.b2.update(self.learningRate)
                        # enumerate over all data, if loss is small enough, break
                        for id,x in enumerate(self.data):
                                y = self.labels[id]
                                self.loss = self.get_loss(x,y)
                                sum += self.loss.value
                        if sum < 0.01 * len(self.data) or iter > 200:
                                break
                # debug("train loss")

        def predict(self, x) -> SellerChoices:
                if len(self.data) % 20 == 0 and len(self.data):
                        if not self.trained:
                                self.train()
                        self.trained = True
                else:
                        self.trained = False
                y_hat = self.run(x)
                # return the index of the max value
                arg = np.argmax(y_hat.data)
                if arg == 0:
                        return SellerChoices.HIGH
                elif arg == 1:
                        return SellerChoices.MEDIUM
                elif arg == 2:
                        return SellerChoices.LOW
                elif arg == 3:
                        return SellerChoices.SUPERLOW
                

        def addData(self, consumer:people.Consumer, choice:SellerChoices) -> None:
                # translate choice to label
                # class SellerChoices:
                #         HIGH = 12
                #         MEDIUM = 10
                #         LOW = 8
                #         SUPERLOW = 6
                data = np.array(consumer.getPreference())
                label = np.zeros(5)
                if choice == SellerChoices.HIGH:
                        label[0] = 1
                elif choice == SellerChoices.MEDIUM:
                        label[1] = 1
                elif choice == SellerChoices.LOW:
                        label[2] = 1
                elif choice == SellerChoices.SUPERLOW:
                        label[3] = 1
                else:
                        label[4] = 1
                self.data.append(data)
                self.labels.append(label)