# (Not So) Fast Forward Solver

[Fast Forward](https://planning.wiki/ref/planners/ff) solver is a well-known algorithm for classical planning problems. 
This laboratory has two aims:

1. To implement the [Graphplan](https://home.ttic.edu/~avrim/graphplan.html) algorithm as a smarter and less memory-consuming alternative to the blind Breadth First-Search
2. Then to use the Graphplan as a heuristic for the FastForward solver.

All the necessary knowledge to understand the algorithms is available via [wiki](https://gitlab.com/agh-courses/24/miasi/wiki-02/-/wikis/home).
The repository contains also a `presentation.pdf` file with nice presentation on the topic of this class.

## TODO: 

- [x] read this `README` to the end
- [x] run solvers `forwardbfs` and `forwarddfs` on the `blocks` domain, an `easy` instance
- [x] fill `#TODO:` in the graphplan solver: `solvers/graphplan/solver.py`
  - use basic `blocks` instances, e.g. `solved`, `one_move`, `sussman`, `easy` to test the solver
  - `npuzzle` also has some easy instances :)
- [x] implement (not so) fast forward solvesr:
  - `TODO:` in `solvers/fast_forward/heuristic/relaxed_solver.py`
  - `TODO:` in `solvers/fast_forward/fast_forward.py`
- [x] compare algorithms on: 
  - `blocks/big.instance`
  - `hanoi/3r_4d.instance`
  - `npuzzle/31_moves.instance`

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
    git push 
    ```

The rest will be taken care of automatically. You can check the `GRADE.md` file for your grade / test results. Be aware that it may take some time (up to one hour) till this file

## How To Run

This class requires Python with version at least 3.10.
Recommended way to run is to create a virtual environment first:
 
- `python -m venv nsffs`
- `source nsffs/bin/activate`

Then install required packages:
- `pip install -r requirements.txt`

Finally you can run a solver:

- `python solve.py -d <stripsdomain> -a <algorithm> -t <timelimit> <instance>`

for example:
- `python solve.py -d problems/blocks/blocks.domain -a forwarddfs -t 3 problems/blocks/easy.instance` (there are three problems with instances in the `problems` directory)

There will be a new `txt` file in the solver directory, e.g., `./blocks - easy_ForwardBFS.txt` with the result and its validation report.

You can also run a benchmark:
- `python benchmark.py -d <domain> -t <timeout> <path_to_instance>`

for example:

- `python benchmark.py -d problems/blocks/blocks.domain -t 3 problems/blocks/big.instance`

If you run script with incorrect arguments, you will get some helpful info ;)

## Project Structure

    .
    ├── problems    # contains STRIPS definition of the problems 
    │  ├── blocks   # - domain/instance files for the blocks world problem
    │  ├── hanoi    # - domain/instance files for the hanoi problem
    │  ├── npuzzle  # - domain/instance files for the npuzzle problem
    │  │  ├── ...
    │  │  ├── 7_moves.instance # example of an instance file
    │  │  └── npuzzle.domain   # a domain file
    │  ├── action.py           # defines STRIPS actions
    │  ├── dto.py              # dataclasses reponsible for problem serialization/deserialization
    │  ├── plan_validator.py   # this class validates STRIPS plans 
    │  ├── problem.py          # the main class defining a STRIPS problem
    │  ├── problem_builder.py  # class building a problem from files
    │  ├── state.py            # defines STRIPS states
    │  └── unifier.py          # grounds actions based on the state
    ├── solvers
    │  ├── fast_forward             # the fast-forward solver
    │  │  ├── heuristic             #   - heuristic used in the solver
    │  │  │  ├── graph              #       * planning graph used by the relaxed graphplan algorithm 
    │  │  │  └── relaxed_solver.py  #       * TODO: a relaxed graphplan solver to calculate the heuristic 
    │  │  ├── fast_forward.py       #   - TODO: defines FastForward and NotSoFastForward solvers
    │  │  └── generic_best_first_search.py  # basic implementation of a heuristic search
    │  ├── forward                  # basic forward search solver
    │  │  ├── forward.py            #   - defines BFS and DFS search procedures
    │  │  └── generic_forward.py    #   - generic forward tree search procedure
    │  ├── graphplan                # graphlan algorithm:
    │  │  ├── graph                 #   - contains data structures used by the algorithm
    │  │  │  ├── graph.py           #       * the main graph class
    │  │  │  └── ...           
    │  │  └── solver.py             #   - TODO: the graphplan solver
    │  └── solver.py                # solver interface to be implemented by all the solvers
    ├── utils                       # some utils used in the solvers
    ├── LICENSE           # a LICENSE file 
    ├── README.md         # this README
    ├── benchmark.py      # script to run algorithm benchmarks
    ├── cli_config.py     # configuration of the cli, do not touch :)
    ├── presentation.pdf  # PDF file with nice presentation on the class topis
    ├── requirements.txt  # virtual env requirements
    └── solve.py          # script to run a specific algorithm on a selected problem
