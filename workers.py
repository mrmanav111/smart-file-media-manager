from threading import Event
from PyQt6.QtCore import QThread, pyqtSignal
from file_model import scan_directory


class FolderScanner(QThread):
    progress = pyqtSignal(int)
    result_ready = pyqtSignal(list, int, bool)
    error = pyqtSignal(str)

    def __init__(self, folder, parent=None):
        super().__init__(parent)
        self.folder = folder
        self._cancel = Event()

    def cancel(self):
        self._cancel.set()

    def run(self):
        try:
            records, skipped, cancelled = scan_directory(
                self.folder,
                on_progress=self.progress.emit,
                should_cancel=self._cancel.is_set,
            )
            self.result_ready.emit(records, skipped, cancelled)
        except Exception as exc:
            self.error.emit(str(exc))
