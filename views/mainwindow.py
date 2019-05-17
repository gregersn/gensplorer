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
from .tabwidget import TabWidget
from .census2markdown import View as CensusView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.resize(640, 480)
        self.central_widget = TabWidget()

        self.central_widget.add_tab(CensusView(), "Census")
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exit(app.exec_())
