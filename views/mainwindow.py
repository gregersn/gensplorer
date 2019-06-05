#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import (QMainWindow,
                             QAction,
                             QActionGroup,
                             QMessageBox,
                             qApp)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMdiArea, QMdiSubWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from .stackwidget import StackWidget
from .census2markdown import View as CensusView
from .gedcom import View as GedcomView
from .dna import View as DNAView

from services import settings

ICONS = {
    'exit': './assets/icons/icons8-exit-96.png'
}


class MainWindow(QMainWindow):
    """Handle all subwindows."""
    def __init__(self, s=None, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.settings = s
        self.actions = {}
        self.views = {}

        self.toolbar = None
        self.init_ui()
        self.init_actions()
        self.init_menu()

        self.add_view(CensusView(), 'census')
        self.add_view(GedcomView(), 'gedcom')
        self.add_view(DNAView(), 'dna')

        open_windows = self.settings.get('window')
        for window, state in open_windows.items():
            if state:
                self.actions[window].trigger()

    def init_ui(self):
        """Initialize UI."""
        self.resize(640, 480)

        self.central_widget = QMdiArea()

        self.setCentralWidget(self.central_widget)

    def init_menu(self):
        """Initialize the main menu."""
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(self.actions['preferences'])
        filemenu.addAction(self.actions['exit'])

        self.viewmenu = menubar.addMenu('&View')
        windowmenu = menubar.addMenu("&Window")
        windowmenu.addAction(self.actions['cascade'])
        windowmenu.addAction(self.actions['tile'])

        helpmenu = menubar.addMenu("&Help")
        helpmenu.addAction(self.actions['about'])
    
    def view_chosen(self, t):
        data = t.data()
        self.central_widget.set_current(data)
        self.settings.set('current_view', data)

    def init_toolbar(self):
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.actions['exit'])

    def init_actions(self):
        self.actions['exit'] = QAction(QIcon(ICONS['exit']), '&Exit', self)
        self.actions['exit'].setShortcut('Ctrl+Q')
        self.actions['exit'].menuRole = QAction.QuitRole
        self.actions['exit'].triggered.connect(self.close)

        self.actions['preferences'] = QAction("Preferences", self)
        self.actions['preferences'].menuRole = QAction.PreferencesRole

        self.actions['about'] = QAction("&About", self)
        self.actions['about'].menuRole = QAction.AboutRole
        self.actions['about'].triggered.connect(self.about)

        self.actions['tile'] = QAction("Tile", self)
        self.actions['tile'].triggered.connect(self.central_widget.tileSubWindows)

        self.actions['cascade'] = QAction("Cascade", self)
        self.actions['cascade'].triggered.connect(self.central_widget.cascadeSubWindows)
    
    def toggle_view(self, actionname):
        action = self.actions[actionname]
        if action.isChecked():
            self.open_window(self.views[actionname])
            self.settings.set("window.{}".format(actionname), True)
        else:
            self.close_window(self.views[actionname])
            self.settings.set("window.{}".format(actionname), False)

    def about(self):
        about = QMessageBox()
        about.setTextFormat(Qt.RichText)
        about.setText("Created by Greger Stolt Nilsen")
        about.setInformativeText("<br />".join(["Icons from <a href='https://icons8.com/'>Icons8</a>",
                                                "Source at <a href='https://github.com/gregersn/gensplorer'>GitHub</a>"]))
        about.exec_()

    def add_view(self, w, name):
        sub = QMdiSubWindow()
        sub.setWidget(w)
        self.views[name] = sub
        
        self.actions[name] = QAction(w.display_name if hasattr(w, 'display_name') else name, self, checkable=True)
        self.actions[name].setData(name)
        self.actions[name].triggered.connect(lambda: self.toggle_view(name))

        self.viewmenu.addAction(self.actions[name])

    def open_window(self, w):
        print("Opening window", w)
        self.central_widget.addSubWindow(w)
        w.show()
    
    def close_window(self, w):
        print("Closing window", w)
        self.central_widget.removeSubWindow(w)
    
    def closeEvent(self, event):
        print("Close event")
        self.settings.save()

