import logging
from yapsy.IPlugin import IPlugin
from lookdevtools.ui.libs import *

from lookdevtools.maya import maya
from lookdevtools.maya import surfacing_projects
from lookdevtools.maya.surfacing_projects import viewport

class MayaSurfacingViewport(IPlugin):
    name = "MayaSurfacingViewport Plugin"

    plugin_layout = None

    def __init__ (self):
        logging.info('PLUGIN: MayaSurfacingViewport loaded')
        # Load dcc python packages inside a try, to catch the application
        # environment, this will be replaced by IPlugin Categories
        try:
            import pymel.core as pm 
        except:
            logging.warning('PLUGIN: MayaSurfacingViewport ui not loaded, katana libs not found')
            self.plugin_layout = QtWidgets.QWidget()
            self.label_ui = QtWidgets.QLabel(self.plugin_layout)
            self.label_ui.setText('Plugin not available in this application')
        else:
            self.plugin_layout = QtWidgets.QWidget()
            main_layout = QtWidgets.QVBoxLayout()
            project_btns_layout = QtWidgets.QHBoxLayout()
            object_btns_layout = QtWidgets.QHBoxLayout()
            selection_layout = QtWidgets.QHBoxLayout()
            wireframe_layout = QtWidgets.QHBoxLayout()
            material_layout = QtWidgets.QHBoxLayout()
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
            self.lbl_wireframe = QtWidgets.QLabel("wireframe colors")
            self.btn_wireframe_color_projects = QtWidgets.QPushButton(
                "per Surfacing Project"
            )
            self.btn_wireframe_color_objects = QtWidgets.QPushButton("per Surfacing Object")
            self.btn_wireframe_color_none = QtWidgets.QPushButton("X")
            self.btn_wireframe_color_none.setMaximumWidth(20)
            self.btn_wireframe_color_none.setStyleSheet('QPushButton {color: %s;}' % red_text)
            self.lbl_materials = QtWidgets.QLabel("material colors")
            self.btn_material_color_projects = QtWidgets.QPushButton("per Surfacing Project")
            self.btn_material_color_objects = QtWidgets.QPushButton("per Surfacing Object")
            self.lbl_validate_scene = QtWidgets.QLabel("validation")
            self.btn_validate_scene = QtWidgets.QPushButton("validate scene")
            self.lbl_export = QtWidgets.QLabel("Export")
            self.btn_export_project = QtWidgets.QPushButton("Selected Project")
            self.btn_export_all = QtWidgets.QPushButton("All Projects")

            # Attach widgets to the main layout
            main_layout.addWidget(self.lbl_wireframe)
            main_layout.addLayout(wireframe_layout)
            main_layout.setAlignment(QtCore.Qt.AlignTop)
            wireframe_layout.addWidget(self.btn_wireframe_color_projects)
            wireframe_layout.addWidget(self.btn_wireframe_color_objects)
            wireframe_layout.addWidget(self.btn_wireframe_color_none)
            main_layout.addWidget(self.lbl_materials)
            main_layout.addLayout(material_layout)
            material_layout.addWidget(self.btn_material_color_projects)
            material_layout.addWidget(self.btn_material_color_objects)
            main_layout.addWidget(self.lbl_validate_scene)
            main_layout.addWidget(self.btn_validate_scene)

            # Set main layout
            self.plugin_layout.setLayout(main_layout)

            # Connect buttons signals
            self.btn_wireframe_color_projects.clicked.connect(
                viewport.set_wireframe_colors_per_project
            )
            self.btn_wireframe_color_objects.clicked.connect(
                viewport.set_wireframe_colors_per_object
            )
            self.btn_wireframe_color_none.clicked.connect(
                viewport.set_wifreframe_color_none
            )
            self.btn_material_color_projects.clicked.connect(
                viewport.set_materials_per_project
            )
            self.btn_material_color_objects.clicked.connect(
                viewport.set_materials_per_object
            )