"""Module for running solutions in a separate thread using QRunnable."""
from typing import Any, List

from PyQt6.QtCore import QRunnable, pyqtSlot

from ari3d.gui.controller.io.album_c import AlbumController


class RunSolutionTask(QRunnable):
    """QRunnable task for running a solution in a separate thread."""

    def __init__(self, album_api: AlbumController, solution: str, argv: List[Any]):
        """Initialize the task with the album API, solution ID, and arguments."""
        super().__init__()
        self.album_api = album_api
        self.solution = solution
        self.argv = argv
        # self.signals = WorkerSignalsSolution()

    @pyqtSlot()
    def run(self):
        """Run the solution using the album API."""
        try:
            import logging

            from album.core.utils.core_logging import push_active_logger

            push_active_logger(
                logging.getLogger("album")
            )  # we are in a thread. push the logger again

            self.album_api.install_solution(self.solution)
            self.album_api.run(self.solution, argv=self.argv)
            if self.on_finished:
                self.on_finished()
        except Exception as e:
            if self.on_error:
                self.on_error(e)
            else:
                raise e
