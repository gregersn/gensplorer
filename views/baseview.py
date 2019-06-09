from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QErrorMessage


class BaseView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.error_dialog = QErrorMessage()
        self.data = {}
        self.initUi()
    
    def initUi(self):
        pass
    
    def show_error(self, message):
            self.error_dialog.showMessage(message)


def show_widget(widget: QWidget):
    import sys
    from PyQt5.QtWidgets import QApplication
    
    APP = QApplication(sys.argv)
    w  = widget()
    w.show()
    sys.exit(APP.exec_())

if __name__ == "__main__":
    show_widget(BaseView)
