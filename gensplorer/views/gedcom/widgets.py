#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt
from PyQt5.Qt import QStandardItem, QStandardItemModel


class PersonCompleter(QCompleter):
    ConcatenationRole = Qt.UserRole + 1

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.create_model(data)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)

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
