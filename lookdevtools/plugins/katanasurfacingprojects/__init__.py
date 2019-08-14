import logging
from yapsy.IPlugin import IPlugin
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PySide2 import QtGui, QtWidgets, QtWidgets, QtUiTools, QtCore


class KatanaSurfacingProjects(IPlugin):
    '''Build katana collections and materials for surfacing projects'''
    name = "Katana Surfacing Projects"

    plugin_layout = None

    def __init__ (self):
        logging.info('PLUGIN: KatanaSurfacingProjects loaded')
        # cheap way to know if we are in katana or not
        # replace with IPlugin Categories
        try:
            from Katana import NodegraphAPI
        except:
            logging.warning('PLUGIN: KatanaSurfacingProjects ui not loaded, katana libs not found')
            self.plugin_layout = QtWidgets.QWidget()
            self.label_ui = QtWidgets.QLabel(self.plugin_layout)
            self.label_ui.setText('Plugin not available in this application')
            return False
        