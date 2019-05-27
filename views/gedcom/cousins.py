from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSpinBox, QWidget
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel
from PyQt5.Qt import QRect

from ..baseview import BaseView


class CousinsTable(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Cousins(BaseView):
    def __init__(self, gedcom, parent=None):
        super().__init__(parent=parent)
        self.gedcom = gedcom

    def initUi(self):
        layout = QHBoxLayout()

        searchbtn = QPushButton("Cousins")
        searchbtn.clicked.connect(self.execute_search)

        self.cousinlevel = QSpinBox(self)
        self.cousinlevel.setMinimum(1)
        self.cousinlevel.setMaximum(10)
        self.cousinlevel.setValue(1)

        layout.addWidget(self.cousinlevel)
        layout.addWidget(searchbtn)
        self.setLayout(layout)

    def execute_search(self):
        rootref = self.parent.data['search'].text()
        level = self.cousinlevel.value()
        cousins = self.parent.gedcom.get_cousins(rootref, level)

        self.show_result(cousins)

    def show_result(self, cousins):
        self.w = CousinsTable()
        self.w.setGeometry(QRect(100, 100, 400, 200))

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Cousins"))

        table = QTableWidget(self)
        table.setRowCount(len(cousins))
        table.setColumnCount(2)
        for index, cousin in enumerate(cousins):
            name = cousin.name
            table.setItem(index, 0, QTableWidgetItem(name[0]))
            table.setItem(index, 1, QTableWidgetItem(name[1]))
        
        layout.addWidget(table)
        self.w.setLayout(layout)

        self.w.show()
