#!/usr/bin/env python3
import os
import sys
import json

from PyQt5.QtWidgets import (QApplication,
                             QLabel, QWidget,
                             QVBoxLayout, QHBoxLayout, QAction,
                             qApp, QMainWindow,
                             QLineEdit, QPushButton,
                             QFileDialog)

from PyQt5.QtGui import (QStandardItemModel, QStandardItem)
from PyQt5 import uic

from UI.add_tester import Ui_AddTesterDialog

# from UI.painter import Ui_MainWindow
Ui_Window, QtBaseClass = uic.loadUiType("./UI/painter.ui")

# from gensplorer.services.dna.match import Matches


class PainterGUI(QtBaseClass):
    def __init__(self, arguments, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = {}
        self.matches = None
        self.ui = Ui_Window()
        self.ui.setupUi(self)

        self.ui.btnOpenGedcom.clicked.connect(self.openGedcomDialog)

        self.ui.btnAddTester.clicked.connect(self.add_tester)

        self.initmenu()

        self.show()

        if len(arguments) > 1:
            self.load_settings(arguments[1])

    def add_tester(self):
        dialog = Ui_AddTesterDialog(self)
        if dialog.exec_():
            print(dialog.tester)

    def load_settings(self, filename):
        with open(filename, 'r') as f:
            self.data = json.load(f)

        tester_list = self.ui.listTesters
        model = QStandardItemModel(tester_list)

        if 'testers' in self.data:
            for tester in self.data['testers']:
                item = QStandardItem(tester['name'])
                model.appendRow(item)
        tester_list.setModel(model)

    def save_settings(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f)

    def openDialog(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", '')
        # self.matches = Matches(fname[0])

        # tester_list = self.ui.listTesters
        if len(fname[0]) > 0:
            self.load_settings(fname[0])

    def saveDialog(self):
        fname = QFileDialog.getSaveFileName(self, "Save file", '')
        if len(fname[0]) > 0:
            self.save_settings(fname[0])

    def initmenu(self):
        self.ui.actionE_xit.triggered.connect(qApp.quit)
        self.ui.action_Open.triggered.connect(self.openDialog)
        self.ui.action_Save.triggered.connect(self.saveDialog)
        self.ui.actionSave_as.triggered.connect(self.saveDialog)

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
