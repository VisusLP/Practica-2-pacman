# Tests the effectiveness of training just one time in labAA1, labAA2, labAA3, labAA4

# Resets the qtable
cp qtable-ini.txt qtable.txt &&
# Trains in the map labAA1, labAA2, labAA3, labAA4 for 1 game
python busters.py -p QLearningAgent -k 3 -l labAA1 -n 1 &&
python busters.py -p QLearningAgent -k 3 -l labAA2 -n 1 &&
python busters.py -p QLearningAgent -k 3 -l labAA3 -n 1 &&
python busters.py -p QLearningAgent -k 3 -l labAA4 -n 1 &&
# Sets epsilon and alpha to 0, and executes the 5 maps 10 times
python busters.py -p QLearningAgent -k 1 -l labAA1 -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -k 2 -l labAA2 -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -k 3 -l labAA3 -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -k 3 -l labAA4 -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -k 3 -l labAA5 -n 10 -r 0 -e 0 -q