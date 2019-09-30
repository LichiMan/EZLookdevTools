"""
.. module:: constants
   :synopsis: Constants used through out packages.

.. moduleauthor:: Ezequiel Mastrasso

"""

#: Subdivision level to apply on Surfacing object at alembic export
SURFACING_SUBDIV_ITERATIONS = 2

#: Attributes for tagging meshes for surfacing and texture-to-mesh matching
ATTR_SURFACING_PROJECT = "surfacing_project"
ATTR_SURFACING_OBJECT = "surfacing_object"

#: Attribute for tagging Materials. Values: name of assigned project or object
ATTR_MATERIAL = "surfacing_material"
#: Attribute for tagging material assignmnents. Values: 'project' or 'object']
ATTR_MATERIAL_ASSIGN = "surfacing_assign"
#: Attribute for tagging viewport material. Values: 'color' or 'pattern']
ATTR_MATERIAL_VP = "surfacing_vp"

#: Global string matching ratios to compare strings against lucidity parsed files.
#: Notice that the ratio constant should be high enough,
TEXTURESET_MATCHING_RATIO = 90
TEXTURESET_ELEMENT_MATCHING_RATIO = 90

#: Texture file template, ANCHOR RIGHT
TEXTURESET_ELEMENT_PATTERN = '{surfacing_project}_{surfacing_object}_{textureset_element}_{colorspace}.{udim}.{extension}'

# utils constants
PROCESSES=4

#: Materials json Config, contains texture name mappings to shader plugs
CONFIG_MATERIALS_JSON = '/run/media/ezequielm/misc/wrk/dev/EZLookdevTools/lookdevtools/config/materials.json'
# TODO: get sys.environ['LOOKDEVTOOLS'] to fetch the json
