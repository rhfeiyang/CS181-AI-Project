This is a course project of CS181 of ShanghaiTech University. 

## Usage

To run our application, please switch to branch `master`. The `main` branch is our proposal and slides. 

## requirements


requirement files are at code/requirements.txt.



## Usage 

```
git switch master
cd ./code
pip install -r requirements.txt 
python main.py --numTraining 40000 --numGames 100 --agent MCQApproximateQAgent --rival GreedySellerHigh --initBalance 20 --consumerName Tom Jerry
```

it works well with `Python 3.11.3`

Arguments

- numTraining
- numGames
- record
- weightFile
- agent
- expType
- rival
- consumerName
- saveFileName
- initBalance
- dailyCost
- dailyIncome
- maxDay
- highPrice
- mediumPrice
- lowPrice
- superLowPrice


## For neural network (perceptron) usage

```
git switch nn_predict
cd ./code
python ./main.py 1
```

To use multithread testing, 

```
git switch nn_predict
cd ./code
chmod +x excute.sh
./excute.sh
```

switch back to master if you need.
