#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from views.mainwindow import MainWindow
from services import settings


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exit(app.exec_())

if __name__ == "__main__":
    main()
