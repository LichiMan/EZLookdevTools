"""
.. module:: maya
   :synopsis: general maya material utilities.

.. moduleauthor:: Ezequiel Mastrasso

"""

import logging
import pymel.core as pm

from lookdevtools.common import utils
from lookdevtools.common.constants import ATTR_SURFACING_PROJECT
from lookdevtools.common.constants import ATTR_SURFACING_OBJECT
from lookdevtools.common.constants import ATTR_MATERIAL
from lookdevtools.common.constants import ATTR_MATERIAL_ASSIGN
from lookdevtools.common.constants import ATTR_MATERIAL_VP

logger = logging.getLogger(__name__)


def create_file_node(name=None):
    """
    Create a file node, and its 2dPlacement Node.

    Kwargs:
        name (str): file node name

    Returns:
        PyNode. Image file node

    """
    file_node = pm.shadingNode(
        'file', name=name, asTexture=True, isColorManaged=True)
    placement_name = '%s_place2dfile_nodeture' % name
    placement_node = pm.shadingNode(
        'place2dTexture', name=placement_name, asUtility=True)
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


def create_shader(type='PxrSurface'):
    """
    Create shaders and shading groups.

    Kwargs:
        type (str): type of material shader to create, for ie 'blinn'
        tag (str): tag to set in ATTR_MATERIAL, usually the
                   surfacing project or surfacing object

    Returns:
        tuple. PyNode shader, and PyNode shading_group

    """
    shader, shading_group = pm.createSurfaceShader(type)
    pm.setAttr('%s.%s' % (shading_group, ATTR_MATERIAL), '', force=True)
    pm.setAttr('%s.%s' % (shading_group, ATTR_MATERIAL_ASSIGN), '', force=True)
    pm.setAttr('%s.%s' % (shading_group, ATTR_MATERIAL_VP), '', force=True)
    return shader, shading_group
