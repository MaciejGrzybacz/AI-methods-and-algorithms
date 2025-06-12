import sys
import traceback
import stopit
import argparse
from cli_config import VERSION, avl_algos
from typing import Union
from pathlib import Path
import time

from problems import StripsAction, StripsPlanValidator
from problems.problem_builder import StripsProblemBuilder
from solvers.solver import Solver


class BenchmarkMonitor:

    def __init__(self, solver: Solver, longest_name: int, timeout: float) -> None:
        self.solver = solver
        self.solver.register_callback(self.print_stats)
        self._reset_stats()
        self.longest_name = longest_name
        self.timeout = timeout

    @stopit.threading_timeoutable(default='timeout')
    def solve_with_timeout(self) -> list[StripsAction] | None:
        return self.solver.solve()

    def solve(self) -> list[StripsAction] | str | None:
        self._reset_stats()
        self.print_stats(None)
        try:
            result = self.solve_with_timeout(timeout=self.timeout)
        except RecursionError:
            result = "recursion stack overflow"
        self.print_stats(None)
        self.print_result(result)
        return result

    def _reset_stats(self):
        self.start_time = time.time()

    @property
    def wall_time(self) -> float:
        return time.time() - self.start_time

    def _solver_name(self) -> str:
        return self.solver.__class__.__name__

    def print_stats(self, metric: str | None):
        details = metric if metric is not None else self.solver.metric()
        algo_name = self._solver_name()
        print(f"\r{algo_name: >{self.longest_name}} | {self.wall_time:<8.2f} | {details} |", end='', flush=True)

    def print_result(self, result: list[StripsAction]):
        if result is None:
            print(" fail")
        elif isinstance(result, str):
            print(f" {result}")
        else:
            plan_validator = StripsPlanValidator(self.solver.problem)
            report = plan_validator.validate(result)
            valid = "" if report.is_valid else "INVALID "

            print(f" {valid}PLAN ({len(result)} STEPS)")


def print_header(problem, timeout, longest_name):
    print(f"> STRIPS Benchmark ({VERSION})")
    print(f"-  problem: {problem.name}")
    print(f"-  timeout: {timeout}s")
    print(f"{'solver name': >{longest_name}} | {'time (s)': <8} | details | result")
    print("-" * 110)


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def parse_args():
    parser = MyParser(prog="STRIPS Solver Benchmark",
                      formatter_class=argparse.RawDescriptionHelpFormatter,
                      description="          _,-\"\"\"\"-..__\n     |`,-\'_. `  ` ``  `--\'\"\"\".\n     ;  ,\'  | ``  ` `  ` ```  `.\n   ,"
                                  "-\'   ..-\' ` ` `` `  `` `  ` |==.\n ,\'    ^    `  `    `` `  ` `.  ;   \\\n`}_,-^-   _ .  ` \\ "
                                  "`  ` __ `   ;    #\n   `\"---\"\' `-`. ` \\---\"\"`.`.  `;\n              \\\\` ;       ; `. `,"
                                  "\n  the lost     ||`;      / / | |\n  boar of      //_;`    ,_;\' ,_;\"\n Zakrzówek           ")
    parser.add_argument("instance",
                        help="path to the strips instance to be solved")
    parser.add_argument("-d", "--domain", required=True,
                        help="path to the strips domain")
    parser.add_argument("-t", "--timelimit", required=False, default=30,
                        help="path to the strips domain")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    timelimit = int(args.timelimit)

    try:
        with open(args.domain) as domain_file:
            domain_text = domain_file.read()
    except FileNotFoundError as e:
        print(f'> Path to the domain {args.instance} seem to be incorrect, are you sure of it?')
        sys.exit(1)

    try:
        with open(args.instance) as instance_file:
            instance_text = instance_file.read()
    except FileNotFoundError as e:
        print(f'> Path to the instance {args.instance} seem to be incorrect, are you sure of it?')
        sys.exit(1)

    problem = StripsProblemBuilder(domain_text, instance_text).build()

    longest_name = max(len(a.__name__) for a in avl_algos.values()) + 2
    print_header(problem, timelimit, longest_name)
    for algorithm_class in avl_algos.values():
        algorithm: Solver | None = None
        solver_name = algorithm_class.__name__
        try:
            algorithm = algorithm_class(problem)
            solver_monitor = BenchmarkMonitor(
                algorithm, longest_name, timelimit)
            solver_monitor.solve()
        except NotImplementedError as e:
            print("\r" + " " * 100, end='')
            print(
                f"\r{solver_name: >{longest_name}} | algorithm is not implemented yet")
        except Exception as e:
            print("\r" + " " * 100, end='')
            print(
                f"\r{solver_name: >{longest_name}} | algorithm raised an error {repr(e)}")
    print("-" * 110)
