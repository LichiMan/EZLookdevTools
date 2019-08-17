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

class MayaMaterials(IPlugin):
    name = "MayaMaterials Plugin"

    plugin_layout = None

    def __init__ (self):
        logging.info('PLUGIN: MayaMaterials loaded')
        # Load dcc python packages inside a try, to catch the application
        # environment, this will be replaced by IPlugin Categories
        if not DCC_CONTEXT:
            logging.warning('PLUGIN: MayaMaterials  not loaded, dcc libs not found')
            self.plugin_layout = QtWidgets.QWidget()
            self.label_ui = QtWidgets.QLabel(self.plugin_layout)
            self.label_ui.setText('MayaMaterials\nPlugin not available in this application')
        else:
            self.build_ui()
    
    def build_ui(self):
        self.plugin_layout = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()
        wireframe_layout = QtWidgets.QHBoxLayout()
        red_text = '#AA0000'

        # Create UI widgets
        # wireframe colors
        self.lbl_materials = QtWidgets.QLabel("search textures and create materials")
        self.lbl_materials_per_project = QtWidgets.QPushButton(
            "per Surfacing Project"
        )
        self.lbl_materials_per_object = QtWidgets.QPushButton(
            "per Surfacing Object"
        )
        self.btn_wireframe_color_objects = QtWidgets.QPushButton("search textures in folder")

        # Attach widgets to the main layout
        main_layout.addWidget(self.lbl_materials)
        main_layout.addLayout(wireframe_layout)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        wireframe_layout.addWidget(self.lbl_materials_per_project)
        wireframe_layout.addWidget(self.btn_wireframe_color_objects)

        # Set main layout
        self.plugin_layout.setLayout(main_layout)

        # Connect buttons signals