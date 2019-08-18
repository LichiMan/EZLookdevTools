from lookdevtools.ui.libs import *

def get_folder_path():
    """Gets a folder path from the user"""
    file_dialog = QtWidgets.QFileDialog()
    file_dialog.setFileMode(QtWidgets.QFileDialog.Directory)
    if file_dialog.exec_():
        path = str(file_dialog.selectedFiles()[0])
        return path
    else:
        return None