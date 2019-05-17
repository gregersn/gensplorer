from PyQt5.QtWidgets import (QMainWindow,
                             QWidget,
                             QTabWidget,
                             QHBoxLayout,
                             QVBoxLayout,
                             QPushButton,
                             QLineEdit,
                             QTextEdit)

from PyQt5.QtWidgets import QApplication

from services import census


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.initUi()

    def initUi(self):
        self.resize(640, 480)
        self.central_widget = QWidget()

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addLayout(self.entry())
        self.layout.addWidget(self.output())

        self.setCentralWidget(self.central_widget)

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
        print("Get census")
        url = self.data['url'].text()
        census_data = census.get_census(url)
        markdown = census.census_to_markdown(**census_data)
        self.data['output'].setText(markdown)
    
    def copy_census(self, event):
        self.data['output'].selectAll()
        self.data['output'].copy()





if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exit(app.exec_())
