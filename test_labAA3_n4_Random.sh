# Tests the effectiveness of training just one time in labAA3

# Resets the qtable
cp qtable-ini.txt qtable.txt &&
# Trains in the map labAA3 for 4 game
python busters.py -p QLearningAgent -k 3 -l labAA3 -n 4 -g RandomGhost &&
# Sets epsilon and alpha to 0, and executes the 5 maps 10 times
python busters.py -p QLearningAgent -k 1 -l labAA1 -n 10 -r 0 -e 0 -q -g RandomGhost &&
python busters.py -p QLearningAgent -k 2 -l labAA2 -n 10 -r 0 -e 0 -q -g RandomGhost &&
python busters.py -p QLearningAgent -k 3 -l labAA3 -n 10 -r 0 -e 0 -q -g RandomGhost &&
python busters.py -p QLearningAgent -k 3 -l labAA4 -n 10 -r 0 -e 0 -q -g RandomGhost &&
python busters.py -p QLearningAgent -k 3 -l labAA5 -n 10 -r 0 -e 0 -q -g RandomGhost