from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSpinBox, QWidget
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QTextEdit
from PyQt5.QtCore import QCoreApplication
from PyQt5.Qt import QRect

from ..baseview import BaseView


class DNAProfile(BaseView):
    @staticmethod
    def new(xref: QTextEdit, mainWindow):
        w = QWidget()

        layout = QHBoxLayout()

        btn = QPushButton("New DNA profile")

        def create_profile():
            print(xref.text())
            profile = DNAProfile(xref.text())
            app = QCoreApplication.instance()
            app.mainwindow.add_window(profile)

        btn.clicked.connect(create_profile)

        layout.addWidget(btn)
        w.setLayout(layout)

        return w
    
    def __init__(self, xref, *args, **kwargs):
        self.xref = xref
        super().__init__(*args, **kwargs)

        # Name of profile person
        # List of found matches
        # List of potential matches

class View(BaseView):
    def __init__(self):
        super().__init__()
        self.display_name = "DNA"
    
    def initUi(self):
        pass
