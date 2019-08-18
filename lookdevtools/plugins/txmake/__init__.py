import os
import logging

from yapsy.IPlugin import IPlugin

from lookdevtools.ui.libs import *
from lookdevtools.ui import qtutils
from lookdevtools.common import utils
from lookdevtools.renderman import txmake
reload(txmake)

# Non DCC specific
DCC_CONTEXT = True

class TxMake(IPlugin):
    name = "TxMake Plugin"

    plugin_layout = None

    def __init__ (self):
        logging.info('PLUGIN: TxMake loaded')
        # Load dcc python packages inside a try, to catch the application
        # environment, this will be replaced by IPlugin Categories
        if not DCC_CONTEXT:
            logging.warning('PLUGIN: TxMake  not loaded, dcc libs not found')
            self.plugin_layout = QtWidgets.QWidget()
            self.label_ui = QtWidgets.QLabel(self.plugin_layout)
            self.label_ui.setText('TxMake\nPlugin not available in this application')
        else:
            self.build_ui()
    
    def build_ui(self):
        self.plugin_layout = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()
        txmake_layout = QtWidgets.QVBoxLayout()

        # Create UI widgets
        # txmake colors
        self.lbl_txmake = QtWidgets.QLabel("Convert Textures to .tex renderman format")
        self.lbl_extension = QtWidgets.QLabel("file extension search")
        self.line_extension = QtWidgets.QLineEdit(".exr")
        self.cbox_recursive = QtWidgets.QCheckBox("search subdirectories")
        self.btn_txmake = QtWidgets.QPushButton(
            "Select a folder"
        )

        # Attach widgets to the main layout
        main_layout.addWidget(self.lbl_txmake)
        main_layout.addLayout(txmake_layout)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        txmake_layout.addWidget(self.lbl_extension)
        txmake_layout.addWidget(self.line_extension)
        txmake_layout.addWidget(self.cbox_recursive)
        txmake_layout.addWidget(self.btn_txmake)

        # Set main layout
        self.plugin_layout.setLayout(main_layout)

        # Connect buttons signals
        self.btn_txmake.clicked.connect(
            self.run
        )

    def run(self):
        folder_path = qtutils.get_folder_path()
        file_list = utils.get_files_in_folder(folder_path,
                                            recursive= self.cbox_recursive.checkState(),
                                            pattern= self.line_extension.text()
                                            )
        txmake.convert_to_tx(file_list)