from cornflow_client.constants import (
    STATUS_UNDEFINED,
    SOLUTION_STATUS_INFEASIBLE,
)
from .base_worker import BaseWorker
from .tools import stdout_redirected
import os
import sys

# import traceback
from PySide6 import QtCore
import multiprocessing


def solver_process(app_class, instance, solution, options, force_log_redirect_win):
    # This function runs in a separate process
    status = dict(status=STATUS_UNDEFINED, status_sol=SOLUTION_STATUS_INFEASIBLE)
    soldata = ""
    success = False
    try:
        my_app = app_class()
        my_solver = my_app.get_solver(options["solver"])

        log_name = options.get("logPath", "log.txt")
        if not os.path.exists(log_name):
            open(log_name, "w").close()

        with (
            open(log_name, "a") as f,
            stdout_redirected(f, sys.stdout, force_log_redirect_win),
            stdout_redirected(f, sys.stderr, force_log_redirect_win),
        ):
            experiment = my_solver(instance, solution)
            status = experiment.solve(options)
            solution_obj = experiment.solution

        if solution_obj is not None:
            soldata = solution_obj.to_dict()
        success = True
        # print("we got a result")
        return ("result", success, status["status_sol"], soldata)
    except Exception:
        import traceback

        # print("we got an error")
        return ("error", traceback.format_exc())


class OptimWorkerMulti(BaseWorker):
    options: dict
    finished = QtCore.Signal(bool, int, dict)
    error = QtCore.Signal(str)
    started = QtCore.Signal()
    status = QtCore.Signal(str)
    killed = QtCore.Signal()

    _instance_count = 0

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
        self._pool = None
        self._async_result = None
        self._aborted = False
        # OptimWorkerMulti._instance_count += 1
        # print(
        #     f"[OptimWorkerMulti] __init__ called. Instance count: {OptimWorkerMulti._instance_count} (id={id(self)})"
        # )

    # def __del__(self):
    #     OptimWorkerMulti._instance_count -= 1
    #     print(
    #         f"[OptimWorkerMulti] __del__ called. Instance count: {OptimWorkerMulti._instance_count} (id={id(self)})"
    #     )

    def run(self):
        # print(f"[OptimWorkerMulti] run called (id={id(self)})")
        # This method is called in the Qt thread, but the solver runs in a subprocess
        self.status.emit("Task started!")
        self.started.emit()
        app_class = type(self.my_app)
        self._pool = multiprocessing.Pool(processes=1)
        self._async_result = self._pool.apply_async(
            solver_process,
            (
                app_class,
                self._instance,
                self.solution,
                self.options,
                self.force_log_redirect_win,
            ),
            callback=self._on_result,
        )

    def _on_result(self, result):
        # print(f"[OptimWorkerMulti] _on_result called (id={id(self)})")
        if result[0] == "error":
            self.error.emit(result[1])
            self.finished.emit(False, SOLUTION_STATUS_INFEASIBLE, {})
        elif result[0] == "result":
            _, success, status_sol, soldata = result
            self.status.emit("Task finished!")
            self.finished.emit(success, status_sol, soldata)
            print("Loaded results")
        self._cleanup()

    def _cleanup(self):
        # print(f"[OptimWorkerMulti] _cleanup called (id={id(self)})")
        if self._pool:
            self._pool.terminate()
            self._pool = None
        self._async_result = None

    def kill(self):
        # print(f"[OptimWorkerMulti] kill called (id={id(self)})")
        self._aborted = True
        self.killed.emit()
        # print("killed pool")
        self._cleanup()
