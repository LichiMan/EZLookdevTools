"""
NAME: EZCollectionsCreate_surfacing_object
ICON: icon.png
KEYBOARD_SHORTCUT: 
SCOPE:
creates collections for EZSurfacing object

"""

# The following symbols are added when run as a shelf item script:
# exit():      Allows 'error-free' early exit from the script.
# console_print(message, raiseTab=False):
#              Prints the given message to the result area of the largest
#              available Python tab.
#              If raiseTab is passed as True, the tab will be raised to the
#              front in its pane.
#              If no Python tab exists, prints the message to the shell.
# console_clear(raiseTab=False):
#              Clears the result area of the largest available Python tab.
#              If raiseTab is passed as True, the tab will be raised to the
#              front in its pane.

from lookdevtools.katana import surfacing

attribute_name = "geometry.arbitrary.EZSurfacing_object"
surfacing.create_collections(attribute_name)
