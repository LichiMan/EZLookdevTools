"""
.. module:: maya
   :synopsis: general maya utilities.

.. moduleauthor:: Ezequiel Mastrasso

"""

from lookdevtools.ui.libs import *

def unsaved_scene():
    """Check for unsaved changes."""
    import maya.cmds as cmds

    return cmds.file(q=True, modified=True)

def save_scene_dialog():
    """
    Ask the user to go ahead save or cancel the operation.

    Returns:
        bool. True is Ok clicked, false otherwise.
    
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