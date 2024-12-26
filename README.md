Brief Overview: The purpose of this project is to determine the effectiveness of A* and MCTS algorithms for the planning phase in a partially observable taxi environment. Using GTPyhop (https://github.com/dananau/GTPyhop), I was able to run Lazy-Lookahead for the acting phase. There is also a PDF with my report for this experiment.<br />
deprecated: code used from GTPyhop to get started. Irrelevant to my project now.<br />
Tables: folder containing tables I used in the paper (they are also in the paper)<br />
TrialsLayout: folder with the environment for the experiment I ran with A* vs MCTS. bush_{value}.png, where value signifies the # of bushes in the environment<br />
display.py: manual script for visualizing the Taxi environment<br />
gtypyhop.py and test_harness.py: copied from GTPyhop<br />
problem.ppdl and taxi.pddl: how I first visualized this problem<br />
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