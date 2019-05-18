from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QErrorMessage

class BaseView(QWidget):
    def __init__(self):
        super().__init__()
        self.error_dialog = QErrorMessage()
        self.data = {}
        self.initUi()
    
    def initUi(self):
        pass
    
    def show_error(self, message):
            self.error_dialog.showMessage(message)
