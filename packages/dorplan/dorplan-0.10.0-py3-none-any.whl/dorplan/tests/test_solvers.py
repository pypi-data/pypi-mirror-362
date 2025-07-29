import unittest
import os
import sys
from cornflow_client.constants import SOLUTION_STATUS_FEASIBLE

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dorplan.tests.data.graph_coloring import GraphColoring


class GraphColoringSolversTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = GraphColoring()
        cls.test_cases = cls.app.test_cases
        cls.solver_names = cls.app.solvers.keys()

    def _run_solver_and_check(self, solver_name, test_case, **kwargs):
        instance = self.app.instance.from_dict(test_case["instance"])
        solver_cls = self.app.get_solver(solver_name)
        solver = solver_cls(instance)
        status = solver.solve(kwargs)
        objective = solver.get_objective()
        # Check solution validity
        checks = solver.check_solution()
        self.assertTrue(status["status_sol"] == SOLUTION_STATUS_FEASIBLE)
        self.assertIs(len(checks["pairs"]), 0)
        self.assertIs(len(checks["missing"]), 0)
        self.assertTrue(objective >= 1)
        print(f"{solver_name}: {objective}")

    def test_ortools_dataset1(self):
        self._run_solver_and_check("ortools", self.test_cases[0])

    def test_ortools_dataset2(self):
        self._run_solver_and_check("ortools", self.test_cases[1])

    def test_pulp_dataset1(self):
        self._run_solver_and_check("pulp", self.test_cases[0])

    def test_pulp_dataset2(self):
        self._run_solver_and_check("pulp", self.test_cases[1], timeLimit=5)

    def test_timefold_dataset1(self):
        self._run_solver_and_check("timefold", self.test_cases[0], timeLimit=2)

    def test_timefold_dataset2(self):
        self._run_solver_and_check("timefold", self.test_cases[1], timeLimit=5)

    def test_networkx_dataset1(self):
        self._run_solver_and_check("networkx", self.test_cases[0], timeLimit=2)

    def test_networkx_dataset2(self):
        self._run_solver_and_check("networkx", self.test_cases[1], timeLimit=5)
