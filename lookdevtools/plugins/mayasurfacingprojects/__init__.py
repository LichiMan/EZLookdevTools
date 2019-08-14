import logging
from yapsy.IPlugin import IPlugin
from lookdevtools.ui.libs import *


import pymel.core as pm 

from lookdevtools.maya import maya
from lookdevtools.maya import surfacing_projects
from lookdevtools.maya.surfacing_projects import viewport

class MayaSurfacingProjects(IPlugin):
    name = "mayaSurfacingProjects Plugin"

    plugin_layout = None

    def __init__ (self):
        logging.info('PLUGIN: MayaSurfacingProjects loaded')
        # Load dcc python packages inside a try, to catch the application
        # environment, this will be replaced by IPlugin Categories
        try:
            import pymel.core as pm 
        except:
            logging.warning('PLUGIN: KatanaSurfacingProjects ui not loaded, katana libs not found')
            self.plugin_layout = QtWidgets.QWidget()
            self.label_ui = QtWidgets.QLabel(self.plugin_layout)
            self.label_ui.setText('Plugin not available in this application')
            return False
        self.plugin_layout = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()
        project_btns_layout = QtWidgets.QHBoxLayout()
        object_btns_layout = QtWidgets.QHBoxLayout()
        selection_layout = QtWidgets.QHBoxLayout()
        red_text = '#AA0000'

        # Create UI widgets
        self.refresh = QtWidgets.QPushButton("refresh")
        self.sync_selection = QtWidgets.QCheckBox("Sync object set selection")
        self.expand_selection = QtWidgets.QCheckBox("expand selection to members")
        self.project_new_btn = QtWidgets.QPushButton("new texture project")
        self.project_delete_btn = QtWidgets.QPushButton("X")
        self.project_delete_btn.setMaximumWidth(20)
        self.project_delete_btn.setStyleSheet('QPushButton {color: %s;}' % red_text)
        self.list_projects = QtWidgets.QListWidget()
        self.list_projects.setSortingEnabled(True)
        self.btn_new_texture_object = QtWidgets.QPushButton("new texture object")
        self.btn_delete_texture_object = QtWidgets.QPushButton("X")
        self.btn_delete_texture_object.setMaximumWidth(20)
        self.btn_delete_texture_object.setStyleSheet('QPushButton {color: %s;}' % red_text)
        self.btn_add_to_texture_object = QtWidgets.QPushButton(
            "add selected to texture object"
        )
        self.list_texture_objects = QtWidgets.QListWidget()
        self.list_texture_objects.setSortingEnabled(True)
        self.lbl_validate_scene = QtWidgets.QLabel("validation")
        self.btn_validate_scene = QtWidgets.QPushButton("validate scene")
        self.lbl_export = QtWidgets.QLabel("Export")
        self.btn_export_project = QtWidgets.QPushButton("Selected Project")
        self.btn_export_all = QtWidgets.QPushButton("All Projects")

        # TODO
        # To remove the manually refesh button
        # Need to add this to maya as selection changed callback to
        # update the UI avoiding validating the scene
        # import maya.OpenMaya as OpenMaya
        # idx = OpenMaya.MEventMessage.addEventCallback("SelectionChanged", self.update_ui_projects
        # OpenMaya.MMessage.removeCallback(idx)

        # Attach widgets to the main layout
        main_layout.addWidget(self.refresh)
        main_layout.addLayout(selection_layout)
        selection_layout.addWidget(self.sync_selection)
        selection_layout.addWidget(self.expand_selection)
        main_layout.addLayout(project_btns_layout)
        project_btns_layout.addWidget(self.project_new_btn)
        project_btns_layout.addWidget(self.project_delete_btn)
        main_layout.addWidget(self.list_projects)
        main_layout.addLayout(object_btns_layout)
        object_btns_layout.addWidget(self.btn_new_texture_object)
        object_btns_layout.addWidget(self.btn_delete_texture_object)
        main_layout.addWidget(self.btn_add_to_texture_object)
        main_layout.addWidget(self.list_texture_objects)
        main_layout.addWidget(self.lbl_validate_scene)
        main_layout.addWidget(self.btn_validate_scene)
        main_layout.addWidget(self.lbl_export)
        main_layout.addWidget(self.btn_export_project)
        main_layout.addWidget(self.btn_export_all)

        # Set main layout
        self.plugin_layout.setLayout(main_layout)

        # Connect buttons signals
        self.refresh.clicked.connect(self.update_ui_projects)
        self.project_new_btn.clicked.connect(self.create_project)
        self.project_delete_btn.clicked.connect(self.delete_project)
        self.list_projects.itemClicked.connect(self.update_ui_texture_objects)
        self.list_projects.itemDoubleClicked.connect(self.editItem)
        self.btn_new_texture_object.clicked.connect(self.create_texture_object)
        self.btn_delete_texture_object.clicked.connect(self.delete_texture_object)
        self.btn_add_to_texture_object.clicked.connect(self.add_to_texture_object)
        self.btn_validate_scene.clicked.connect(self.validate_scene)
        self.list_texture_objects.itemClicked.connect(self.select_texture_object)
        self.list_texture_objects.itemDoubleClicked.connect(self.editItem)

        self.btn_export_project.clicked.connect(self.export_project)
        self.btn_export_all.clicked.connect(self.export_all_projects)


        self.update_ui_projects()

    def editItem(self, item):
        item_object_set = pm.PyNode(str(item.text()))
        text, okPressed = QtWidgets.QInputDialog.getText(
            self, "", "rename to:", QtWidgets.QLineEdit.Normal, str(item.text())
        )
        if okPressed and text != "":
            logging.info("renaming objsetSet %s to %s" % (item.text(), text))
            try:
                pm.rename(item_object_set, text)
            except:
                pass
            finally:
                self.update_ui_projects()

    def delete_project(self):
        selected_project = pm.PyNode(self.list_projects.currentItem().text())
        surfacing_projects.delete_project(selected_project)
        self.update_ui_projects()

    def select_texture_object(self, item):
        """selects the texture object on the scene"""
        selected_texture_object = pm.PyNode(str(item.text()))
        if self.sync_selection.isChecked():
            pm.select(selected_texture_object, ne=True)
            if self.expand_selection.isChecked():
                pm.select(selected_texture_object)

    def create_project(self):
        """Initializes the scene with the required nodes"""
        root = surfacing_projects.create_project()
        self.update_ui_projects()

    def create_texture_object(self):
        """Creates a new texture object set"""
        if self.list_projects.currentItem():
            selected_project = pm.PyNode(self.list_projects.currentItem().text())
            pm.select(selected_project)
            surfacing_projects.create_object(selected_project)
            self.update_ui_texture_objects(self.list_projects.currentItem())

    def delete_texture_object(self):
        if self.list_texture_objects.currentItem():
            selected_object = pm.PyNode(self.list_texture_objects.currentItem().text())
            if selected_object and surfacing_projects.is_texture_object(selected_object):
                pm.delete(selected_object)
                self.update_ui_projects()

    def update_ui_projects(self):
        """updates the list of texture projects"""
        root = surfacing_projects.get_project_root()
        # update_lists
        projects = surfacing_projects.get_projects()
        self.list_projects.clear()
        for each in projects:
            self.list_projects.addItem(str(each))
        self.list_texture_objects.clear()

    def update_ui_texture_objects(self, item):
        """updates the list of texture objects in the selected texture project"""
        selected_project = pm.PyNode(str(item.text()))
        texture_objects = surfacing_projects.get_objects(selected_project)
        self.list_texture_objects.clear()
        for each in texture_objects:
            self.list_texture_objects.addItem(str(each))
        if self.sync_selection.isChecked():
            pm.select(selected_project, ne=True)

    def add_to_texture_object(self):
        """add maya selection to currently selected texture object"""
        selected_texture_object = pm.PyNode(
            str(self.list_texture_objects.currentItem().text())
        )
        if selected_texture_object:
            surfacing_projects.add_mesh_transforms_to_object(
                pm.PyNode(selected_texture_object), pm.ls(sl=True)
            )

    def validate_scene(self):
        """scene validation and update"""
        surfacing_projects.validate_scene()

    def export_project(self):
        selected_project = pm.PyNode(str(self.list_projects.currentItem().text()))
        if selected_project:
            surfacing_projects.export_project(selected_project)

    def export_all_projects(self):
        surfacing_projects.export_all_projects()
