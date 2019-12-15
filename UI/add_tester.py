from PyQt5 import uic

Ui_Dialog, QtBaseClass = uic.loadUiType("./UI/add_tester.ui")

print(type(QtBaseClass))
print(QtBaseClass)


class Ui_AddTesterDialog(QtBaseClass):
    def __init__(self, parent=None, *args, **kwargs):
        super(Ui_AddTesterDialog, self).__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.tester = {}

        self.ui.buttonBox.accepted.connect(self.submitclose)
        self.ui.buttonBox.rejected.connect(self.close)
        self.show()

    def submitclose(self):
        self.tester = {
            'name': self.ui.inName,
            'ftdna': self.ui.inFtdna,
            'myheritage': self.ui.inMyheritage,
            'xref': self.ui.inXref
        }
        self.accept()

