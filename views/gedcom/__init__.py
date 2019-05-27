#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QPushButton, QTextEdit, QLineEdit
from PyQt5.QtWidgets import QErrorMessage, QFileDialog
from PyQt5.QtWidgets import QCompleter
from PyQt5.Qt import QStringListModel, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

import os

from ..baseview import BaseView
from .snipper import Snipper
from .cousins import Cousins

from services import gedsnip
from services import settings


class PersonCompleter(QCompleter):
    ConcatenationRole = Qt.UserRole + 1

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.create_model(data)

    def pathFromIndex(self, ix):
        return ix.data(PersonCompleter.ConcatenationRole)

    def create_model(self, data):
        def addItems(parent, elements, t=""):
            for xref, name in elements:
                item = QStandardItem(name)
                data = xref
                item.setData(data)
                parent.appendRow(item)
        model = QStandardItemModel(self)
        addItems(model, data)
        self.setModel(model)


class View(BaseView):
    def __init__(self):
        self.gedcom = None

        super().__init__()

        self.datafolder = settings.get("datafolder") or ""

        if settings.get("gedcomfile"):
            self.readgedcom(settings.get("gedcomfile"))

    # Layout functions

    def initUi(self):
        self.layout = QVBoxLayout()

        # File selector for choosing ged-file
        self.layout.addLayout(self.opengedcom())

        # Search box for finding the right person as root
        self.layout.addLayout(self.searchbox())
        # Options for what to include

        # self.layout.addLayout(self.functions())
        function_layout = QHBoxLayout()
        function_layout.addWidget(Snipper(self.gedcom, parent=self))
        function_layout.addWidget(Cousins(self.gedcom, parent=self))

        self.layout.addLayout(function_layout)
        self.setLayout(self.layout)

    def opengedcom(self):
        layout = QHBoxLayout()
        
        layout.addWidget(QLabel("Gedcom file:"))
        self.data['filename'] = QLineEdit()
        layout.addWidget(self.data['filename'])

        openbtn = QPushButton("Open gedcom")
        openbtn.clicked.connect(self.openFileNameDialog)
        layout.addWidget(openbtn)

        return layout

    def searchbox(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Root person:"))
        self.data['search'] = QLineEdit()
        layout.addWidget(self.data['search'])

        return layout

    def functions(self):
        layout = QHBoxLayout()
        # layout.addLayout(self.snipfunction())
        return layout

    def updatesearchbox(self):
        self.completer = PersonCompleter(self.gedcom.namelist, self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.activated.connect(self.activated)
        self.data['search'].setCompleter(self.completer)

    # Event handlers

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Open Gedcom",
                                                  self.datafolder,
                                                  "Gedcom files (*.ged);;All files (*)",
                                                  options=options)

        if not filename:
            return

        assert os.path.isfile(filename)

        self.datafolder = os.path.dirname(filename)
        settings.set("datafolder", self.datafolder)

        settings.set("gedcomfile", filename)

        self.readgedcom(filename)

    def saveFileNameDialog(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Gedcom snippet",
                                                  self.datafolder,
                                                  "Gedcom files (*.ged);;All files (*)",
                                                  options=options)
        if filename:
            print(filename)
            return filename

        return None

    def readgedcom(self, filename):
        self.data['filename'].setText(filename)
        self.gedcom = gedsnip.GedcomManipulator(filename)
        self.updatesearchbox()

    def activated(self, *args, **kwargs):
        pass
