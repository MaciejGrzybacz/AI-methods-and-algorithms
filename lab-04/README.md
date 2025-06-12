# Lab 06 - Monte Carlo Search

This is a direct continuation of the previous lab and one is expected to have proper understanding of the MinMax algorithms family. 

The following assignments are meant to teach about another family algorithms based on the random sampling of the state space using so-called Monte Carlo methods.

# TODO: 

First, just look around at the codebase, read the whole `README`, etc.
Search for `TODO` text in the repository with CTRL+F and replace it with you code written according to it.

The preferred task order is: 

- [x] copy/finish NegaMax implementations from the previous lab
- [x] implement `algorithms/monte_carlo.py` 
- [x] implement `algorithms/ucb.py` 
- [x] implement `algorithms/mcts.py` 
- [x] run `experiment_5.py` and `experiment_6.py`

Use `main.py` to play around with various duels and `main_competition.py` to play tournaments.

## How To Run

This class requires Python with version 3.10.*.
Recommended way to run is to create a virtual environment first:
 
- `python -m venv adversarial-search`
- `source adversarial-search/bin/activate`

Then install required packages:
- `pip install -r requirements.txt`

After that configure `main.py`:

- specify `game` (see `games` folder)
- specify algorithm (see `algorithm` folder) 

and run the file.


Also, you can run a tournament between bots, by configuring file `main-tournament.py`.
In tournament a match is played between all configured bots for every configured game and results in the following output:

![image](https://user-images.githubusercontent.com/21079319/221435950-18cb0b7b-15be-439e-b021-f30c0d018bb8.png)


You will see a summary with total wins for every engaged bot and a table presenting statistics for bot vs bot clashes.

## Grading

* [x] Make sure, you have a **private** group
  * [how to create a group](https://docs.gitlab.com/ee/user/group/#create-a-group)
* [x] Fork this project into your private group
  * [how to create a fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#creating-a-fork)
* [x] Add @bobot-is-a-bot as the new project's member (role: **maintainer**)
  * [how to add an user](https://docs.gitlab.com/ee/user/project/members/index.html#add-a-user)
* [x] Clone repository: git clone:
    ```bash
    git clone <repository url>
    ```
* [x] Solve the exercises
* [x] Commit your changes
    ```bash
    git add <path to the changed files>
    git commit -m <commit message>
    ```
* [x] Push changes to the gitlab master branch
    ```bash
    git push 
    ```

The rest will be taken care of automatically. You can check the `GRADE.md` file for your grade / test results. Be aware that it may take some time (up to one hour) till this file