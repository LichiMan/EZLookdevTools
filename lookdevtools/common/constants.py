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
# patterns elements
TEXTURESET_MATCHING_RATIO = 90
TEXTURESET_ELEMENT_MATCHING_RATIO = 90

# Example texture template
# folderPathsToProject/textures/
# {textureset}_{textureset_element}_{colorspace}.{UDim}.{extension}
# For ie:
# kettle_baseColor_ACEScg.1001.exr
TEXTURESET_ELEMENT_PATTERN = '{surfacing_project}_{surfacing_object}_{textureset_element}_{colorspace}.{UDim}.{extension}'