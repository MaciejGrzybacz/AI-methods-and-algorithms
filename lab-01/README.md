# State Space Search

This repository contains a basic framework to implement and test state space search algorithms. Your task is to finish it :)

## TODO: 

  * [ ] run already implementend algorithm `dfsrecursive` on the `grid_pathfinding` problem, use the smallest instance named `5.txt` (from the `problems/grid_pathfinding/instances/` directory). Checkout the result: `GridPathfinding_5_DFSRecursive.gif`. Section `How To Run` should help you.
  * [ ] implement the uninformed search following the TODO comments: `solvers/generic/uninformed.py`
    - run benchmark on the `n_puzzle` problem, instance `03_03` to compare the uninformed algorithms
  * [ ] implement the directed search following the TODO comments: `solvers/generic/best_first.sh`
    - run benchmarks:
      - `rush_hour` problem, instance `16`
      - `pancake` problem, instance `14`
  * [ ] implement heuristics: `problems/grid_pathfinding/heuristics/euclidean_heuristic.py`, `problems/grid_pathfinding/heuristics/manhattan_heuristic.py`, `problems/grid_pathfinding/heuristics/diagonal_heuristic.py`
    - run benchmark for `grid_pathfinding`, instance `40`
  * [ ] implement heuristics: `problems/n_puzzle/heuristics/n_puzzle_tiles_out_of_place_heuristic.py`, `problems/n_puzzle/heuristics/n_puzzle_manhattan_heuristic.py`
    - run benchmark for `n_puzzle`, instance `03_31`
    - use the best algorithm to solve the instance and relax a bit watching the gif result
  * [ ] finish `n_blocks` environment: `problems/blocks_world/blocks_world_problem.py`, `problems/blocks_world/blocks_world_action.py` and implement a heuristic `problems/blocks_world/blocks_world_heuristic.py`
    - run benchmark on the `03_07_14` instance
  * [ ] implement the bidirectional directed search algorithm: `solvers/generic/bidirectional_search.py`
    - run benchmark: `n_puzzle`, instance `03_31`
    - run benchmark: `blocks_world`, instance `04_10_15`
    - run benchmark: `grid_pathfinding`, instance `38_26` — why NBA is so much better in this particular scenario?

### Useful links:

- [interactive pathfinding on grids](http://krzysztof.kutt.pl/didactics/psi/pathfinder/)
- [definitions of various grid heuristics](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#heuristics-for-grid-maps)
- [nice blog post about A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [elegant n-puzzle visualization](http://krzysztof.kutt.pl/didactics/psi/npuzzles/)
- NBA* - papers explaining the algorithm: [1](https://www.researchgate.net/publication/46434387_Yet_another_bidirectional_algorithm_for_shortest_paths), [2 — requires access via AGH library/other means](https://www.sciencedirect.com/science/article/abs/pii/S0377221708007613), 

## Grading

* [ ] Make sure, you have a **private** group
  * [how to create a group](https://docs.gitlab.com/ee/user/group/#create-a-group)
* [ ] Fork this project into your private group
  * [how to create a fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#creating-a-fork)
* [ ] Add @bobot-is-a-bot as the new project's member (role: **maintainer**)
  * [how to add an user](https://docs.gitlab.com/ee/user/project/members/index.html#add-a-user)

## How To Submit Solutions

* [ ] Clone repository: git clone:
    ```bash
    git clone <repository url>
    ```
* [ ] Solve the exercises
    * use MiniZincIDE, whatever
* [ ] Commit your changes
    ```bash
    git add <path to the changed files>
    git commit -m <commit message>
    ```
* [ ] Push changes to the gitlab master branch
    ```bash
    git push -u origin master
    ```

The rest will be taken care of automatically. You can check the `GRADE.md` file for your grade / test results. Be aware that it may take some time (up to one hour) till this file

## How To Run

This assignment has been tested with Python 3.13.*. 
*Probably* one could use any Python >= 3.10 — in such case one may have remove the pinned package versions from the `requirements.txt`.
The simplest way to run the project is to create a virtual environment first:
 
- `python -m venv state-search`
- `source state-search/bin/activate`

Then install required packages:
- `pip install -r requirements.txt`

Finally you can run a solver:
- `python solve.py -a <algorithm> -p <problem> -h <heuristic> <path_to_instance>`, e.g.
- `python solve.py -p rush_hour -a astar -h rush_hour_indirect problems/rush_hour/instances/81.txt` (every problem has several instances in the `instances` directory)

You can also run a benchmark:
- `python benchmark.py -p <problem> -t timeout <path_to_instance>`, e.g.
- `python benchmark.py -p rush_hour problems/rush_hour/instances/54.txt`

If you run script with incorrect arguments (or without them), you will get some helpful info ;)

## Project Structure

    .
    ├── base                # API for problem and solver classes
    ├── problems            # list of defined problems (place to define problems)
    │   ├── ...
    │   ├── n_puzzle        # directory with a problem
    │   │   ├── instances   # directory with problem instances
    │   │   └── ...
    │   └── ...
    ├── solvers             # directory with algorithms
    │   ├── generic         # code shared by several algorithms
    │   ├── bfs.py          # example of an algorithm
    │   └── ...
    ├── tree                # search tree representation
    ├── utils               # various utilities
    ├── solve.py            # solve tool (run as a script)
    ├── benchmark.py        # benchmark tool (run as a script)
    └── cli_config.py       # configuration of the cli tools (do not touch)
