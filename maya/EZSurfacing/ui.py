import logging
import pymel.core as pm
from PySide2 import QtCore
from PySide2 import QtGui,QtWidgets, QtWidgets, QtUiTools
from PySide2.QtWidgets import QMessageBox
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import os

import EZSurfacing as EZSurfacing
reload (EZSurfacing)
	
class MainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)

        # Main widget
        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()
        self.setWindowTitle('EZSurfacing')

        main_widget.closeEvent = self.close
        # Create UI widgets
        self.refresh = QtWidgets.QPushButton('refresh')
        self.btn_set_path = QtWidgets.QPushButton('set path')
        self.path = QtWidgets.QLabel('')
        self.sync_selection = QtWidgets.QCheckBox('Sync object set selection')
        self.expand_selection = QtWidgets.QCheckBox('expand selection to members')
        self.project_new_btn = QtWidgets.QPushButton('new texture project')
        self.list_projects = QtWidgets.QListWidget(self)
        self.list_projects.setSortingEnabled(True)
        self.btn_new_texture_object = QtWidgets.QPushButton('new texture object')
        self.btn_add_to_texture_object = QtWidgets.QPushButton('add selected to texture object')
        self.list_texture_objects = QtWidgets.QListWidget(self)
        self.list_texture_objects.setSortingEnabled(True)
        self.btn_validate_scene = QtWidgets.QPushButton('validate scene')
        self.btn_export_project = QtWidgets.QPushButton('export selected project')
        self.btn_export_all = QtWidgets.QPushButton('export all projects')

        EZSurfacing.EZSurfacingInit()
        self.update_ui_projects()

        # TODO
        # To remove the manually refesh button
        # Need to add this to maya as selection changed callback to
        # update the UI avoiding validating the scene
        # import maya.OpenMaya as OpenMaya
        # idx = OpenMaya.MEventMessage.addEventCallback("SelectionChanged", self.update_ui_projects
        # OpenMaya.MMessage.removeCallback(idx)

        # Attach widgets to the main layout
        main_layout.addWidget(self.refresh)
        main_layout.addWidget(self.btn_set_path)
        main_layout.addWidget(self.path)
        main_layout.addWidget(self.sync_selection)
        main_layout.addWidget(self.project_new_btn)
        main_layout.addWidget(self.list_projects)
        main_layout.addWidget(self.btn_new_texture_object)
        main_layout.addWidget(self.expand_selection)
        main_layout.addWidget(self.list_texture_objects)
        main_layout.addWidget(self.btn_add_to_texture_object)
        main_layout.addWidget(self.btn_validate_scene)
        main_layout.addWidget(self.btn_export_project)
        main_layout.addWidget(self.btn_export_all)
        
        # Set main layout
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Connect buttons signals
        self.refresh.clicked.connect(self.update_ui_projects)
        self.btn_set_path.clicked.connect(self.set_path)
        self.project_new_btn.clicked.connect(self.create_project)
        self.list_projects.itemClicked.connect(self.update_ui_texture_objects)
        self.btn_new_texture_object.clicked.connect(self.create_texture_object)
        self.btn_add_to_texture_object.clicked.connect(self.add_to_texture_object)
        self.btn_validate_scene.clicked.connect(self.validate_scene)
        self.list_texture_objects.itemClicked.connect(self.select_texture_object)

        self.btn_export_project.clicked.connect(self.export_project)
        self.btn_export_all.clicked.connect(self.export_all_projects)


    def close(self):
        '''Function to call on panel close'''
        pass

    def select_texture_object(self, item):
        '''selects the texture object on the scene'''
        selected_texture_object = pm.PyNode(str(item.text()))
        if self.sync_selection.isChecked():
            pm.select(selected_texture_object,ne=True)
            if self.expand_selection.isChecked():
                pm.select(selected_texture_object)


    def set_path(self):
        '''sets the EZTool texture root path attribute to where to export'''
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        if file_dialog.exec_():
            root = EZSurfacing.get_project_root()
            path= str(file_dialog.selectedFiles()[0])
            pm.setAttr('%s.EZSurfacing_root' % root, path)
            self.path.setText(os.path.basename(path))

    def create_project(self):
        '''Initializes the scene with the required nodes'''
        root = EZSurfacing.create_project()
        self.update_ui_projects()

    def create_texture_object(self):
        '''Creates a new texture object set'''
        if self.list_projects.currentItem():
            selected_project = pm.PyNode(self.list_projects.currentItem().text())
            pm.select(selected_project)
            EZSurfacing.create_object(selected_project)
            self.update_ui_texture_objects(self.list_projects.currentItem())

    def update_ui_projects(self):
        '''updates the list of texture projects'''
        root = EZSurfacing.get_project_root()
        self.path.setText("Export path: %s" % os.path.basename(pm.getAttr('%s.EZSurfacing_root' % root)))
        #update_lists
        projects = EZSurfacing.get_projects()
        self.list_projects.clear()
        for each in projects:
            self.list_projects.addItem(str(each))
        self.list_texture_objects.clear()


    def update_ui_texture_objects(self, item):
        '''updates the list of texture objects in the selected texture project'''
        selected_project = pm.PyNode(str(item.text()))
        texture_objects = EZSurfacing.get_objects(selected_project)
        self.list_texture_objects.clear()
        for each in texture_objects:
            self.list_texture_objects.addItem(str(each))
        if self.sync_selection.isChecked():
            pm.select(selected_project,ne=True)

    def add_to_texture_object(self):
        '''add maya selection to currently selected texture object'''
        selected_texture_object = pm.PyNode(str(self.list_texture_objects.currentItem().text()))
        if selected_texture_object:
            EZSurfacing.add_mesh_transforms_to_object(pm.PyNode(selected_texture_object),pm.ls(sl=True))

    def validate_scene(self):
        '''scene validation and update'''
        EZSurfacing.validate_scene()

    def export_project(self):
        selected_project = pm.PyNode(str(self.list_projects.currentItem().text()))
        if selected_project:
            EZSurfacing.export_project(selected_project)

    def export_all_projects(self):
        EZSurfacing.export_all_projects()

def show():
    w = MainWindow()
    w.show(dockable=True, floating=False, area='left')