from PySide6 import QtWidgets, QtCore, QtGui
import os


class ProgressMonitor(QtCore.QObject):
    file_path: str
    text_browser: QtWidgets.QTextBrowser
    progress_bar: QtWidgets.QProgressBar
    time_limit: int
    interval: int
    last_position: int
    elapsed_time: float
    keep_log_file: bool
    timer: QtCore.QTimer

    def __init__(
        self,
        file_path,
        text_browser: QtWidgets.QTextBrowser,
        progress_bar: QtWidgets.QProgressBar | None,
        time_limit: int,
        interval=1000,
        parent=None,
        keep_log_file=False,
    ):
        super().__init__(parent)
        self.file_path = file_path
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        self.text_browser = text_browser
        self.progress_bar = progress_bar
        if self.progress_bar is not None:
            self.progress_bar.setEnabled(True)
            self.progress_bar.setValue(0)
        self.elapsed_time = 0  # in sec
        self.time_limit = time_limit  # in sec
        self.text_browser.clear()
        self.interval = interval  # in msec
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_log)
        self.last_position = 0
        self.keep_log_file = keep_log_file

    @QtCore.Slot()
    def start(self):
        self.timer.start(self.interval)

    @QtCore.Slot()
    def stop(self):
        # we update the log one last time
        self.update_log()
        # we stop the timer
        self.timer.stop()
        if self.progress_bar is not None:
            self.progress_bar.setEnabled(False)
        # we delete the log file, unless we configure not to
        if not self.keep_log_file and os.path.exists(self.file_path):
            os.remove(self.file_path)

    @QtCore.Slot()
    def update_log(self):
        if self.progress_bar is not None:
            self.elapsed_time += self.interval / 1000
            self.progress_bar.setValue(
                round(self.elapsed_time * 100 // self.time_limit)
            )
        if not os.path.exists(self.file_path):
            return
        with open(self.file_path, "r") as file:
            file.seek(self.last_position)
            content = file.read()
            self.last_position = file.tell()
            if content:
                self.text_browser.insertPlainText(content)
                self.text_browser.moveCursor(QtGui.QTextCursor.MoveOperation.End)
