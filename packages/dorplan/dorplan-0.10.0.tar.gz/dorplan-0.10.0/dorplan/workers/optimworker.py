from cornflow_client.constants import (  # type: ignore[import-untyped]
    STATUS_UNDEFINED,
    SOLUTION_STATUS_INFEASIBLE,
)
from .base_worker import BaseWorker
from .tools import stdout_redirected
import os
import sys
from PySide6 import QtCore


class OptimWorker(BaseWorker):
    options: dict
    finished = QtCore.Signal(bool, int, dict)

    def __init__(
        self,
        my_app,
        instance,
        solution,
        options: dict,
        force_log_redirect_win=False,
        *args,
        **kwargs,
    ):
        BaseWorker.__init__(self, my_app, instance, solution, *args, **kwargs)
        self.solver_name: str = options["solver"]
        self.my_callback_obj = None
        self.options = dict(options)
        self.log_name = None
        self.force_log_redirect_win = force_log_redirect_win

    def run(self):
        status = dict(status=STATUS_UNDEFINED, status_sol=SOLUTION_STATUS_INFEASIBLE)
        soldata = ""
        success = False
        try:
            self.status.emit("Task started!")
            self.started.emit()
            my_solver = self.my_app.get_solver(self.solver_name)
            # we configure the callback object and tie it to the solver and the worker
            try:
                # we need to attach the object to self so that it persists
                self.options["stop_condition"] = self.my_callback_obj = (
                    my_solver.getStopOnUser_callback()
                )
            except AttributeError:
                # not all solvers have a callback object
                pass

            # we redirect the stdout to the log file, so that we can see the progress in the GUI
            # if logPath is not provided for whatever reason, we create a log file in the current directory
            self.log_name = self.options.get("logPath", "log.txt")
            if not os.path.exists(self.log_name):
                open(self.log_name, "w").close()

            with (
                open(self.log_name, "a") as f,
                stdout_redirected(f, sys.stdout, self.force_log_redirect_win),
                stdout_redirected(f, sys.stderr, self.force_log_redirect_win),
            ):
                experiment = my_solver(self._instance, self.solution)
                status = experiment.solve(self.options)

            self.solution = experiment.solution

        except:
            import traceback

            self.error.emit(traceback.format_exc())
            success = False

        else:
            success = True
            self.status.emit("Task finished!")
        finally:
            if self.solution is not None:
                soldata = self.solution.to_dict()
            self.finished.emit(success, status["status_sol"], soldata)

    def kill(self):
        # we do not really kill it, we stop it, so we do not call the killed signal
        self.abort = True
        if self.my_callback_obj:
            self.my_callback_obj.stop()
