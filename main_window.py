from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QComboBox, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QProgressBar,
    QPushButton, QTableWidget, QVBoxLayout, QWidget, QHeaderView, QSlider,
    QAbstractItemView,
)


class MainWindow(QMainWindow):
    """Only creates the visible controls. Actions live in controller.py."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Smart File & Media Manager')
        self.resize(1200, 720)
        root = QWidget()
        layout = QVBoxLayout(root)

        actions = QHBoxLayout()
        self.open_button = QPushButton('Open Folder')
        self.scan_button = QPushButton('Start Scan')
        self.cancel_button = QPushButton('Cancel Scan')
        self.cancel_button.setEnabled(False)
        self.export_button = QPushButton('Export CSV')
        for button in (self.open_button, self.scan_button, self.cancel_button, self.export_button):
            actions.addWidget(button)
        actions.addStretch()
        layout.addLayout(actions)

        self.folder_label = QLabel('No folder selected')
        self.folder_label.setWordWrap(True)
        layout.addWidget(self.folder_label)

        filters = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText('Search file names...')
        self.type_filter = QComboBox()
        self.type_filter.addItems(['All files', 'Images', 'Audio', 'Documents', 'Other'])
        filters.addWidget(self.search_box, 3)
        filters.addWidget(self.type_filter, 1)
        layout.addLayout(filters)

        center = QHBoxLayout()
        self.file_table = QTableWidget(0, 4)
        self.file_table.setHorizontalHeaderLabels(['Name', 'Type', 'Size', 'Location'])
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.file_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.file_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        for column, width in enumerate((330, 95, 95, 330)):
            self.file_table.setColumnWidth(column, width)
        center.addWidget(self.file_table, 3)

        right = QVBoxLayout()
        right.addWidget(QLabel('Media Preview'))
        self.preview_label = QLabel('Select a file to see its details')
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setWordWrap(True)
        self.preview_label.setMinimumSize(250, 260)
        self.preview_label.setStyleSheet('border: 1px solid #999; padding: 12px;')
        right.addWidget(self.preview_label, 1)
        self.play_button = QPushButton('Play Audio')
        self.play_button.setEnabled(False)
        right.addWidget(self.play_button)
        self.volume_label = QLabel('Volume: 70%')
        right.addWidget(self.volume_label)
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        right.addWidget(self.volume_slider)
        center.addLayout(right, 2)
        layout.addLayout(center)

        layout.addWidget(QLabel('Scan Progress'))
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        self.count_label = QLabel('0 files')
        layout.addWidget(self.count_label)
        self.setCentralWidget(root)
        self.statusBar().showMessage('Ready')

        file_menu = self.menuBar().addMenu('File')
        self.open_action = QAction('Open Folder', self)
        self.export_action = QAction('Export CSV', self)
        self.exit_action = QAction('Exit', self)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.export_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        help_menu = self.menuBar().addMenu('Help')
        self.about_action = QAction('About', self)
        help_menu.addAction(self.about_action)
