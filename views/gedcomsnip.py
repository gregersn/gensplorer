#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QTextEdit, QLineEdit
from PyQt5.QtWidgets import QErrorMessage

from .baseview import BaseView

class View(BaseView):
    def initUi(self):
        # File selector for choosing ged-file
        # Search box for finding the right person as root
        # Options for what to include
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)
