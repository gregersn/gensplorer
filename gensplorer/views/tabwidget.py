from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget


class TabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.tabs = QTabWidget()
    
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def add_tab(self, w, n):
        self.tabs.addTab(w, n)
