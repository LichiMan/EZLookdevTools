import logging
from functools import partial
from yapsy.IPlugin import IPlugin
from lookdevtools.ui.libs import *
from lookdevtools.ui import qtutils
from lookdevtools.common import utils
from lookdevtools.common import templates
from lookdevtools.common.constants import TEXTURESET_ELEMENT_PATTERN
from lookdevtools.maya.surfacing_projects import materials
reload(utils)

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

class MaterialMapping(IPlugin):
    name = "MaterialMapping Plugin"

    plugin_layout = None

    def __init__ (self):
        logger.info('PLUGIN: MaterialMapping loaded')
        # Load dcc python packages inside a try, to catch the application
        # environment, this will be replaced by IPlugin Categories
        if not DCC_CONTEXT:
            logger.warning('PLUGIN: MaterialMapping  not loaded, dcc libs not found')
            self.plugin_layout = QtWidgets.QWidget()
            self.label_ui = QtWidgets.QLabel(self.plugin_layout)
            self.label_ui.setText('MaterialMapping\nPlugin not available in this application')
        else:
            self.build_ui()
    
    def build_ui(self):
        self.plugin_layout = QtWidgets.QWidget()
        self.lbl_custom_template = QtWidgets.QLabel('File load template')
        self.ln_custom_template = QtWidgets.QLineEdit(TEXTURESET_ELEMENT_PATTERN)
        self.btn_search_files = QtWidgets.QPushButton(
            "Search files in folder"
        )
        self.btn_save = QtWidgets.QPushButton(
            "Save json"
        )
        self.btn_load = QtWidgets.QPushButton(
            "Load json"
        )
        self.form_widget = QtWidgets.QTableWidget(0, 7)
        col_headers = ['filepath', 'surfacing_project', 'surfacing_object', 'textureset_element', 'colorspace','udim', 'shader_plug']
        self.form_widget.setHorizontalHeaderLabels(col_headers)
        main_layout = QtWidgets.QVBoxLayout()

        # Attach widgets to the main layout
        main_layout.addWidget(self.lbl_custom_template)
        main_layout.addWidget(self.ln_custom_template)
        main_layout.addWidget(self.btn_search_files)
        main_layout.addWidget(self.form_widget)
        main_layout.addWidget(self.btn_load)
        main_layout.addWidget(self.btn_save)

        # Set main layout
        self.plugin_layout.setLayout(main_layout)

        self.btn_search_files.clicked.connect(
            self.load_textures
        )
        #self.btn_load.clicked.connect(
        #    self.load_json
        #)
        self.btn_save.clicked.connect(
            self.load_json
        )
    
    def load_textures(self):
        config = utils.get_config_materials()
        search_folder = qtutils.get_folder_path()
        if search_folder:
            self.form_widget.setRowCount(0)
            logger.info('Search folder: %s' %search_folder)
            file_list = utils.get_files_in_folder(search_folder, recursive = True, pattern= '.tif')
            custom_template = self.ln_custom_template.text()
            logger.info('Using template: %s' %custom_template)
            file_templates = []
            for file_path in file_list:
                try:
                    file_template_object = templates.custom_texture_file_template(custom_template)
                    file_template = file_template_object.parse(file_path)
                    file_template['file_path'] = file_path
                    try:
                        file_template['shader_plug'] = config['material_mapping']['PxrSurface'][file_template['textureset_element']]
                    except:
                        file_template['shader_plug'] = "None"
                    file_templates.append(file_template)
                except BaseException:
                    logger.warning('File pattern not matched: %s' %file)
            self.form_widget.setRowCount(len(file_templates))
            self.populate_form(file_templates)
            
    def populate_form(self,file_templates):
        for num, file_template in enumerate(file_templates):
            try:
                item = QtWidgets.QTableWidgetItem(file_template['file_path'])
                self.form_widget.setItem(num, 0, item)
            except BaseException:
                logger.error('file_path not in file_template dict.')
            try:
                item = QtWidgets.QTableWidgetItem(file_template['surfacing_project'])
                self.form_widget.setItem(num, 1, item)
            except BaseException:
                logger.error('surfacing_project not in file_template dict.')
            try:
                item = QtWidgets.QTableWidgetItem(file_template['surfacing_object'])
                self.form_widget.setItem(num, 2, item)
            except BaseException:
                logger.error('surfacing_object not in file_template dict.')
            try:
                item = QtWidgets.QTableWidgetItem(file_template['textureset_element'])
                self.form_widget.setItem(num, 3, item)
            except BaseException:
                logger.error('textureset_element not in file_template dict.')
            try:
                item = QtWidgets.QTableWidgetItem(file_template['colorspace'])
                self.form_widget.setItem(num, 4, item)
            except:
                logger.warning('colorspace not in file_template dict.')
            try:
                item = QtWidgets.QTableWidgetItem(file_template['udim'])
                self.form_widget.setItem(num, 5, item)
            except:
                logger.warning('udim not in file_template dict.')
            try:
                search_plug = utils.search_material_mapping(file_template['textureset_element'])
                item = QtWidgets.QTableWidgetItem(search_plug)
                if search_plug == 'None':
                    logger.warning('textureset_element could not be mappend to a shader plug: %s' %file_template['textureset_element'])
                self.form_widget.setItem(num, 6, item)
            except:
                pass
    
    def get_form_data(self):
        file_templates = []
        form_column_count = self.form_widget.columnCount()
        logger.info('Form column count: %s' %form_column_count)
        form_row_count = self.form_widget.rowCount()
        logger.info('Form row count: %s' %form_row_count)
        logger.info('Retrieving form data')
        row = 0
        while row < form_row_count:
            column = 0
            file_templates.append({})
            while column < form_column_count:
                logger.info('Form Coords %s,%s' %(row,column))
                try:
                    item_text = self.form_widget.item(row,column).text()  
                except:
                    item_text = ''     
                column_name = self.form_widget.horizontalHeaderItem(column).text()
                logger.info('Data pair %s,%s' %(column_name,item_text))
                logger.info('Appending to data index %s' %column)
                file_templates[row][column_name] = item_text
                column = column + 1
            row = row + 1
        print file_templates
        return file_templates

    def load_json(self):
        self.get_form_data()
        