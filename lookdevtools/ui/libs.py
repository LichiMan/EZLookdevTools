import logging

qt_loaded = False
try:
    logging.info('UI Libs: Trying to load PySide2')
    from PySide2.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
    from PySide2 import QtGui, QtWidgets, QtUiTools, QtCore
    qt_loaded = True
except:
    logging.warning('UI Libs: Could not load PySide2')
try:
    logging.info('UI Libs: Loading PyQt5')
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
    from PyQt5 import QtGui, QtWidgets, QtCore
    qt_loaded = True
except:
    logging.warning('UI Libs: Could not load PyQt5')

if not qt_loaded:
    logging.error('UI Libs: Could not load PyQt5 nor PySide2')