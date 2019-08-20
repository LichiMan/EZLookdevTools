import logging
from functools import partial
from yapsy.IPlugin import IPlugin
from lookdevtools.ui.libs import *
from lookdevtools.ui import qtutils
from lookdevtools.maya.surfacing_projects import materials

logger = logging.getLogger(__name__)

DCC_CONTEXT = None

try:
    import pymel.core as pm
    from lookdevtools.maya import maya
    from lookdevtools.maya import surfacing_projects
    from lookdevtools.maya.surfacing_projects import viewport
    DCC_CONTEXT = True
except:
    logger.warning('PLUGIN: Maya packages not loaded, not this dcc')

class MayaMaterials(IPlugin):
    name = "MayaMaterials Plugin"

    plugin_layout = None

    def __init__ (self):
        logger.info('PLUGIN: MayaMaterials loaded')
        # Load dcc python packages inside a try, to catch the application
        # environment, this will be replaced by IPlugin Categories
        if not DCC_CONTEXT:
            logger.warning('PLUGIN: MayaMaterials  not loaded, dcc libs not found')
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
        self.btn_materials_per_project = QtWidgets.QPushButton(
            "per Surfacing Project"
        )
        self.btn_materials_per_object = QtWidgets.QPushButton("per Surfacing Object")

        # Attach widgets to the main layout
        main_layout.addWidget(self.lbl_materials)
        main_layout.addLayout(wireframe_layout)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        wireframe_layout.addWidget(self.btn_materials_per_project)
        wireframe_layout.addWidget(self.btn_materials_per_object)

        # Set main layout
        self.plugin_layout.setLayout(main_layout)

        # Connect buttons signals
        self.btn_materials_per_project.clicked.connect(
            partial (self.create_materials,"geometry.arbitrary.surfacing_project")
        )
        self.btn_materials_per_object.clicked.connect(
            partial (self.create_materials,"geometry.arbitrary.surfacing_object")
        )
    
    def create_materials(self, attribute):
        search_folder = qtutils.get_folder_path()
        logger.info('Search folder: %s' %search_folder)
        logger.info('Search attribute: %s' %attribute)