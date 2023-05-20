import people
from bayesNet import Factor
import bayesNet

class bayesSellerOutcomeSpacer:
        def __init__(self,seller:people.Seller) -> None:                
                self.seller:people.Seller = seller
        def __hash__(self) -> int:
                return hash(f"Choice of {self.seller.getIndex()} spacer")
class bayesConsumerDomain:
        preferA = "prefer A"
        preferB = "prefer B"
        domain = [preferA,preferB]
class bayesSellerDomain:
        domain = [0,1,2]

class simpleFixedBayesNet:
        def __init__(self) -> None:
                pass
        def generateSingleStructureInstance(sellerList:list[people.Seller],consumerList:list[people.Consumer],currentSeller:people.Seller,currentConsumer:people.Consumer) -> bayesNet.BayesNet:
                outcomespacer = bayesSellerOutcomeSpacer(currentSeller)
                variables = set(sellerList) + set(consumerList) + set([outcomespacer])
                in_edges = {v:[] for v in variables}
                out_edges = {v:[] for v in variables}
                in_edges[currentSeller] = [currentConsumer,curstate]
                out_edges[currentConsumer].append(currentSeller)
                out_edges[outcomespacer].append(currentSeller)
                domains = {v:bayesConsumerDomain.domain for v in consumerList}
                domains = domains + {v:bayesSellerDomain.domain for v in sellerList}
                domains = domains + {outcomespacer:people.seller.SellerChoices}
                return bayesNet(variables,in_edges,out_edges,domains)
        
