from lookdevtools.ui.libs import *

def unsaved_scene():
    """ check for unsaved changes """
    import maya.cmds as cmds

    return cmds.file(q=True, modified=True)

def save_scene_dialog():
    """
    If the scene has unsaved changes, it will ask the user to go ahead save or cancel
    """
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("Your scene has unsaved changes")
    msg.setInformativeText("")
    msg.setWindowTitle("Warning")
    msg.setDetailedText(
        "This tool will do undoable changes. It requires you to save your scene, and reopen it after its finished"
    )
    msg.setStandardButtons(
        QtWidgets.QMessageBox.Ok
        | QtWidgets.QMessageBox.Cancel
    )
    retval = msg.exec_()
    if retval == QtWidgets.QMessageBox.Ok:
        return True
    else:
        return False


def get_folder_path():
    """gets a folder path for export"""
    file_dialog = QtWidgets.QFileDialog()
    file_dialog.setFileMode(QtWidgets.QFileDialog.Directory)
    if file_dialog.exec_():
        path = str(file_dialog.selectedFiles()[0])
        return path
    else:
        return None