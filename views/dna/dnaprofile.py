import os
import json

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSpinBox, QWidget
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QTextEdit, QLabel, QListView
from PyQt5.QtCore import QCoreApplication
from PyQt5.Qt import QRect
from PyQt5.QtCore import QUrl, QAbstractItemModel, QAbstractListModel, Qt
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5 import uic

from ..baseview import BaseView
from services import gedsnip
from services.settings import SETTINGS
from views.gedcom.widgets import PersonCompleter

qt_creator_file = "views/dna/dnaprofile.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class MatchListModel(QAbstractListModel):
    def __init__(self, *args, matches=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.matches = matches or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.matches[index.row()]['name']

        if role == Qt.EditRole:
            return self.matches[index.row()]

    def rowCount(self, index):
        return len(self.matches)

    def add(self, data):
        self.matches.append(data)
    
    def xref_index(self, xref):
        for idx, match in enumerate(self.matches):
            if match['xref'] == xref:
                return idx



"""
class MatchModel(QAbstractItemModel):
    def __init__(self, *args, xref=None, dna=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.xref = xref or None
        self.dna = dna or {'ftdna': '', 'myheritage': ''}

    def add_dna(self, service, data):
        self.dna[service] = data
    
    def to_dict(self):
        return {
            'xref': self.xref,
            'dna': self.dna
        }
"""


class Model(QAbstractItemModel):
    def __init__(self, *args, xref=None, datafolder=".", **kwargs):
        super().__init__(*args, **kwargs)
        self.xref = xref or None
        self.datafolder = datafolder
        self.manipulator = gedsnip.init_manipulator()
        self.matches = MatchListModel(matches=self.load())

    def get_by_xref(self, xref):
        return self.manipulator.gedcom[xref]

    @property
    def name(self):
        return " ".join(self.manipulator.gedcom[self.xref].name)

    def add_match(self, data):
        self.matches.add(data)
        self.matches.layoutChanged.emit()

    def save(self):
        if len(self.matches.matches) < 1:
            return

        filename = os.path.join(self.datafolder, "matches_{}.json".format(self.xref))
        with open(filename, 'w', newline="\n") as f:
            json.dump(self.matches.matches, f, indent=4)

    def load(self):
        filename = os.path.join(self.datafolder, "matches_{}.json".format(self.xref))
        if not os.path.isfile(filename):
            return []

        with open(filename, 'r') as f:
            return json.load(f)


class View(BaseView, Ui_MainWindow):
    @staticmethod
    def new(xref: QTextEdit, mainWindow):
        w = QWidget()

        layout = QHBoxLayout()

        btn = QPushButton("DNA profile")

        def create_profile():
            print(xref.text())
            profile = View(xref.text())
            app = QCoreApplication.instance()
            app.mainwindow.add_window(profile)

        btn.clicked.connect(create_profile)

        layout.addWidget(btn)
        w.setLayout(layout)

        return w

    def __init__(self, xref, *args, **kwargs):
        self.xref = xref
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.model = Model(xref=self.xref, datafolder=SETTINGS.get('datafolder'))
        # self.listView.setModel(self.model)
        self.nameLabel.setText(self.model.name)
        self.matchListView.setModel(self.model.matches)
        self.matchListView.selectionModel().currentChanged.connect(self.showmatch)
        self.matchListView.clicked.connect(self.showmatch)

        def selectedPerson(xref, *args, **kwargs):
            person = self.model.get_by_xref(xref)
            # Check if there already is a match with same xref
            match = self.model.matches.xref_index(xref)
            if match is not None:
                self.showmatch(match, None)
            else:
                self.matchName.setText(" ".join(person.name))
                self.matchDataFTDNA.setPlainText("")
                self.matchDataMyHeritage.setPlainText("")
    
        completer = PersonCompleter(self.model.manipulator.namelist, self)
        completer.activated.connect(selectedPerson)
        self.matchXREF.setCompleter(completer)

        self.btnAddMatch.clicked.connect(self.addmatch)

        self.okButton.clicked.connect(self.close)

    def add(self):
        text = self.xrefEdit.text()
        if text:
            self.model.todos.append((False, text))
            self.model.layoutChanged.emit()
            self.xrefEdit.setText("")

    def close(self):
        self.model.save()
        app = QCoreApplication.instance()
        app.mainwindow.close_window(self.parentWidget())

    def showmatch(self, current, previous=None):
        data = self.model.matches.data(current, Qt.EditRole)
        self.matchDataFTDNA.setPlainText(data.get('ftdna', ''))
        self.matchDataFTDNA.setLineWrapMode(0)
        self.matchDataMyHeritage.setPlainText(data.get('myheritage', ''))
        self.matchDataMyHeritage.setLineWrapMode(0)
        self.matchXREF.setText(data.get('xref', ''))
        self.matchName.setText(data.get('name', ''))

    def addmatch(self):
        xref = self.matchXREF.text()
        name = self.matchName.text()
        ftdna = self.matchDataFTDNA.toPlainText()
        myheritage = self.matchDataMyHeritage.toPlainText()

        self.model.add_match({
            'xref': xref,
            'name': name,
            'ftdna': ftdna,
            'myheritage': myheritage
        })

        self.model.layoutChanged.emit()

