import unittest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dorplan.tests.data.graph_coloring import GraphColoring
from dorplan.app import DorPlan
from dorplan.tests.dummy_ui import DummyUi, MockWorker, MockRepWorker


class AppTest(unittest.TestCase):
    def setUp(self):
        # Patch QApplication and QMainWindow for all tests
        self.qapp_patcher = patch("dorplan.app.QtWidgets.QApplication")
        self.mainwindow_patcher = patch("dorplan.app.QtWidgets.QMainWindow")
        self.mock_qapp = self.qapp_patcher.start()
        self.mock_mainwindow = self.mainwindow_patcher.start()
        self.mock_qapp.return_value = MagicMock()
        self.mock_mainwindow.return_value = MagicMock()
        self.dummy_ui = DummyUi()

    def tearDown(self):
        self.qapp_patcher.stop()
        self.mainwindow_patcher.stop()

    def test_open_app(self):
        app = DorPlan(GraphColoring, {}, ui=DummyUi)
        self.assertIsInstance(app, DorPlan)

    def test_update_options(self):
        self.dummy_ui.max_time.text.return_value = "120"
        self.dummy_ui.log_level.currentIndex.return_value = 1
        self.dummy_ui.solver.currentText.return_value = "solver1"
        app = DorPlan(GraphColoring, {}, ui=lambda: self.dummy_ui)
        app.options = {}
        result = app.update_options()
        self.assertEqual(app.options["timeLimit"], 120)
        self.assertTrue(app.options["debug"])
        self.assertEqual(app.options["solver"], "solver1")
        self.assertEqual(result, 1)

    def test_update_ui_no_instance(self):
        app = DorPlan(GraphColoring, {}, ui=lambda: self.dummy_ui)
        # app.ui = dummy_ui
        app.instance = None
        app.solution = None
        result = app.update_ui()
        self.dummy_ui.instCheck.setText.assert_called_with("No instance loaded")
        self.dummy_ui.instCheck.setStyleSheet.assert_called()
        self.dummy_ui.solCheck.setText.assert_called_with("No solution loaded")
        self.dummy_ui.solCheck.setStyleSheet.assert_called()
        self.dummy_ui.reuse_sol.setEnabled.assert_called_with(False)
        self.dummy_ui.reuse_sol.setChecked.assert_called_with(False)
        self.assertEqual(result, 1)

    def test_load_test_loads_instance_and_solution(self):
        app = DorPlan(GraphColoring, {}, ui=lambda: self.dummy_ui)
        app.instance = None
        app.solution = None
        app.load_test()
        self.assertIsNotNone(app.instance)
        # Some test cases may not have a solution, so just check attribute exists
        self.assertTrue(hasattr(app, "solution"))

    def test_generate_solution_runs_and_updates_ui(self):
        self.dummy_ui.reuse_sol.isChecked.return_value = False
        self.dummy_ui.solver.currentText.return_value = "default"
        self.dummy_ui.max_time.text.return_value = "60"
        self.dummy_ui.log_level.currentIndex.return_value = 0
        self.dummy_ui.solver.addItems = MagicMock()
        self.dummy_ui.tabWidget = MagicMock()
        app = DorPlan(GraphColoring, {}, ui=lambda: self.dummy_ui)
        app.options = {"solver": "default", "timeLimit": 60, "debug": False}
        app.load_test()
        # Patch OptimWorker to avoid threading and side effects
        with (
            patch("dorplan.app.OptimWorker", MockWorker),
            patch("dorplan.app.ProgressMonitor"),
        ):
            mock_worker_instance = app.opt_worker
            self.dummy_ui.stopExecution.clicked.connect = MagicMock()
            self.dummy_ui.generateSolution.setEnabled = MagicMock()
            self.dummy_ui.stopExecution.setEnabled = MagicMock()
            result = app.generate_solution()
            self.assertEqual(result, 1)
            # No need to check mock_worker_instance.start, as it's a MagicMock

    def test_generate_report_runs_and_updates_ui(self):
        app = DorPlan(GraphColoring, {}, ui=lambda: self.dummy_ui)
        app.instance = app.Instance.from_dict(GraphColoring().test_cases[0]["instance"])
        app.solution = app.Solution.from_dict(
            GraphColoring().test_cases[0].get("solution", {})
        )
        # Patch RepWorker and dependencies
        with (
            patch("dorplan.app.RepWorker", MockRepWorker),
            patch("dorplan.app.ProgressMonitor"),
        ):
            result = app.generate_report()
            self.assertTrue(result)
            # Check that the solution_report log was cleared
            self.assertEqual(self.dummy_ui.solution_report.lines, [])

    def test_check_instance_valid(self):
        """Test DorPlan.check_instance with a valid GraphColoring instance."""
        app = DorPlan(GraphColoring, {}, ui=lambda: self.dummy_ui)
        data = GraphColoring().test_cases[0]["instance"]
        app.instance = app.Instance.from_dict(data)
        app.check_instance()
        log = self.dummy_ui.solution_log.lines
        self.assertIn("No errors found in the instance.", log[-1])

    def test_check_instance_invalid(self):
        """Test DorPlan.check_instance with a modified (invalid) GraphColoring instance."""
        app = DorPlan(GraphColoring, {}, ui=lambda: self.dummy_ui)
        data = GraphColoring().test_cases[0]["instance"].copy()
        # Introduce an invalid edge (nodes not in the node list)
        data["pairs"].append(dict(n1="nonexistent_node", n2="another_fake_node"))
        app.instance = app.Instance.from_dict(data)
        app.check_instance()
        log = self.dummy_ui.solution_log.lines
        self.assertTrue(any("Errors found in the instance:" in line for line in log))


if __name__ == "__main__":
    unittest.main()
