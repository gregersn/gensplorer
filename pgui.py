# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/painter.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 791, 551))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.inputGedcom = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.inputGedcom.setObjectName("inputGedcom")
        self.horizontalLayout_2.addWidget(self.inputGedcom)
        self.btnOpenGedcom = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnOpenGedcom.setObjectName("btnOpenGedcom")
        self.horizontalLayout_2.addWidget(self.btnOpenGedcom)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.listTesters = QtWidgets.QListView(self.verticalLayoutWidget)
        self.listTesters.setObjectName("listTesters")
        self.verticalLayout_4.addWidget(self.listTesters)
        self.btnAddTester = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnAddTester.setObjectName("btnAddTester")
        self.verticalLayout_4.addWidget(self.btnAddTester)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.listMatches = QtWidgets.QListView(self.verticalLayoutWidget)
        self.listMatches.setObjectName("listMatches")
        self.verticalLayout_3.addWidget(self.listMatches)
        self.btnAddMatch = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnAddMatch.setObjectName("btnAddMatch")
        self.verticalLayout_3.addWidget(self.btnAddMatch)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Open = QtWidgets.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.action_Save = QtWidgets.QAction(MainWindow)
        self.action_Save.setObjectName("action_Save")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        self.actionE_xit.setObjectName("actionE_xit")
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addAction(self.actionSave_as)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionE_xit)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnOpenGedcom.setText(_translate("MainWindow", "Choose gedcom"))
        self.btnAddTester.setText(_translate("MainWindow", "Add tester"))
        self.btnAddMatch.setText(_translate("MainWindow", "Add match"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.action_Open.setText(_translate("MainWindow", "&Open"))
        self.action_Save.setText(_translate("MainWindow", "&Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save &as..."))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
