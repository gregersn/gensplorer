import os

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSpinBox, QWidget
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QTextEdit, QLabel
from PyQt5.QtCore import QCoreApplication
from PyQt5.Qt import QRect
from PyQt5.QtCore import QUrl
from PyQt5.QtQuickWidgets import QQuickWidget

from ..baseview import BaseView



class View(BaseView):
    def __init__(self):
        super().__init__()
        self.display_name = "DNA"

    def initUi(self):
        pass
