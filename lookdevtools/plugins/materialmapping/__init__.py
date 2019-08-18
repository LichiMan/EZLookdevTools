import logging
from functools import partial
from yapsy.IPlugin import IPlugin
from lookdevtools.ui.libs import *
from lookdevtools.ui import qtutils
from lookdevtools.common import utils
from lookdevtools.common import templates
from lookdevtools.maya.surfacing_projects import materials
reload(utils)
DCC_CONTEXT = None

try:
    import pymel.core as pm
    from lookdevtools.maya import maya
    from lookdevtools.maya import surfacing_projects
    from lookdevtools.maya.surfacing_projects import viewport
    DCC_CONTEXT = True
except:
    logging.warning('PLUGIN: Maya packages not loaded, not this dcc')

class MaterialMapping(IPlugin):
    name = "MaterialMapping Plugin"

    plugin_layout = None

    def __init__ (self):
        logging.info('PLUGIN: MaterialMapping loaded')
        # Load dcc python packages inside a try, to catch the application
        # environment, this will be replaced by IPlugin Categories
        if not DCC_CONTEXT:
            logging.warning('PLUGIN: MaterialMapping  not loaded, dcc libs not found')
            self.plugin_layout = QtWidgets.QWidget()
            self.label_ui = QtWidgets.QLabel(self.plugin_layout)
            self.label_ui.setText('MaterialMapping\nPlugin not available in this application')
        else:
            self.build_ui()
    
    def build_ui(self):
        self.plugin_layout = QtWidgets.QWidget()
        self.btn_search_files = QtWidgets.QPushButton(
            "Search files in folder"
        )
        self.btn_save = QtWidgets.QPushButton(
            "Save json"
        )
        self.btn_load = QtWidgets.QPushButton(
            "Load json"
        )
        self.form_widget = QtWidgets.QTableWidget(0, 6)
        col_headers = ['filepath', 'surfacing_project', 'surfacing_object', 'textureset_element', 'colorspace', 'shader_plug']
        self.form_widget.setHorizontalHeaderLabels(col_headers)
        main_layout = QtWidgets.QVBoxLayout()

        # Attach widgets to the main layout
        main_layout.addWidget(self.btn_search_files)
        main_layout.addWidget(self.form_widget)
        main_layout.addWidget(self.btn_load)
        main_layout.addWidget(self.btn_save)

        # Set main layout
        self.plugin_layout.setLayout(main_layout)

        self.btn_search_files.clicked.connect(
            self.load_textures
        )
        self.btn_load.clicked.connect(
            self.load_json
        )
    
    def load_textures(self):
        config = utils.get_config()
        search_folder = qtutils.get_folder_path()
        logging.info('Search folder: %s' %search_folder)
        file_list = utils.get_files_in_folder(search_folder, recursive = True, pattern= '.tif')
        print file_list
        file_templates = []
        for file_path in file_list:
            try:
                file_template = templates.textureset_element_template.parse(file_path)
                file_template['file_path'] = file_path
                try:
                    file_template['shader_plug'] = config['material_mapping']['PxrSurface'][file_template['textureset_element']]
                except:
                    file_template['shader_plug'] = "None"
                file_templates.append(file_template)
            except BaseException:
                logging.warning('File pattern not matched: %s' %file)
        self.form_widget.setRowCount(len(file_templates))

        for num, file_template in enumerate(file_templates):
            item = QtWidgets.QTableWidgetItem(file_template['file_path'])
            self.form_widget.setItem(num, 0, item)
            item = QtWidgets.QTableWidgetItem(file_template['surfacing_project'])
            self.form_widget.setItem(num, 1, item)
            item = QtWidgets.QTableWidgetItem(file_template['surfacing_object'])
            self.form_widget.setItem(num, 2, item)
            item = QtWidgets.QTableWidgetItem(file_template['textureset_element'])
            self.form_widget.setItem(num, 3, item)
            item = QtWidgets.QTableWidgetItem(file_template['colorspace'])
            self.form_widget.setItem(num, 4, item)
            try:
                search_plug = utils.search_material_mapping(file_template['textureset_element'])
                item = QtWidgets.QTableWidgetItem(search_plug)
                self.form_widget.setItem(num, 5, item)
            except:
                pass
        print utils.search_material_mapping()
            
    def populate_form(self):
        pass

    def load_json(self):
        print utils.get_config()