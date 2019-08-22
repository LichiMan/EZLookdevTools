import logging
import pymel.core as pm

from lookdevtools.common import utils
from lookdevtools.maya import surfacing_projects
from lookdevtools.common.constants import ATTR_SURFACING_PROJECT
from lookdevtools.common.constants import ATTR_SURFACING_OBJECT

logger = logging.getLogger(__name__)

def create_file_node(name=None):
    file_node = pm.shadingNode('file', name=name, asTexture=True, isColorManaged=True)
    placement_name = '%s_place2dfile_nodeture' % name
    placement_node = pm.shadingNode('place2dTexture', name=placement_name, asUtility=True)
    file_node.filterType.set(0)
    pm.connectAttr(placement_node.outUV, file_node.uvCoord)
    pm.connectAttr(placement_node.outUvFilterSize, file_node.uvFilterSize)
    pm.connectAttr(placement_node.coverage, file_node.coverage)
    pm.connectAttr(placement_node.mirrorU, file_node.mirrorU)
    pm.connectAttr(placement_node.mirrorV, file_node.mirrorV)
    pm.connectAttr(placement_node.noiseUV, file_node.noiseUV)
    pm.connectAttr(placement_node.offset, file_node.offset)
    pm.connectAttr(placement_node.repeatUV, file_node.repeatUV)
    pm.connectAttr(placement_node.rotateFrame, file_node.rotateFrame)
    pm.connectAttr(placement_node.rotateUV, file_node.rotateUV)
    pm.connectAttr(placement_node.stagger, file_node.stagger)
    pm.connectAttr(placement_node.translateFrame, file_node.translateFrame)
    pm.connectAttr(placement_node.wrapU, file_node.wrapU)
    pm.connectAttr(placement_node.wrapV, file_node.wrapV)
    return file_node
    
def get_surfacing_projects_matching_parsed(parsed_files):
    """ Gets a parsed files template dict, and finds matching surfacing projects
    in the maya file"""
    local_surfacing_projects = surfacing_projects.get_projects()
    parsed_surfacing_projects = utils.get_unique_key_values(parsed_files, ATTR_SURFACING_PROJECT)

    surfacing_projects_found = []

    for project in local_surfacing_projects:
        project_name = project.getAttr(ATTR_SURFACING_PROJECT)
        if project_name in parsed_surfacing_projects:
            surfacing_projects_found.append(project)
    return surfacing_projects_found

def def_surfacing_objects_matching_parsed(parsed_files):
    """ Gets a parsed files template dict, and finds matching surfacing objects
    in the maya file"""
    local_surfacing_projects = surfacing_projects.get_projects()
    parsed_surfacing_objects = utils.get_unique_key_values(parsed_files, ATTR_SURFACING_PROJECT)
    surfacing_objects_found = []

    for project in local_surfacing_projects:
        project_name = project.getAttr(ATTR_SURFACING_PROJECT)
        local_surfacing_objects = surfacing_projects.get_objects(project)
        for local_surfacing_object in local_surfacing_objects:
            object_name = local_surfacing_object.getAttr(ATTR_SURFACING_OBJECT)
            if object_name in parsed_surfacing_objects:
                surfacing_objects_found.append(local_surfacing_object)
    return surfacing_objects_found