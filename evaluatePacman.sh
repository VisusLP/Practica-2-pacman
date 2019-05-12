cp qtable-ini.txt qtable.txt &&

python busters.py -p QLearningAgent -k 1 -l labAA1 -n 10 -x 10 &&
python busters.py -p QLearningAgent -k 2 -l labAA2 -n 10 -x 10 &&
python busters.py -p QLearningAgent -k 3 -l labAA3 -n 10 -x 10 &&
python busters.py -p QLearningAgent -k 3 -l labAA4 -n 10 -x 10 &&
python busters.py -p QLearningAgent -k 3 -l labAA5 -n 10 -x 10 &&

python busters.py -p QLearningAgent -l newmap -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -l oneHunt -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -l openClassic -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -l openHunt -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -l originalClassic -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -l 20Hunt -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -l bigHunt -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -l capsuleClassic -n 10 -r 0 -e 0 -q && 
python busters.py -p QLearningAgent -l classic -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -l contestClassic -n 10 -r 0 -e 0 -q && 
python busters.py -p QLearningAgent -l mediumClassic -n 10 -r 0 -e 0 -q && 
python busters.py -p QLearningAgent -l mimapa -n 10 -r 0 -e 0 -q && 
python busters.py -p QLearningAgent -l sixHunt -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -l smallClassic -n 10 -r 0 -e 0 -q && 
python busters.py -p QLearningAgent -l smallHunt -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -l testClassic -n 10 -r 0 -e 0 -q &&
python busters.py -p QLearningAgent -l trappedClassic -n 10 -r 0 -e 0 -q && 
python busters.py -p QLearningAgent -l trickyClassic -n 10 -r 0 -e 0 -q 