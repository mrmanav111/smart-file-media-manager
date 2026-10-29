import os
from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem

from file_model import file_category, filter_files, readable_size, save_file_report
from main_window import MainWindow
from workers import FolderScanner


class AppController(MainWindow):
    def __init__(self):
        super().__init__()
        self.folder = ''
        self.records = []
        self.scanner = None
        self.audio_path = None
        self.audio_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.audio_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.7)

        self.open_button.clicked.connect(self.choose_folder)
        self.scan_button.clicked.connect(self.start_scan)
        self.cancel_button.clicked.connect(self.cancel_scan)
        self.export_button.clicked.connect(self.export_csv)
        self.open_action.triggered.connect(self.choose_folder)
        self.export_action.triggered.connect(self.export_csv)
        self.exit_action.triggered.connect(self.close)
        self.about_action.triggered.connect(self.show_about)
        self.search_box.textChanged.connect(self.update_table)
        self.type_filter.currentTextChanged.connect(self.update_table)
        self.file_table.itemSelectionChanged.connect(self.show_preview)
        self.play_button.clicked.connect(self.toggle_audio)
        self.volume_slider.valueChanged.connect(self.change_volume)
        self.audio_player.playbackStateChanged.connect(self.update_play_button)
        self.audio_player.errorOccurred.connect(self.audio_error)

    def show_about(self):
        QMessageBox.information(self, 'About', 'Smart File & Media Manager\nBuilt with Python and PyQt6.')

    def choose_folder(self):
        if self.scanner is not None and self.scanner.isRunning():
            QMessageBox.information(self, 'Scan in progress', 'Finish or cancel the scan first.')
            return
        folder = QFileDialog.getExistingDirectory(self, 'Choose a folder')
        if not folder:
            return
        self.stop_audio()
        self.folder = folder
        self.records = []
        self.folder_label.setText(f'Selected folder: {folder}')
        self.search_box.clear()
        self.type_filter.setCurrentText('All files')
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.update_table()
        self.statusBar().showMessage('Folder selected. Ready to scan.')

    def start_scan(self):
        if self.scanner is not None and self.scanner.isRunning():
            return
        if not self.folder or not os.path.isdir(self.folder):
            QMessageBox.warning(self, 'Folder needed', 'Please select an existing folder first.')
            return
        self.stop_audio()
        self.open_button.setEnabled(False)
        self.scan_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.progress_bar.setRange(0, 0)  # Unknown total: show a moving bar
        self.count_label.setText('Scanning...')
        self.statusBar().showMessage('Scanning files...')
        self.scanner = FolderScanner(self.folder, self)
        self.scanner.progress.connect(self.scan_progress)
        self.scanner.result_ready.connect(self.scan_complete)
        self.scanner.error.connect(self.scan_failed)
        self.scanner.finished.connect(self.scan_finished)
        self.scanner.start()

    def cancel_scan(self):
        if self.scanner is not None and self.scanner.isRunning():
            self.scanner.cancel()
            self.cancel_button.setEnabled(False)
            self.statusBar().showMessage('Cancelling scan...')

    def scan_progress(self, count):
        self.count_label.setText(f'{count} files found so far')
        self.statusBar().showMessage(f'Scanning... {count} files found')

    def scan_complete(self, records, skipped, cancelled):
        self.records = records
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0 if cancelled else 100)
        self.update_table()
        status = 'Scan cancelled' if cancelled else 'Scan completed'
        message = f'{status}: {len(records)} files found.'
        if skipped:
            message += f' {skipped} files or folders could not be read.'
        self.statusBar().showMessage(message)
        if skipped:
            QMessageBox.warning(self, 'Some files were skipped', message)

    def scan_failed(self, message):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.statusBar().showMessage('Scan failed')
        QMessageBox.critical(self, 'Scan error', message)

    def scan_finished(self):
        self.open_button.setEnabled(True)
        self.scan_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

    def matching_files(self):
        return filter_files(self.records, self.search_box.text(), self.type_filter.currentText())

    def update_table(self, *_):
        matching = self.matching_files()
        self.file_table.setSortingEnabled(False)
        self.file_table.setRowCount(len(matching))
        for row, record in enumerate(matching):
            values = (record['name'], record['type'], readable_size(record['size']), record['location'])
            for col, value in enumerate(values):
                cell = QTableWidgetItem(str(value))
                cell.setData(Qt.ItemDataRole.UserRole, record['location'])
                self.file_table.setItem(row, col, cell)
        self.file_table.setSortingEnabled(True)
        self.count_label.setText(f'Showing {len(matching)} of {len(self.records)} files')

    def selected_path(self):
        row = self.file_table.currentRow()
        cell = self.file_table.item(row, 0) if row >= 0 else None
        return cell.data(Qt.ItemDataRole.UserRole) if cell else None

    def show_preview(self):
        path = self.selected_path()
        self.stop_audio()
        self.preview_label.clear()
        if not path:
            self.preview_label.setText('Select a file to see its details')
            return
        category = file_category(path)
        if category == 'Images':
            image = QPixmap(path)
            if not image.isNull():
                self.preview_label.setPixmap(image.scaled(
                    400, 360, Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation))
                return
        self.preview_label.setText(f'File: {Path(path).name}\nType: {category}\nPath: {path}')
        if category == 'Audio':
            self.audio_path = path
            self.play_button.setEnabled(True)

    def stop_audio(self):
        self.audio_player.stop()
        self.audio_player.setSource(QUrl())
        self.audio_path = None
        self.play_button.setEnabled(False)
        self.play_button.setText('Play Audio')

    def toggle_audio(self):
        path = self.audio_path
        if not path:
            QMessageBox.information(self, 'Select audio', 'Choose an audio file first.')
            return
        if not os.path.isfile(path):
            QMessageBox.warning(self, 'File missing', 'This audio file no longer exists.')
            self.stop_audio()
            return
        if self.audio_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.audio_player.pause()
        else:
            if self.audio_player.source().toLocalFile() != path:
                self.audio_player.setSource(QUrl.fromLocalFile(path))
            self.audio_player.play()

    def update_play_button(self, state):
        playing = state == QMediaPlayer.PlaybackState.PlayingState
        self.play_button.setText('Pause Audio' if playing else 'Play Audio')
        if self.audio_path:
            self.statusBar().showMessage('Playing audio' if playing else 'Audio paused or stopped')

    def change_volume(self, value):
        self.audio_output.setVolume(value / 100)
        self.volume_label.setText(f'Volume: {value}%')

    def audio_error(self, error, message):
        if error != QMediaPlayer.Error.NoError:
            self.statusBar().showMessage('Audio playback failed')
            QMessageBox.warning(self, 'Audio error', message or 'Unable to play this file.')

    def export_csv(self):
        if not self.records:
            QMessageBox.information(self, 'Nothing to export', 'Scan a folder first.')
            return
        destination, _ = QFileDialog.getSaveFileName(
            self, 'Save file report', 'file_report.csv', 'CSV files (*.csv)')
        if not destination:
            return
        try:
            save_file_report(destination, self.matching_files())
            self.statusBar().showMessage(f'Saved report: {destination}')
        except OSError as exc:
            QMessageBox.critical(self, 'Export failed', str(exc))

    def closeEvent(self, event):
        if self.scanner is not None and self.scanner.isRunning():
            QMessageBox.information(self, 'Scan in progress', 'Cancel the scan and close once it finishes.')
            event.ignore()
            return
        self.stop_audio()
        event.accept()
