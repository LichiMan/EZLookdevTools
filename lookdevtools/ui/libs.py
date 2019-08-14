import logging

try:
    logging.info('UI Libs: Loading PySide2')
    from PySide2.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
    from PySide2 import QtGui, QtWidgets, QtWidgets, QtUiTools, QtCore
except:
    logging.error('UI Libs: Could not load PySide2')

try:
    logging.info('UI Libs: Loading PyQt5')
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
    from PyQt5 import QtGui, QtWidgets, QtWidgets, QtCore
except:
    logging.error('UI Libs: Could not load PyQt5')


