from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget


class StackWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.views = {}
        self.layout = QVBoxLayout()

        self.stack = QStackedWidget()
    
        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)

    def add_view(self, w, n):
        index = self.stack.addWidget(w)
        self.views[n] = index
    
    def set_current(self, name):
        if name is None:
            self.stack.setCurrentIndex(0)
            return

        self.stack.setCurrentIndex(self.views[name])
