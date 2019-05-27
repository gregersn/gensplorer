from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGroupBox, QCheckBox

from ..baseview import BaseView


class Snipper(BaseView):
    def __init__(self, gedcom, parent=None):
        self._options = {}
        super().__init__(parent=parent)

    def initUi(self):
        layout = QVBoxLayout()
        snipbtn = QPushButton("Snip")
        snipbtn.clicked.connect(self.execute_snip)
        layout.addWidget(self.init_options())
        layout.addWidget(snipbtn)
        self.setLayout(layout)

    def execute_snip(self):
        print(self.options)
        filename = self.parent.saveFileNameDialog()
        if filename:
            output = self.parent.gedcom.get_branch(self.parent.data['search'].text(), **self.options)
            output.save(filename, overwrite=True)

    def init_options(self):
        groupbox = QGroupBox("Snipping options")

        self._options['ancestors'] = QCheckBox("Include ancestors")
        self._options['siblings'] = QCheckBox("Include siblings")
        self._options['descendants'] = QCheckBox("Include descendants")
        
        vbox = QVBoxLayout()
        for k, v in self._options.items():
            vbox.addWidget(v)
        groupbox.setLayout(vbox)
        return groupbox

    @property
    def options(self):
        return {k: v.isChecked() for k, v in self._options.items()}
