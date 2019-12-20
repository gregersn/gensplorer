#!/usr/bin/env python3
import os
import sys
import json

from PyQt5.QtWidgets import (QApplication,
                             QLabel, QWidget,
                             QHBoxLayout,
                             qApp,
                             QLineEdit, QPushButton,
                             QFileDialog)

from PyQt5.QtCore import QAbstractListModel, QAbstractTableModel
from PyQt5 import QtCore
from PyQt5 import uic

from gensplorer.services.dna.match import Matches
from gensplorer.services.gedsnip import GedcomManipulator

from UI.add_tester import Ui_AddTesterDialog
from UI.add_match import Ui_AddMatchDialog

Ui_Window, QtBaseClass = uic.loadUiType("./UI/painter.ui")


class ModelTesters(QAbstractListModel):
    """Model to hold testers."""
    def __init__(self, *args, testers=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.testers = testers

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.testers[index.row()]['name']

    def rowCount(self, index):
        return len(self.testers)


class ModelMatches(QAbstractTableModel):
    """Model to hold matches."""
    def __init__(self, *args, matches=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.matches = matches

    def data(self, index, role):
        key = sorted(self.matches.keys())[index.row()]
        match = self.matches[key]
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return match['xref']
            if index.column() == 1:
                return match['ftdna'] if 'ftdna' in match else ''
            if index.column() == 2:
                return match['myheritage'] if 'myheritage' in match else ''

    def index(self, row, col, parent=None):
        return self.createIndex(row, col)

    def rowCount(self, index):
        return len(self.matches)

    def columnCount(self, index):
        return 3


class PainterGUI(QtBaseClass):
    def __init__(self, arguments, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = {}
        self.matches = None
        self.gedcom = None
        self.ui = Ui_Window()
        self.ui.setupUi(self)

        self.ui.btnOpenGedcom.clicked.connect(self.openGedcomDialog)

        self.ui.btnAddTester.clicked.connect(self.add_tester)
        self.ui.btnEditTester.clicked.connect(self.edit_tester)
        self.ui.btnAddMatch.clicked.connect(self.add_match)
        self.ui.btnAddMatch.setEnabled(False)
        self.ui.inputGedcom.textChanged.connect(self.update_data)

        self.initmenu()

        self.show()

        if len(arguments) > 1:
            self.load_settings(arguments[1])

    def update_data(self):
        self.data['gedfile'] = self.ui.inputGedcom.text()

    def add_tester(self):
        dialog = Ui_AddTesterDialog(self, self.gedcom)
        if dialog.exec_():
            self.data['testers'].append(dialog.tester)
            self.model_testers.layoutChanged.emit()

    def edit_tester(self):
        dialog = Ui_AddTesterDialog(self, self.gedcom, edit=self.selected_tester)
        if dialog.exec_():
            tester = self.matches.get_tester(self.selected_tester['name'])
            tester['xref'] = dialog.tester['xref']
            if 'shared_segments' not in tester:
                tester['shared_segments'] = {}
            tester['shared_segments']['myheritage'] = dialog.tester['shared_segments']['myheritage']
            tester['shared_segments']['ftdna'] = dialog.tester['shared_segments']['ftdna']

    def add_match(self):
        dialog = Ui_AddMatchDialog(self, self.gedcom, self.selected_tester)
        if dialog.exec_():
            self.matches.add_match(self.selected_tester, **dialog.matcher)
            self.model_matches.layoutChanged.emit()

    def select_tester(self, current, previous):
        if current.row() > -1:
            self.ui.btnAddMatch.setEnabled(True)
            self.ui.btnEditTester.setEnabled(True)
        self.selected_tester = self.data['testers'][current.row()]
        matches = self.matches.get_matches(self.selected_tester['name'])
        self.model_matches.matches = matches
        self.model_matches.layoutChanged.emit()

    def load_settings(self, filename):
        self.matches = Matches(filename)
        self.data = self.matches.data
        self.cwd = os.getcwd()
        self.workingdirectory = os.path.dirname(filename)
        os.chdir(self.workingdirectory)
        self.settings_filename = os.path.basename(filename)
        print(self.settings_filename)

        self.ui.inputGedcom.setText(self.data['gedfile'])
        self.gedcom = GedcomManipulator(self.data['gedfile'])

        tester_list = self.ui.listTesters
        matches_list = self.ui.listMatches
        if 'testers' in self.data:
            self.model_testers = ModelTesters(tester_list, testers=self.data['testers'])
            tester_list.setModel(self.model_testers)
            self.ui.listTesters.selectionModel().currentChanged.connect(self.select_tester)

            self.model_matches = ModelMatches(matches_list, matches={})
            matches_list.setModel(self.model_matches)

    def save_settings(self, filename=None):
        if filename is None:
            filename = self.settings_filename
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def openDialog(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", '')
        # self.matches = Matches(fname[0])

        # tester_list = self.ui.listTesters
        if len(fname[0]) > 0:
            self.load_settings(fname[0])

    def saveAsDialog(self):
        fname = QFileDialog.getSaveFileName(self, "Save file", '')
        if len(fname[0]) > 0:
            self.save_settings(fname[0])

    def initmenu(self):
        self.ui.actionE_xit.triggered.connect(qApp.quit)
        self.ui.action_Open.triggered.connect(self.openDialog)
        self.ui.action_Save.triggered.connect(lambda: self.save_settings())
        self.ui.actionSave_as.triggered.connect(self.saveAsDialog)

    def openGedcomDialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Open Gedcom",
                                                  '.',
                                                  "Gedcom files (*.ged);;All files (*)",
                                                  options=options)

        if not filename:
            return

        assert os.path.isfile(filename)

        self.datafolder = os.path.dirname(filename)
        self.ui.inputGedcom.setText(filename)
        # settings.set("datafolder", self.datafolder)

        # settings.set("gedcomfile", filename)

        # self.readgedcom(filename)

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

    def opengedcom(self):
        layout = QHBoxLayout()

        layout.addWidget(QLabel("Gedcom file:"))
        self.data['filename'] = QLineEdit()
        layout.addWidget(self.data['filename'])

        openbtn = QPushButton("Open gedcom")
        openbtn.clicked.connect(self.openGedcomDialog)
        layout.addWidget(openbtn)

        return layout

    def initUI(self):
        self.initmenu()

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("DNAMapper")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        centralLayout = QHBoxLayout()
        centralWidget.setLayout(centralLayout)

        centralLayout.addLayout(self.opengedcom())

        self.show()


def main():
    app = QApplication(sys.argv)
    pgui = PainterGUI(app.arguments())
    sys.exit(app.exec_())
    """
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    """


if __name__ == "__main__":
    main()
