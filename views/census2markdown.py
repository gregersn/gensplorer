#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QTextEdit, QLineEdit
from PyQt5.QtWidgets import QErrorMessage

from .baseview import BaseView
from services import census


class View(BaseView):
    def __init__(self):
        super().__init__()

    def initUi(self):
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.entry())
        self.layout.addWidget(self.output())
        self.setLayout(self.layout)

    def entry(self):
        layout = QHBoxLayout()
        self.data['url'] = QLineEdit()
        layout.addWidget(self.data['url'])
        btn = QPushButton("Get census")
        btn.clicked.connect(self.get_census)
        layout.addWidget(btn)
        return layout

    def output(self):
        self.data['output'] = QTextEdit()
        self.data['output'].mousePressEvent = self.copy_census
        return self.data['output']

    def get_census(self):
        url = self.data['url'].text()
        try:
            census_data = census.get_census(url)
            markdown = census.census_to_markdown(**census_data)
            self.data['output'].setText(markdown)
        except census.MissingSchema as err:
            self.show_error("ERROR: Is the URL correct?")
        except census.InvalidURL as err:
            self.show_error("ERROR: URL {} is invalid".format(url))
    
    def copy_census(self, event):
        self.data['output'].selectAll()
        self.data['output'].copy()
