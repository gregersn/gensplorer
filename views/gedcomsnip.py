#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QTextEdit, QLineEdit
from PyQt5.QtWidgets import QErrorMessage, QFileDialog
from PyQt5.QtWidgets import QCompleter
from PyQt5.Qt import QStringListModel
from PyQt5.QtCore import Qt

import os

from .baseview import BaseView

from services import gedsnip
from services import settings


class View(BaseView):
    def __init__(self):
        self.gedcom = None

        super().__init__()

        self.datafolder = settings.get("datafolder") or ""

    # Layout functions

    def initUi(self):
        self.layout = QVBoxLayout()

        # File selector for choosing ged-file
        self.layout.addLayout(self.opengedcom())

        # Search box for finding the right person as root
        self.layout.addLayout(self.searchbox())
        # Options for what to include

        self.setLayout(self.layout)
    
    def opengedcom(self):
        layout = QHBoxLayout()
        
        self.data['filename'] = QLineEdit()
        layout.addWidget(self.data['filename'])

        openbtn = QPushButton("Open gedcom")
        openbtn.clicked.connect(self.openFileNameDialog)
        layout.addWidget(openbtn)

        return layout
    
    def searchbox(self):
        layout = QHBoxLayout()
        self.data['search'] = QLineEdit()
        layout.addWidget(self.data['search'])

        searchbtn = QPushButton("Search")
        searchbtn.clicked.connect(self.execute_search)

        layout.addWidget(searchbtn)

        return layout
    
    def updatesearchbox(self):
        completer = QCompleter()

        model = QStringListModel()
        model.setStringList(self.gedcom.namelist)

        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)

        self.data['search'].setCompleter(completer)


    # Event handlers
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Open Gedcom", self.datafolder, "Gedcom files (*.ged);;All files (*)", options=options)

        if not filename:
            return

        assert os.path.isfile(filename)

        self.datafolder = os.path.dirname(filename)
        settings.set("datafolder", self.datafolder)

        self.data['filename'].setText(filename)

        self.gedcom = gedsnip.GedcomManipulator(filename)
        self.updatesearchbox()

    def execute_search(self):
        pass
