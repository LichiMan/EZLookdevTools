import sys
import imp
import os
import logging
from functools import partial

from lookdevtools.ui.libs import *

import lookdevtools
reload(lookdevtools)

plugins = lookdevtools.load_plugins()

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
    '''Main Tools UI Window. Loads the plugInfo.plugin_object.plugin_layout
    QWidget from all loaded plugins as tabs'''
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setWindowTitle("Look Dev Tool Set")
        self.setGeometry(0, 0, 450, 600)
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        tabwidget = QtWidgets.QTabWidget()
        tabwidget.setTabBar(HTabWidget(width=150,height=50))
        tabwidget.setTabPosition(QtWidgets.QTabWidget.West)

        # Stylesheet fix for Katana
        # With default colors, the tab text is almost the
        # same as the tab background
        stylesheet = """
        QTabBar::tab:unselected {background: #222222;}
        QTabWidget>QWidget>QWidget{background: #222222;}
        QTabBar::tab:selected {background: #303030;}
        QTabWidget>QWidget>QWidget{background: #303030;}
        """
        tabwidget.setStyleSheet(stylesheet)
        
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
