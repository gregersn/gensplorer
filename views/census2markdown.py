from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QTextEdit, QLineEdit
from PyQt5.QtWidgets import QErrorMessage


from services import census


class View(QWidget):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.entry())
        self.layout.addWidget(self.output())
        self.setLayout(self.layout)
        self.error_dialog = QErrorMessage()

    def entry(self):
        layout = QHBoxLayout()
        self.data['url'] = QLineEdit()
        layout.addWidget(self.data['url'])
        btn = QPushButton("Get census")
        btn.clicked.connect(self.get_census)
        layout.addWidget(btn)
        return layout

    def output(self):
        self.data['output'] = QTextEdit()
        self.data['output'].mousePressEvent = self.copy_census
        return self.data['output']

    def get_census(self):
        url = self.data['url'].text()
        try:
            census_data = census.get_census(url)
            markdown = census.census_to_markdown(**census_data)
            self.data['output'].setText(markdown)
        except:
            self.show_error("Something went wrong when trying to get\n{}".format(url))
    
    def show_error(self, message):
            self.error_dialog.showMessage(message)

    def copy_census(self, event):
        self.data['output'].selectAll()
        self.data['output'].copy()
