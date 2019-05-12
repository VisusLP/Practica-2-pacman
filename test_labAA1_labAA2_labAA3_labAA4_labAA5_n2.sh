# Tests the effectiveness of training just one time in labAA1, labAA2, labAA3, labAA4 and labAA5

# Resets the qtable
cp qtable-ini.txt qtable.txt &&
# Trains in the map labAA1, labAA2, labAA3, labAA4 and labAA5 for 2 game
python busters.py -p QLearningAgent -k 3 -l labAA1 -n 2 &&
python busters.py -p QLearningAgent -k 3 -l labAA2 -n 2 &&
python busters.py -p QLearningAgent -k 3 -l labAA3 -n 2 &&
python busters.py -p QLearningAgent -k 3 -l labAA4 -n 2 &&
python busters.py -p QLearningAgent -k 3 -l labAA4 -n 2 &&
# Sets epsilon and alpha to 0, and executes the 5 maps 10 times
python busters.py -p QLearningAgent -k 1 -l labAA1 -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -k 2 -l labAA2 -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -k 3 -l labAA3 -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -k 3 -l labAA4 -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -k 3 -l labAA5 -n 10 -r 0 -e 0 -q