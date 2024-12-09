deprecated: code used from GTPyhop to get started. Irrelevant to my project now.
Tables: folder containing tables I used in the paper (they are also in the paper)
TrialsLayout: folder with the environment for the experiment I ran with A* vs MCTS. bush_{value}.png, where value signifies the # of bushes in the environment
display.py: manual script for visualizing the Taxi environment
gtypyhop.py and test_harness.py: copied from GTPyhop
problem.ppdl and taxi.pddl: how I first visualized this problem
taxi_htn: MAIN CODE. 
- Creates environment
- Actions
- TOHTN methods
- Runs lazylookahead
- Naive, A*, MCTS algorithms
- Commands
- ManhattanDist heuristic
- Helper function
- main to run code