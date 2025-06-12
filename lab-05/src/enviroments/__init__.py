from gym.envs.registration import register
from src.enviroments.grid_pathfinding.env import GridPathfindingEnv
from inspect import getmodule

def as_entry_point(cls: type):
    return f'{getmodule(cls).__name__}:{cls.__name__}'

register("custom/gridpathfinding-v0", entry_point=as_entry_point(GridPathfindingEnv))