# DISCLAIMER
# This is a huge script, it will take some time

cp qtable-ini.txt qtable.txt &&

python busters.py -p QLearningAgent -k 1 -l labAA1 -n 100 -x 100 &&
python busters.py -p QLearningAgent -k 2 -l labAA2 -n 100 -x 100 &&
python busters.py -p QLearningAgent -k 3 -l labAA3 -n 100 -x 100 &&
python busters.py -p QLearningAgent -k 3 -l labAA4 -n 100 -x 100 &&
python busters.py -p QLearningAgent -k 3 -l labAA5 -n 100 -x 100 &&

python busters.py -p QLearningAgent -g RandomGhost -l newmap -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l oneHunt -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l openClassic -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l openHunt -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l originalClassic -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l 20Hunt -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l bigHunt -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l capsuleClassic -n 100 -r 0 -e 0 -q && 
python busters.py -p QLearningAgent -g RandomGhost -l classic -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l contestClassic -n 100 -r 0 -e 0 -q && 
python busters.py -p QLearningAgent -g RandomGhost -l mediumClassic -n 100 -r 0 -e 0 -q && 
python busters.py -p QLearningAgent -g RandomGhost -l mimapa -n 100 -r 0 -e 0 -q && 
python busters.py -p QLearningAgent -g RandomGhost -l sixHunt -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l smallClassic -n 100 -r 0 -e 0 -q && 
python busters.py -p QLearningAgent -g RandomGhost -l smallHunt -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l testClassic -n 100 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -g RandomGhost -l trappedClassic -n 100 -r 0 -e 0 -q && 
python busters.py -p QLearningAgent -g RandomGhost -l trickyClassic -n 100 -r 0 -e 0 -q 