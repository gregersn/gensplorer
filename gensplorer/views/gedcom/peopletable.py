from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.Qt import QRect


class PeopleTable(QWidget):
    def set_data(self, data):
        layout = QHBoxLayout()

        table = QTableWidget(self)
        table.setRowCount(len(data))
        table.setColumnCount(2)

        for index, person in enumerate(data):
            name = person.name
            table.setItem(index, 0, QTableWidgetItem(name[0]))
            table.setItem(index, 1, QTableWidgetItem(name[1]))

        layout.addWidget(table)

        self.setGeometry(QRect(100, 100, 400, 200))

        self.setLayout(layout)


