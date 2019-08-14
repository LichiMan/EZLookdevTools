import logging
from yapsy.IPlugin import IPlugin
from lookdevtools.ui.libs import *

DCC_CONTEXT = None

try:
    import pymel.core as pm
    from lookdevtools.maya import maya
    from lookdevtools.maya import surfacing_projects
    from lookdevtools.maya.surfacing_projects import viewport
    DCC_CONTEXT = True
except:
    logging.warning('PLUGIN: Maya packages not loaded, not this dcc')

class MayaSurfacingViewport(IPlugin):
    name = "MayaSurfacingViewport Plugin"

    plugin_layout = None

    def __init__ (self):
        logging.info('PLUGIN: MayaSurfacingViewport loaded')
        # Load dcc python packages inside a try, to catch the application
        # environment, this will be replaced by IPlugin Categories
        if not DCC_CONTEXT:
            logging.warning('PLUGIN: MayaSurfacingViewport  not loaded, dcc libs not found')
            self.plugin_layout = QtWidgets.QWidget()
            self.label_ui = QtWidgets.QLabel(self.plugin_layout)
            self.label_ui.setText('MayaSurfacingViewport\nPlugin not available in this application')
        else:
            self.build_ui()
    
    def build_ui(self):
        self.plugin_layout = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()
        project_btns_layout = QtWidgets.QHBoxLayout()
        object_btns_layout = QtWidgets.QHBoxLayout()
        selection_layout = QtWidgets.QHBoxLayout()
        wireframe_layout = QtWidgets.QHBoxLayout()
        material_layout = QtWidgets.QHBoxLayout()
        red_text = '#AA0000'

        # Create UI widgets
        # wireframe colors
        self.lbl_wireframe = QtWidgets.QLabel("wireframe colors")
        self.btn_wireframe_color_projects = QtWidgets.QPushButton(
            "per Surfacing Project"
        )
        self.btn_wireframe_color_objects = QtWidgets.QPushButton("per Surfacing Object")
        self.btn_wireframe_color_none = QtWidgets.QPushButton("X")
        self.btn_wireframe_color_none.setMaximumWidth(20)
        self.btn_wireframe_color_none.setStyleSheet('QPushButton {color: %s;}' % red_text)
        # material colors
        self.lbl_materials = QtWidgets.QLabel("material colors")
        self.btn_material_color_projects = QtWidgets.QPushButton("per Surfacing Project")
        self.btn_material_color_objects = QtWidgets.QPushButton("per Surfacing Object")

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