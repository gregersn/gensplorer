from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import QStringListModel, Qt, QAbstractTableModel, QModelIndex
from PyQt5.Qt import QStandardItemModel

Ui_Dialog, QtBaseClass = uic.loadUiType("./UI/add_tester.ui")


class XrefCompleter(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)

    def pathFromIndex(self, ix):
        return str(ix.data(Qt.UserRole))


class XrefModel(QAbstractTableModel):
    def __init__(self, *args, people=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.people = people

    def data(self, index, role):
        key, value = self.people[index.row()]
        if role == Qt.DisplayRole:
            return value
        elif role == Qt.EditRole:
            return value
        elif role == Qt.UserRole:
            # return key.replace('@', '')
            return key
        else:
            pass

    def index(self, row, col, parent=None):
        return self.createIndex(row, col)

    def rowCount(self, index):
        return len(self.people)

    def columnCount(self, index):
        return 2

    def headerData(self, section, role):
        print("HeaderData")


class Ui_AddTesterDialog(QtBaseClass):
    def __init__(self, parent, gedcom, *args, **kwargs):
        super(Ui_AddTesterDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.gedcom = gedcom

        self.tester = {}

        self.ui.btnFtdna.clicked.connect(self.browseFtdna)
        self.ui.btnMyheritage.clicked.connect(self.browseMyheritage)

        self.ui.buttonBox.accepted.connect(self.submitclose)
        self.ui.buttonBox.rejected.connect(self.close)

        inXref = self.ui.inXref

        completer = XrefCompleter()
        inXref.setCompleter(completer)

        self.xrefmodel = XrefModel(people=self.gedcom.namelist)
        completer.setModel(self.xrefmodel)

        self.show()

    def browseFtdna(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", '')
        if len(fname[0]) > 0:
            self.ui.inFtdna.setText(fname[0])

    def browseMyheritage(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", '')
        if len(fname[0]) > 0:
            self.ui.inMyheritage.setText(fname[0])

    def submitclose(self):
        self.tester = {
            'name': self.ui.inName.text(),
            'shared_segments': {
                'ftdna': self.ui.inFtdna.text(),
                'myheritage': self.ui.inMyheritage.text()
            },
            'xref': self.ui.inXref.text().replace('@', '')
        }
        valid = True
        if len(self.ui.inName.text()) < 1:
            valid = False

        if len(self.ui.inXref.text()) < 1:
            valid = False
        else:
            xrefmatch = self.xrefmodel.match(self.xrefmodel.index(0, 0),
                                             Qt.UserRole,
                                             self.ui.inXref.text())
            if len(xrefmatch) != 1:
                valid = False

        if valid:
            self.accept()
