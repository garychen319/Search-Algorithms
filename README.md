# Search-Algorithms
Implementation of BFS, DFS, A-Star Search, IDA-Star Search

Search algorithm to solve the n-puzzle game and compare the performance of each search algorithm (i.e. the 8-puzzle game generalized to an n × n array) (mypuzzle.org/sliding).

An instance of the n-puzzle game consists of a board holding n^2 − 1 distinct movable tiles, plus an empty space. The tiles are numbers from the set {1, ..., n^2 − 1}. For any such board, the empty space may be legally swapped with any tile horizontally or vertically adjacent to it. In this assignment, we will represent the blank space with the number 0.
Given an initial state of the board, the combinatorial search problem is to find a sequence of moves that transitions this state to the goal state; that is, the configuration with all tiles arranged in ascending order ⟨0, 1, ..., n^2 − 1⟩. The search space is the set of all possible states reachable from the initial state.
The blank space may be swapped with a component in one of the four directions {‘Up’, ‘Down’, ‘Left’, ‘Right’}, one move at a time. The cost of moving from one configuration of the board to another is the same and equal to one. Thus, the total cost of path is equal to the number of moves made from the initial state to the goal state.


Implementation:
• Breadth-First Search. Used an explicit queue
• Depth-First Search. Used an explicit stack
• A-Star Search. Used a priority queue. For the choice of heuristic, used the Manhattan priority function; that is, the sum of the distances of the tiles from their goal positions. Note that the blanks space is not considered an actual tile here.
• IDA-Star Search. As before, for the choice of heuristic, used the Manhattan priority function. Implementing the Iterative Deepening Search (IDS) algorithm involves first implementing the Depth-Limited Search (DLS) algorithm as a subroutine.

• Breadth-First Search. Enqueue in UDLR order; dequeuing results in UDLR order.
• Depth-First Search. Push onto the stack in reverse-UDLR order; popping off results in UDLR order.


Definition of Variables:
path_to_goal: the sequence of moves taken to reach the goal
cost_of_path: the number of moves taken to reach the goal
nodes_expanded: the number of nodes that have been expanded
fringe_size: the size of the frontier set when the goal node is found
max_fringe_size: the maximum size of the frontier set in the lifetime of the algorithm search_depth: the depth within the search tree when the goal node is found max_search_depth: the maximum depth of the search tree in the lifetime of the algorithm running_time: the total running time of the search instance, reported in seconds max_ram_usage: the maximum RAM usage in the lifetime of the process as measured by the ru_maxrss attribute in the resource module, reported in megabytes
