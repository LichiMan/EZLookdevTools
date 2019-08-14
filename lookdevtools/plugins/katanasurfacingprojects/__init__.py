import logging
from yapsy.IPlugin import IPlugin

from lookdevtools.ui.libs import *


class KatanaSurfacingProjects(IPlugin):
    '''Build katana collections and materials for surfacing projects'''
    name = "Katana Surfacing Projects"

    plugin_layout = None

    def __init__ (self):
        logging.info('PLUGIN: KatanaSurfacingProjects loaded')
        try:
            from Katana import NodegraphAPI
        except:
            logging.warning('PLUGIN: KatanaSurfacingProjects ui not loaded, katana libs not found')
            self.plugin_layout = QtWidgets.QWidget()
            self.label_ui = QtWidgets.QLabel(self.plugin_layout)
            self.label_ui.setText('Plug in no available in this Application')
        else:
            self.plugin_layout = QtWidgets.QWidget()
            self.label_ui = QtWidgets.QLabel(self.plugin_layout)
            self.label_ui.setText('Plug in AVAILABLE')