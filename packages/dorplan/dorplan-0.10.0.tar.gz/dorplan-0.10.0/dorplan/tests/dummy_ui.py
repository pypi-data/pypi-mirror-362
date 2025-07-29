from unittest.mock import MagicMock
from dorplan.workers import OptimWorker  # Import the real OptimWorker


class DummyLog:
    def __init__(self):
        self.lines = []

    def clear(self):
        self.lines.clear()

    def append(self, text):
        self.lines.append(text)

    def insertPlainText(self, text):
        self.lines.append(text)

    def moveCursor(self, *args, **kwargs):
        pass

    def setFont(self, font):
        pass


class DummyUi:
    def __init__(self):
        # Mock all UI elements used in DorPlan
        self.actionOpen_from = MagicMock()
        self.actionSave = MagicMock()
        self.actionSave_As = MagicMock()
        self.actionExit = MagicMock()
        self.chooseFile = MagicMock()
        self.loadTest = MagicMock()
        self.checkSolution = MagicMock()
        self.exportSolution = MagicMock()
        self.exportSolution_to = MagicMock()
        self.generateReport = MagicMock()
        self.generateSolution = MagicMock()
        self.openReport = MagicMock()
        self.max_time = MagicMock()
        self.log_level = MagicMock()
        self.solver = MagicMock()
        self.tabWidget = MagicMock()
        self.instCheck = MagicMock()
        self.solCheck = MagicMock()
        self.reuse_sol = MagicMock()
        self.solution_log = DummyLog()
        self.stopExecution = MagicMock()
        self.solution_report = DummyLog()
        self.objectiveLineEdit = MagicMock()
        self.errorsLineEdit = MagicMock()
        self.progressBar = MagicMock()

    def setupUi(self, MainWindow):
        pass


class MockWorker:
    def __init__(
        self,
        app_type,
        instance_data,
        solution_data,
        options,
        force_log_redirect_win=False,
    ):
        self.started = MagicMock()
        self.finished = MagicMock()
        self.error = MagicMock()
        self.killed = MagicMock()
        self.setObjectName = MagicMock()
        self.start = MagicMock()
        self.kill = MagicMock()
        self.deleteLater = MagicMock()
        self.run_called = False
        # Simulate attributes used in DorPlan.get_solution
        self.success = True
        self.sol_status = 1
        self.soldata = {}
        # Store args for possible use in run
        self.app_type = app_type
        self.instance_data = instance_data
        self.solution_data = solution_data
        self.options = options
        self.force_log_redirect_win = force_log_redirect_win

    # Assign the real OptimWorker.run method to MockWorker.run
    run = OptimWorker.run


class MockRepWorker:
    def __init__(self, *args, **kwargs):
        self.started = MagicMock()
        self.finished = MagicMock()
        self.error = MagicMock()
        self.killed = MagicMock()
        self.setObjectName = MagicMock()
        self.start = MagicMock()
        self.kill = MagicMock()
        self.deleteLater = MagicMock()
        self.run_called = False
        # Simulate attributes used in DorPlan.load_report
        self.success = True
        self.rep_path = "mock_report.html"

    def run(self):
        """
        Simulate the run method of RepWorker.
        Typically, this would emit started, do some work, and emit finished.
        """
        self.run_called = True
        if hasattr(self, "started"):
            self.started.emit()
        if hasattr(self, "finished"):
            # The real RepWorker emits (success, rep_path)
            self.finished.emit(self.success, self.rep_path)
        return "MockRepWorker run executed"
