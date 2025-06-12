import re
from typing import Type, cast
from solvers import ForwardBFS, ForwardDFS, GraphPlan, FastForward, NotSoFastForward
from solvers.solver import Solver

VERSION = "0.3(3) — Irrelevant Iguana"


def snake_to_camel(snake: str) -> str:
    return ''.join(x.title() for x in snake.split('_'))


def camel_to_snake(camel: str, useless_suffix: str = '') -> str:
    useful_camel = camel.replace(useless_suffix, '')
    return re.sub(r'(?<!^)(?=[A-Z])', '_', useful_camel).lower()

avl_algos: dict[str, Type[Solver]] = {a.__name__.lower(): cast(Type[Solver], a)
                                      for a in [ForwardBFS, ForwardDFS, GraphPlan, FastForward, NotSoFastForward]}
