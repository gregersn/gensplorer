import os
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtCore import Qt

from .common import XrefCompleter, XrefModel

Ui_Dialog, QtBaseClass = uic.loadUiType("./UI/add_tester.ui")


class Ui_AddTesterDialog(QtBaseClass):
    def __init__(self, parent, gedcom, *args, edit=None, **kwargs):
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

        if edit is not None:
            self.edit(edit)

        self.show()

    def edit(self, edit):
        self.ui.inXref.setText("@{}@".format(edit['xref']))
        self.ui.inName.setText(edit['name'])
        self.ui.inName.setReadOnly(True)
        if 'shared_segments' in edit:
            if 'myheritage' in edit['shared_segments']:
                self.ui.inMyheritage.setText(edit['shared_segments']['myheritage'])

            if 'ftdna' in edit['shared_segments']:
                self.ui.inFtdna.setText(edit['shared_segments']['ftdna'])

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

        if len(self.ui.inFtdna.text()) > 1:
            if not os.path.isfile(self.ui.inFtdna.text()):
                valid = False

        if len(self.ui.inMyheritage.text()) > 1:
            if not os.path.isfile(self.ui.inMyheritage.text()):
                valid = False

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
