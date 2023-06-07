from game import *
from agents import *
import random
import sys
from matplotlib import pyplot as plt
import numpy as np
import pickle
import argparse
RLanalysisPharse = [500,1000,2000,5000,10000, 13000, 15000, 20000, 25000, 30000 ,35000, 40000]
RLanalysisPharse = [i-1 for i in RLanalysisPharse]
def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--numTraining', type=int, default=0)
    parser.add_argument('--numGames', type=int, default=50)
    parser.add_argument('--record', type=bool, default=False)
    parser.add_argument('--weightFile', type=str, default=None)
    parser.add_argument('--agent', type=str, default=None, help='ExpectimaxAgent, AlphaBetaAgent, SellerQAgent, ApproximateQAgent, MCQAgent, MCQApproximateQAgent, neuralPredictSeller, ManualAgent')
    parser.add_argument('--expType',type=str,required=False)
    parser.add_argument('--rival', type=str, default=None,nargs='+', help='GreedySellerHigh, GreedySellerLow, GreedySellerSuperLow, RandomSeller')
    parser.add_argument('--consumerName',type=str, default=['Tom', 'Jerry'],nargs='+')
    parser.add_argument('--saveFileName',type=str,default=None,required=False)
    parser.add_argument('--initBalance', type=int, default=20)
    parser.add_argument('--dailyCost', type=int, default=1)
    parser.add_argument('--dailyIncome', type=int, default=0)
    parser.add_argument('--maxDay', type=int, default=100)
    parser.add_argument('--highPrice', type=int, default=12)
    parser.add_argument('--mediumPrice', type=int, default=10)
    parser.add_argument('--lowPrice', type=int, default=8)
    parser.add_argument('--superLowPrice', type=int, default=6)

    # parser.add_argument('--consumerNum',type=int,default=None)
    args = parser.parse_args()
    SellerChoices.HIGH=args.highPrice
    SellerChoices.MEDIUM=args.mediumPrice
    SellerChoices.LOW=args.lowPrice
    SellerChoices.SUPERLOW=args.superLowPrice

    if args.agent == "ManualAgent":
        print("You are the manager of a restaurant. You need to make decisions to make the restaurant profitable.")
        print("You have 4 choices: HIGH, MEDIUM, LOW, SUPERLOW for each consumer coming to your restaurant.")
        print("Hight price will lead to high income but low customer satisfaction.")
        print("Low price will lead to low income but high customer satisfaction.")
        print("Meanwhile, you need to pay daily cost for the restaurant.")
        print("You have some rivals in the market. You need to make your restaurant more attractive than your rivals.")
        print("Try to get more income, prevent bankruptcy and beat your rivals!")
        print("Good luck!")
        input("Press Enter to start...")

    else:
        print("Train num:",args.numTraining)
        print("Game num:",args.numGames)
        print("Agent:", args.agent)
        print("ConsumerName:", len(args.consumerName))
        print("Rival:", args.rival)
        print("save file name:", args.saveFileName)
        print("init balance:", args.initBalance)
        print("daily cost:", args.dailyCost)
        print("daily income:", args.dailyIncome)
        print("max day:", args.maxDay)
        print("high price:", args.highPrice)
        print("medium price:", args.mediumPrice)
        print("low price:", args.lowPrice)
        print("super low price:", args.superLowPrice)

    return args

def midTest(player,rivals,args):
    testGames = []
    if isinstance(player, QLearningAgent):
        player.switchTrain()
    for testid in range(100):
        game = Game([player] + rivals,
                    consumerNum=len(args.consumerName), nameList=args.consumerName,
                    balance=args.initBalance, dailyCost=args.dailyCost,
                    dailyIncome=args.dailyIncome, maxDay=args.maxDay)
        game.run(test=True)
        testGames.append(game)

    scores = [game.playerScore for game in testGames]
    rivalScore=[game.rivalScore for game in testGames]
    wins = [game.isWin for game in testGames]
    winRate = wins.count(True) / float(len(wins))
    if isinstance(player, QLearningAgent):
        player.switchTrain()
    return winRate,np.average(scores),np.average(rivalScore)

def runGames(player: Agent, rivals: List[Agent], numGames: int, consumerNameList: List[str], record: bool, numTraining=0, weightFile=None ,args=None):
    games = []
    if weightFile:
        try:
            player.loadWeights(weightFile)
        except:
            print("No weight file found")

    saveFileName="test"
    if args is not None:
        if args.saveFileName is not None:
            saveFileName=args.saveFileName
        else:
            saveFileName=f"{args.agent}_{args.rival}"

    for i in range(numGames):
        beQuiet = i < numTraining
        if beQuiet:
            # Suppress output and graphics
            # import textDisplay
            # gameDisplay = textDisplay.NullGraphics()
            # rules.quiet = True
            pass
        else:
            # gameDisplay = display
            # rules.quiet = False
            pass
        # game = rules.newGame(layout, pacman, ghosts,
        #                      gameDisplay, beQuiet, catchExceptions)

        # consumerNameList = ['Tom', 'Jerry', 'a', 'b', 'c', 'd', 'e']
        consumerNum = len(consumerNameList)

        if i in RLanalysisPharse and isinstance(player, QLearningAgent):
            player.addAnalysisData((i+1,midTest(player,rivals,args)))
            if i==RLanalysisPharse[-1]:
                player.plotAnalysis(rivalName=rivals[0].__class__.__name__)
                player.episodesSoFar+=1

        game = Game([player]+rivals,
                    consumerNum=consumerNum, nameList=consumerNameList,
                    balance=args.initBalance, dailyCost=args.dailyCost,
                    dailyIncome=args.dailyIncome, maxDay=args.maxDay)
        game.run()
        if not beQuiet:
            games.append(game)

        if record:
            # import time
            # import pickle
            # fname = ('recorded-game-%d' % (i + 1)) + \
            #     '-'.join([str(t) for t in time.localtime()[1:6]])
            # with open(fname, 'w') as f:
            #     components = {'layout': layout, 'actions': game.moveHistory}
            #     pickle.dump(components, f)
            game.showRecord()
        if i % 50000==0 and i>0:
            if "QValues" in dir(player):
                with open(saveFileName+'_'+str(i)+'.pickle', 'wb') as file:
                    pickle.dump(player.QValues, file)
            if "weights" in dir(player):
                with open(saveFileName+'_'+str(i)+'.pickle', 'wb') as file:
                    pickle.dump(player.weights, file)

    if (numGames-numTraining) > 0:
        scores = [game.playerScore for game in games]
        wins = [game.isWin for game in games]
        winRate = wins.count(True) / float(len(wins))
        print('Average Score:', sum(scores) / float(len(scores)))
        print('Scores:       ', ', '.join([str(score) for score in scores]))
        print('Win Rate:      %d/%d (%.2f)' %
              (wins.count(True), len(wins), winRate))
        print('Record:       ', ', '.join(
            [['Loss', 'Win'][int(w)] for w in wins]))


    if numTraining>0:
        if "QValues" in dir(player):
            with open(saveFileName+'_'+str(numTraining)+'.pickle', 'wb') as file:
                pickle.dump(player.QValues, file)
        if "weights" in dir(player):
            with open(saveFileName+'_'+str(numTraining)+'.pickle', 'wb') as file:
                pickle.dump(player.weights, file)

    return games


def plot(games: Game = None):
    def getSellerAgentName(agent: Agent):
        if isinstance(agent, ExpectimaxAgent):
            return 'ExpectimaxAgent'
        elif isinstance(agent, AlphaBetaAgent):
            return 'AlphaBetaAgent'
        elif isinstance(agent, RandomSeller):
            return 'RandomSeller'
        # elif isinstance(agent, neuralPredictSeller):
        #     return 'neuralPredictSeller'
        elif isinstance(agent, GreedySellerHigh):
            return 'GreedySellerHigh'
        elif isinstance(agent, GreedySellerLow):
            return 'GreedySellerLow'
        elif isinstance(agent, GreedySellerSuperLow):
            return 'GreedySellerSuperLow'
        return 'Unknown'

    if games != None:
        with open('game.pkl', 'wb') as f:
            pickle.dump(games, f)
    else:
        with open('game.pkl', 'rb') as f:
            games = pickle.load(f)

    sellerNum = games[0].sellerNum
    x = np.arange(1, games[0].maxDay+1)

    sellerBalance = np.zeros(shape=(sellerNum, games[0].maxDay))
    weight = np.zeros(shape=(sellerNum, games[0].maxDay))
    for game in games:
        record = game.record
        for i in range(sellerNum):
            for j in range(len(record)):
                sellerBalance[i][j] += record[j][-1]['seller'][i]['balance']
                weight[i][j] += 1
    sellerBalance /= weight

    plt.figure()
    for i in range(sellerNum):
        plt.plot(x, sellerBalance[i],
                 label=f'{getSellerAgentName(games[0].agents[i])}',
                 linestyle='-' if i == 0 else '--')

    plt.title(f'Average Balance of Different Seller Agents in {len(games)} Games')
    plt.xlabel('Day')
    plt.ylabel('Balance')
    plt.legend()
    plt.xlim(1, game.maxDay)
    # plt.show()
    plt.savefig('output.png')



def peopleGen(args):
    agent=args.agent
    player=peopleFind(agent)(numTraining=args.numTraining)


    rivals=[]
    for id,rival in enumerate(args.rival):
        rivals.append(peopleFind(rival)(id+1))

    # if args.consumerName is not None and args.consumerNum is None:
    #     args.consumerNum=len(args.consumerName)
    # if args.consumerName is not None and len(args.consumerName)!=args.consumerNum:
    #     raise Exception("Consumer number is not equal to number of consumerName")
    # if args.consumerName is None:
    #     consumer=[Consumer(i,None,None) for i in range(args.consumerNum)]
    # else:
    #     consumer=[Consumer(i,args.consumerName[i],None) for i in range(args.consumerNum)]

    return player,rivals


if __name__ == '__main__':
    """
    The main function called when main.py is run
    from the command line:

    > python main.py

    See the usage string for more details.

    > python main.py --help
    """
    # args = readCommand(sys.argv[1:])  # Get game components based on input
    # runGames(**args)
    random.seed('cs181')
    np.random.seed(181)
    args=parseargs()

    numTraining=args.numTraining
    numGames=args.numGames
    record=args.record
    weightFile=args.weightFile
    consumerNameList=args.consumerName
    player, rivals=peopleGen(args)

    # consumerNameList = ['Tom', 'Jerry']
    # player = ApproximateQAgent()
    # numTraining = 500000
    # player.numTraining = numTraining
    # rivals = [GreedySellerHigh(index=1)]

    # runGames(player, rivals, 5, record=True, numTraining=0)
    games = runGames(player, rivals, numTraining+numGames, consumerNameList, record=args.record,
                     numTraining=numTraining, weightFile=args.weightFile,args=args)
    # plot(games)
