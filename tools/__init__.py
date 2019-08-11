import sys
import imp
import os
import logging
from functools import partial
try:
    from PySide2.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
    from PySide2 import QtGui, QtWidgets, QtWidgets, QtUiTools, QtCore
except:
    pass

# Load external packages
current_dir = os.path.dirname(__file__)
external_packages_dir = os.path.join(current_dir,'external')
logging.info('EXTERNAL MODULES: Appending external modules dir to sys.path: %s'
             %external_packages_dir)
sys.path.append(external_packages_dir)

import yapsy as yapsy
try:
    from yapsy.PluginManager import PluginManager
    logging.info('EXTERNAL MODULES: yapsy.PluginManager loaded succesfuly')
except:
    raise RuntimeError('EXTERNAL MODULES: failed to load external modules')

# Plugin manager
plugins = PluginManager()
plugins_folder = os.path.join(current_dir,'plugins')
plugins.setPluginPlaces([plugins_folder])
plugins.collectPlugins()
for pluginInfo in plugins.getAllPlugins():
    plugins.activatePluginByName(pluginInfo.name)

class HTabWidget(QtWidgets.QTabBar):
    '''
    QPaint event to draw the QTabWidget titles horizontally
    '''
    def __init__(self, *args, **kwargs):
        self.tabSize = QtCore.QSize(kwargs.pop('width'), kwargs.pop('height'))
        super(HTabWidget, self).__init__(*args, **kwargs)

    def paintEvent(self, event):
        
        painter = QtWidgets.QStylePainter(self)
        option = QtWidgets.QStyleOptionTab()

        for index in range(self.count()):
            self.initStyleOption(option, index)
            tabRect = self.tabRect(index)
            tabRect.moveLeft(10)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, option)
            painter.drawText(tabRect, QtCore.Qt.AlignVCenter |\
                             QtCore.Qt.TextDontClip, \
                             self.tabText(index));

    def tabSizeHint(self,index):
        return self.tabSize

class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setWindowTitle("Look Dev Tool Set")
        self.setGeometry(0, 0, 800, 400)
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        tabwidget = QtWidgets.QTabWidget()
        tabwidget.setTabBar(HTabWidget(width=100,height=25))
        tabwidget.setTabPosition(QtWidgets.QTabWidget.West)    
        layout.addWidget(tabwidget, 0, 0)
        plugins_ui = {}
        plugins_buttons = {}
        for pluginInfo in plugins.getAllPlugins():
            tabwidget.addTab(
                pluginInfo.plugin_object.plugin_layout,
                pluginInfo.name)
        self.setCentralWidget(tabwidget)

main_window = QApplication.instance()
if main_window:
    app = main_window
else:
    app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()
