from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt, QAbstractTableModel


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
