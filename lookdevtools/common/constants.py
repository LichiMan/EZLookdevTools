# Subdivision level to apply to geometry for Surfacing alembics
SURFACING_SUBDIV_ITERATIONS = 2

# Attributes names used for taggin meshes for surfacing
# and later texture to mesh matching
ATTR_SURFACING_PROJECT = "surfacing_project"
ATTR_SURFACING_OBJECT = "surfacing_object"

# Attributes names used for taggin material nodes
ATTR_MATERIAL = "surfacing_material"
ATTR_MATERIAL_VP = "surfacing_material_vp"

# String matching ratios to compare strings against lucidity
# patterns elements.
# Notice that the ratio constant should be high enough,
# to avoid matching for ie: specular to specularIor!
# See utils.string_matching_ratio() string docs for more info
TEXTURESET_MATCHING_RATIO = 90
TEXTURESET_ELEMENT_MATCHING_RATIO = 90

# Example texture template
# folderPathsToProject/textures/
# {textureset}_{textureset_element}_{colorspace}.{UDim}.{extension}
# For ie:
# kettle_baseColor_ACEScg.1001.exr
TEXTURESET_ELEMENT_PATTERN = '{surfacing_project}_{surfacing_object}_{textureset_element}_{colorspace}.{udim}.{extension}'

# Config json file path
# TODO: get sys.environ['LOOKDEVTOOLS'] to fetch the json
CONFIG_MATERIALS_JSON = '/run/media/ezequielm/misc/wrk/dev/EZLookdevTools/lookdevtools/config/materials.json'