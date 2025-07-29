from .base_worker import BaseWorker
import sys
import os
from PySide6 import QtCore
from .tools import stdout_redirected


class RepWorker(BaseWorker):
    finished = QtCore.Signal(bool, str)

    def __init__(self, my_app, instance, solution, log_path: str, *args, **kwargs):
        BaseWorker.__init__(self, my_app, instance, solution, *args, **kwargs)
        self.log_name = log_path

    def run(self):
        rep_path = ""
        success = False
        try:
            Experiment = self.my_app.get_solver(self.my_app.get_default_solver_name())
            experiment = Experiment(self._instance, self.solution)
            self.status.emit("Task started!")
            self.started.emit()
            if not os.path.exists(self.log_name):
                open(self.log_name, "w").close()
            # we redirect the stdout to the log file, so that we can see the progress in the GUI
            with open(self.log_name, "a") as f, stdout_redirected(f, sys.stderr):
                rep_path = experiment.generate_report("report")
        except:
            import traceback

            self.error.emit(traceback.format_exc())
            self.status.emit("Task failed!")
            success = False

        else:
            success = True
            self.status.emit("Task finished!")
        finally:
            self.finished.emit(success, rep_path)
            sys.stdout = sys.__stdout__  # Restore stdout
