from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog

Ui_Dialog, QtBaseClass = uic.loadUiType("./UI/add_tester.ui")

print(type(QtBaseClass))
print(QtBaseClass)


class Ui_AddTesterDialog(QtBaseClass):
    def __init__(self, parent=None, *args, **kwargs):
        super(Ui_AddTesterDialog, self).__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.tester = {}

        self.ui.btnFtdna.clicked.connect(self.browseFtdna)
        self.ui.btnMyheritage.clicked.connect(self.browseMyheritage)

        self.ui.buttonBox.accepted.connect(self.submitclose)
        self.ui.buttonBox.rejected.connect(self.close)
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
            'xref': self.ui.inXref.text()
        }
        self.accept()
