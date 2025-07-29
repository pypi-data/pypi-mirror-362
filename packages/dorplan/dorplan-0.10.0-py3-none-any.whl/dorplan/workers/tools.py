from contextlib import contextmanager
from io import TextIOWrapper
import sys
import os
import platform


def fileno(file_or_fd: TextIOWrapper | str):
    fd = getattr(file_or_fd, "fileno", lambda: file_or_fd)()
    if fd is None:
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd


@contextmanager
def stdout_redirected(
    to: TextIOWrapper | str = os.devnull, stdout=None, force_log_redirect_win=False
):
    if stdout is None:
        stdout = sys.stdout
    # Special handling for Windows to avoid PyInstaller issues
    windows_pyinstaller = platform.system() == "Windows" and (
        getattr(sys, "frozen", False) or force_log_redirect_win
    )

    if windows_pyinstaller:
        original_write = stdout.write

        def new_write(data):
            to.write(data)
            to.flush()

        stdout.write = new_write
        try:
            yield stdout
        finally:
            stdout.write = original_write
    else:
        try:
            stdout_fd = fileno(stdout)
        except ValueError:
            # If fileno is not supported, use a different approach
            original_write = stdout.write

            def new_write(data):
                to.write(data)
                to.flush()

            stdout.write = new_write
            try:
                yield stdout
            finally:
                stdout.write = original_write

        else:
            # If fileno is supported, use the original approach
            # copy stdout_fd before it is overwritten
            # NOTE: `copied` is inheritable on Windows when duplicating a standard stream
            with os.fdopen(os.dup(stdout_fd), "wb") as copied:
                stdout.flush()  # flush library buffers that dup2 knows nothing about
                try:
                    os.dup2(fileno(to), stdout_fd)  # $ exec >&to
                except ValueError:  # filename
                    to = str(to)
                    with open(to, "wb") as to_file:
                        os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to
                try:
                    yield stdout  # allow code to be run with the redirected stdout
                finally:
                    # restore stdout to its previous value
                    # NOTE: dup2 makes stdout_fd inheritable unconditionally
                    stdout.flush()
                    os.dup2(copied.fileno(), stdout_fd)  # $ exec >&copied
