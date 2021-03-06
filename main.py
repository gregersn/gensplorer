#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the app."""

import sys
from PyQt5.QtWidgets import QApplication

from views.mainwindow import MainWindow

from services.settings import SETTINGS


def main():
    """Start the app."""
    app = QApplication(sys.argv)
    app.mainwindow = MainWindow(SETTINGS)
    app.mainwindow.show()
    app.exit(app.exec_())

if __name__ == "__main__":
    main()
