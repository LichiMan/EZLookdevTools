import logging
from yapsy.IPlugin import IPlugin
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PySide2 import QtGui, QtWidgets, QtWidgets, QtUiTools, QtCore

class ExamplePlugIn(IPlugin):
    name = "Example Plugin"

    plugin_layout = None

    def __init__ (self):
        logging.info('PLUGIN: example_plugin loaded')
        self.plugin_layout = QtWidgets.QWidget()
        #self.plugin_layout.setAlignment(QtCore.Qt.AlignTop)

        self.label_ui = QtWidgets.QLabel(self.plugin_layout)
        self.label_ui.setText('example PlugIn UI')
        #self.plugin_layout.addWidget(self.label_ui)