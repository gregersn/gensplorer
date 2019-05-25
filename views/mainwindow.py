#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow,
                             QAction,
                             QMessageBox,
                             qApp)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from .tabwidget import TabWidget
from .census2markdown import View as CensusView
from .gedcomsnip import View as GedcomSnip

ICONS = {
    'exit': './assets/icons/icons8-exit-96.png'
}


class MainWindow(QMainWindow):
    def __init__(self, settings=None):
        super().__init__()
        self.settings = settings
        self.actions = {}
        self.init_actions()

        self.toolbar = None
        self.init_ui()

    def init_ui(self):
        """Initialize UI."""
        self.resize(640, 480)
        self.central_widget = TabWidget()

        self.init_menu()
        self.init_toolbar()

        self.central_widget.add_tab(CensusView(), "Census")
        self.central_widget.add_tab(GedcomSnip(), "Snip gedcom")
        self.setCentralWidget(self.central_widget)

    def init_menu(self):
        """Initialize the main menu."""
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(self.actions['exit'])

        helpmenu = menubar.addMenu("&Help")
        helpmenu.addAction(self.actions['about'])

    def init_toolbar(self):
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.actions['exit'])

    def init_actions(self):
        self.actions['exit'] = QAction(QIcon(ICONS['exit']), '&Exit', self)
        self.actions['exit'].setShortcut('Ctrl+Q')
        self.actions['exit'].triggered.connect(qApp.quit)

        self.actions['about'] = QAction("&About", self)
        self.actions['about'].triggered.connect(self.about)

    def about(self):
        about = QMessageBox()
        about.setTextFormat(Qt.RichText)
        about.setText("Created by Greger Stolt Nilsen")
        about.setInformativeText("<br />".join(["Icons from <a href='https://icons8.com/'>Icons8</a>",
                                                "Source at <a href='https://github.com/gregersn/gensplorer'>GitHub</a>"]))
        about.exec_()


if __name__ == "__main__":
    APP = QApplication([])
    WINDOW = MainWindow()
    WINDOW.show()
    APP.exit(APP.exec_())
