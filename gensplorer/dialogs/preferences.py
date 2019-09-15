"""Preferences dialog handling."""
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton


class Preferences(QDialog):
    def __init__(self, settings, *args, **kwargs):
        super(Preferences, self).__init__(*args, **kwargs)
        self.settings = settings
        self.data = {}
        self.initUi()

    def initUi(self):
        layout = QVBoxLayout()
        layout.addLayout(self.opengedcom())
        self.setLayout(layout)

    def opengedcom(self):
        layout = QHBoxLayout()

        layout.addWidget(QLabel("Gedcom file:"))
        self.data['filename'] = QLineEdit()
        layout.addWidget(self.data['filename'])

        openbtn = QPushButton("Open gedcom")
        # openbtn.clicked.connect(self.openFileNameDialog)
        layout.addWidget(openbtn)

        return layout
