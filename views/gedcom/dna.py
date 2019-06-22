from PyQt5.QtWidgets import QHBoxLayout, QPushButton
from PyQt5.QtWidgets import QRadioButton

from ..baseview import BaseView
from .peopletable import PeopleTable


class DNASearch(BaseView):
    def __init__(self, gedcom, parent=None):
        super().__init__(parent=parent)
        self.gedcom = gedcom

    def initUi(self):
        layout = QHBoxLayout()

        layout.addWidget(QRadioButton("Y-DNA"))
        layout.addWidget(QRadioButton("mtDNA"))

        searchbtn = QPushButton("Find")
        searchbtn.clicked.connect(self.execute_search)

        layout.addWidget(searchbtn)
        self.setLayout(layout)

    def execute_search(self):
        rootref = self.parent.data['search'].text()
        ydna = self.parent.gedcom.get_ydna(rootref)

        for p in ydna:
            print(p.name)

        t = PeopleTable()
        t.set_data(ydna)
        t.show()
