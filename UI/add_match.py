from PyQt5 import uic
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import QCompleter

from .common import XrefCompleter, XrefModel

from gensplorer.services.dna import DNAProvider

Ui_Dialog, QtBaseClass = uic.loadUiType("./UI/add_match.ui")


class Ui_AddMatchDialog(QtBaseClass):
    def __init__(self, parent, gedcom, tester, *args, **kwargs):
        super(Ui_AddMatchDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.gedcom = gedcom
        self.tester = tester

        if 'shared_segments' in self.tester:
            shared_segments = self.tester['shared_segments']
            if 'myheritage' in shared_segments:
                myheritage_data = [m['matchname']
                                   for m in DNAProvider.parse_matchfile('myheritage', shared_segments['myheritage'])]

                edit = self.ui.inMyheritage
                completer = QCompleter()
                completer.setCaseSensitivity(Qt.CaseInsensitive)
                completer.setFilterMode(Qt.MatchContains)
                edit.setCompleter(completer)

                model = QStringListModel()
                completer.setModel(model)
                model.setStringList(myheritage_data)

            if 'ftdna' in shared_segments:
                ftdna_data = [m['matchname']
                              for m in DNAProvider.parse_matchfile('ftdna', shared_segments['ftdna'])]

                edit = self.ui.inFtdna
                completer = QCompleter()
                completer.setCaseSensitivity(Qt.CaseInsensitive)
                edit.setCompleter(completer)

                model = QStringListModel()
                completer.setModel(model)
                model.setStringList(ftdna_data)

        self.matcher = {}

        self.ui.buttonBox.accepted.connect(self.submitclose)
        self.ui.buttonBox.rejected.connect(self.close)

        inXref = self.ui.inXref

        completer = XrefCompleter()
        inXref.setCompleter(completer)

        self.xrefmodel = XrefModel(people=self.gedcom.namelist)
        completer.setModel(self.xrefmodel)

        self.show()

    def submitclose(self):
        self.matcher = {
            'xref': self.ui.inXref.text().replace('@', ''),
            'ftdna': self.ui.inFtdna.text(),
            'myheritage': self.ui.inMyheritage.text()
        }

        valid = True

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
