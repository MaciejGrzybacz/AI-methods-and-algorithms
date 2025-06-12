import argparse
import math
import sys
import time

from cli_config import avl_algos, VERSION
from problems import StripsPlanValidator, StripsAction, StripsProblem, StripsValidationReport
from problems.problem_builder import StripsProblemBuilder
from solvers.solver import Solver


class PrettyOutputSolver:
    _header_name = "---------------------- STRIPS Solver ----------------------"
    _copyright = "@ 2024 Boring Truffle Production"

    def __init__(self, solver: Solver, problem: StripsProblem) -> None:
        self.solver = solver
        self.solver.register_callback(self.print_metric)
        self.problem = problem
        self.wall_time = 0

    #
    def solve(self) -> list[StripsAction] | None:
        self._reset_stats()
        self.print_header()
        result = self.solver.solve()
        self.print_stats()
        self.print_footer(result)
        return result

    def _reset_stats(self):
        self.start_time = time.time()
        self.wall_time = 0

    def _add_margins(self, text: str, margin_symbol: str = "-", border: str = " ") -> str:
        length = len(self._header_name)
        margin = (length - len(text)) / 2
        margin_line_left = margin_symbol * (math.ceil(margin) - len(border))
        margin_line_right = margin_symbol * (math.floor(margin) - len(border))
        return margin_line_left + border + text + border + margin_line_right

    def _header_version(self) -> str:
        return self._add_margins(VERSION)

    def print_header(self):
        header = f"{self._header_name}\n" \
                 f"{self._add_margins(VERSION)}\n" \
                 f"{self._add_margins(self._copyright)}\n" \
                 f"{'-' * len(self._header_name)}\n" \
                 f".....problem:  {self._problem_name()}\n" \
                 f"...algorithm:  {self._solver_name()}"
        header += f"\n{self._add_margins(' SEARCH STATS ', '_', '|')}"
        print(header)

    def _solver_name(self) -> str:
        return self.solver.__class__.__name__

    def _problem_name(self) -> str:
        return self.problem.name

    def print_footer(self, plan: list[StripsAction] | None):
        print(f"\n{self._add_margins('', '-', '')}")
        if plan is None:
            print(
                "\n...failed to solve :(\n...either the problem is unsolvable or there is a bug in the solver")
            return

        validation_report = StripsPlanValidator(self.problem).validate(plan)
        if validation_report.is_valid:
            print(f"...solved successfully!")
            print(f"...plan length: {len(plan)}")
        else:
            print(f"...the plan is incorrect")
        txt_path = self._txt_path()
        self.save_txt(validation_report, txt_path)
        txt_path = "./" + txt_path
        print(f"...consult the following file for details:")
        print(self._add_margins(txt_path, "-", " "))
        print(self._add_margins("-", "-", ""))

    def _txt_path(self) -> str:
        txt_name = f"{self._problem_name()}_{self._solver_name()}"
        txt_name += ".txt"
        return txt_name

    def save_txt(self, result: StripsValidationReport, path: str):
        with open(path, 'w') as f:
            f.write(str(result))

    def print_metric(self, metric: str):
        self.wall_time = time.time() - self.start_time
        txt = f"{metric} | time: {self.wall_time:<8.2f}"
        txt = self._add_margins(txt, " ", "")
        print(
            f"\r{txt}", end='', flush=True)

    def print_stats(self):
        self.print_metric(self.solver.metric())


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def parse_args():
    parser = MyParser(prog="STRIPS Solver",
                      formatter_class=argparse.RawDescriptionHelpFormatter,
                      description="          _,-\"\"\"\"-..__\n     |`,-\'_. `  ` ``  `--\'\"\"\".\n     ;  ,\'  | ``  ` `  ` ```  `.\n   ,"
                                  "-\'   ..-\' ` ` `` `  `` `  ` |==.\n ,\'    ^    `  `    `` `  ` `.  ;   \\\n`}_,-^-   _ .  ` \\ "
                                  "`  ` __ `   ;    #\n   `\"---\"\' `-`. ` \\---\"\"`.`.  `;\n              \\\\` ;       ; `. `,"
                                  "\n  the lost     ||`;      / / | |\n  boar of      //_;`    ,_;\' ,_;\"\n Zakrzówek           ")
    parser.add_argument("instance",
                        help="path to the strips instance to be solved")
    parser.add_argument("-d", "--domain", required=True,
                        help="path to the strips domain")
    parser.add_argument("-a", "--algorithm", required=True,
                        choices=avl_algos.keys(), help="name of the algorithm solver should use")
    parser.add_argument("-t", "--timelimit", required=False, default=30,
                        help="path to the strips domain")
    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()

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
    solver = avl_algos[args.algorithm](problem)
    pretty_solver = PrettyOutputSolver(solver, problem)
    pretty_solver.solve()
