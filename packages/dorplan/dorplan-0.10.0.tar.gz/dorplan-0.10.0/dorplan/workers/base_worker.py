from PySide6 import QtCore
import logging
from cornflow_client import ApplicationCore  # type: ignore[import-untyped]
from typing import Type


class BaseWorker(QtCore.QThread):
    error = QtCore.Signal(str)
    progress = QtCore.Signal(int)
    status = QtCore.Signal(str)
    killed = QtCore.Signal()
    started = QtCore.Signal()
    finished = QtCore.Signal(bool)
    log_message = QtCore.Signal(str)

    def __init__(
        self,
        my_app: Type[ApplicationCore],
        instance: dict,
        solution: dict,
        *args,
        **kwargs,
    ):
        QtCore.QThread.__init__(self, *args, **kwargs)
        self.abort = False
        self.is_running = True
        self.my_app = my_app()

        self._instance = self.my_app.instance.from_dict(instance)
        self.solution = None
        if solution is not None:
            self.solution = self.my_app.solution.from_dict(solution)

        # self.text_browser_handler = SignalLogger(self.log_message)

    def run(self):
        # sys.stdout = StreamLogger(self.log_message)
        # self.options["log_handler"] = self.text_browser_handler
        # sys.stdout = sys.__stdout__  # Restore stdout

        raise NotImplementedError()

    def kill(self):
        raise NotImplementedError()
