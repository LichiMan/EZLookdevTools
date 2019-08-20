import logging
import pymel.core as pm

logger = logging.getLogger(__name__)

def create_shader(node_type=None, name=None):
    shader = pm.shadingNode(node_type, asShader=True)
    return shader

def create_shading_group ():
    shading_group= pm.sets(renderable=True,noSurfaceShader=True,empty=True)
    return shading_group

def connect_shader_to_shading_groups(shader, shading_group):
    pm.connectAttr('%s.outColor' %shader ,'%s.surfaceShader' %shading_group)


def connect_file_node_to_shader(file_node, shader):
    pm.connectAttr('%s.outColor' %file_node, '%s.color' %shader)

def get_shader_shading_group():
    pass

def assign_material(shading_group, object_list=[]):
    pm.sets(shading_group, edit=True, forceElement=object_list)

def create_file_node(name):
    file_node = pm.shadingNode('file', name=name, asTexture=True, isColorManaged=True)
    placement_name = '%s_place2dfile_nodeture' % name
    if not pm.objExists(placement_name):
        placement_node = pm.shadingNode('place2dTexture', name=placement_name, asUtility=True)
    file_node.filterType.set(0)
    pm.connectAttr(placement_node.outUV, file_node.uvCoord)
    pm.connectAttr(placement_node.outUvFilterSize, file_node.uvFilterSize)
    pm.connectAttr(placement_node.verfile_nodeCameraOne, file_node.verfile_nodeCameraOne)
    pm.connectAttr(placement_node.verfile_nodeUvOne, file_node.verfile_nodeUvOne)
    pm.connectAttr(placement_node.verfile_nodeUvThree, file_node.verfile_nodeUvThree)
    pm.connectAttr(placement_node.verfile_nodeUvTwo, file_node.verfile_nodeUvTwo)
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
    
create_file_node('fileOne')