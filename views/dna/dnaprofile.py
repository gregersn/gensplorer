from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSpinBox, QWidget
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QTextEdit, QLabel, QListView
from PyQt5.QtCore import QCoreApplication
from PyQt5.Qt import QRect
from PyQt5.QtCore import QUrl, QAbstractItemModel, QAbstractListModel, Qt
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5 import uic

from ..baseview import BaseView
from services import gedsnip
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
    def __init__(self, *args, xref=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.xref = xref or None
        self.manipulator = gedsnip.init_manipulator()
        self.matches = MatchListModel(matches=[{'name': 'Match name', 'dnaFTDNA': 'Some dna data'}])
        
    def get_by_xref(self, xref):
        return self.manipulator.gedcom[xref]

    @property
    def name(self):
        return " ".join(self.manipulator.gedcom[self.xref].name)
    

    def add_match(self, data):
        self.matches.add(data)
        self.matches.layoutChanged.emit()


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
        self.model = Model(xref=self.xref)
        # self.listView.setModel(self.model)
        self.nameLabel.setText(self.model.name)
        self.matchListView.setModel(self.model.matches)
        self.matchListView.selectionModel().currentChanged.connect(self.showmatch)

        def selectedPerson(*args, **kwargs):
            person = self.model.get_by_xref(args[0])
            self.matchName.setText(" ".join(person.name))

        completer = PersonCompleter(self.model.manipulator.namelist, self)
        completer.activated.connect(selectedPerson)
        self.matchXREF.setCompleter(completer)

        self.btnAddMatch.clicked.connect(self.addmatch)

    def add(self):
        text = self.xrefEdit.text()
        if text:
            self.model.todos.append((False, text))
            self.model.layoutChanged.emit()
            self.xrefEdit.setText("")

    def showmatch(self, current, previous):
        data = self.model.matches.data(current, Qt.EditRole)
        self.matchDataFTDNA.setPlainText(data.get('dnaFTDNA', ''))
        self.matchDataMyHeritage.setPlainText(data.get('dnaMyHeritage', ''))
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
            'myheritage': myheritage,
            'dna': dna
        })

        self.model.layoutChanged.emit()

