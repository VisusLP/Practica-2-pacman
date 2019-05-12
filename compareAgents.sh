cp qtable-ini.txt qtable.txt &&

python busters.py -p QLearningAgent -k 1 -l labAA1 -n 10 -x 10 &&
python busters.py -p QLearningAgent -k 2 -l labAA2 -n 10 -x 10 &&
python busters.py -p QLearningAgent -k 3 -l labAA3 -n 10 -x 10 &&
python busters.py -p QLearningAgent -k 3 -l labAA4 -n 10 -x 10 &&
python busters.py -p QLearningAgent -k 3 -l labAA5 -n 10 -x 10 &&

python busters.py -p QLearningAgent -g RandomGhost -l newmap -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l oneHunt_noFood -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l 20Hunt -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l bigHunt -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l classic -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l mimapa -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l sixHunt -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l smallHunt -n 100 -r 0 -e 0 -q