"""
.. module:: viewport
   :synopsis: maya viewport utilities.

.. moduleauthor:: Ezequiel Mastrasso

# TODO (eze) use maya render setup for viewport materials
"""

import random
import logging

import pymel.core as pm

from lookdevtools import common
from lookdevtools.common import utils
from lookdevtools.maya import maya
from lookdevtools.maya.maya import materials
from lookdevtools.maya import surfacing_projects
from lookdevtools.common.constants import ATTR_MATERIAL
from lookdevtools.common.constants import ATTR_MATERIAL_ASSIGN
from lookdevtools.common.constants import ATTR_MATERIAL_VP
from lookdevtools.common import constants

logger = logging.getLogger(__name__)


def set_wifreframe_color_black():
    """Set the wireframe color to black in all mesh objects."""
    transforms = pm.ls(type="transform")
    shape_transforms = surfacing_projects.get_mesh_transforms(transforms)
    for mesh in shape_transforms:
        mesh.overrideEnabled.set(1)
        mesh.overrideRGBColors.set(0)
        mesh.overrideColor.set(1)


def set_wifreframe_color_none():
    """Remove the wireframe color in all mesh objects."""
    transforms = pm.ls(type="transform")
    shape_transforms = surfacing_projects.get_mesh_transforms(transforms)
    for mesh in shape_transforms:
        mesh.overrideEnabled.set(0)


def set_wireframe_colors_per_project():
    """
    Set the wireframe color per surfacing project.

    For all meshes, sets it to black to start with,
    this implies that the mesh has not be assigned
    to any surfacing object yet will show black in the VP

    """
    set_wifreframe_color_black()
    projects = surfacing_projects.get_surfacing_projects()
    for project in projects:
        random.seed(project)
        wire_color = random.randint(1, 31)
        for surfacingObject in surfacing_projects.get_surfacing_objects(project):
            for mesh in surfacingObject.members():
                try:
                    mesh.overrideEnabled.set(1)
                    mesh.overrideRGBColors.set(0)
                    mesh.overrideColor.set(wire_color)
                except:
                    logger.error('Could not set override color for: %s, might '
                                 'belong to a display layer'
                                 % mesh
                                 )


def set_wireframe_colors_per_object():
    """
    Set the wireframe color per surfacing object.

    For all meshes, sets it to black to start with,
    this implies that the mesh has not be assigned
    to any surfacing object yet will show black in the VP

    """
    set_wifreframe_color_black()
    projects = surfacing_projects.get_surfacing_projects()
    for project in projects:
        for surfacingObject in surfacing_projects.get_surfacing_objects(project):
            for mesh in surfacingObject.members():
                try:
                    mesh.overrideEnabled.set(1)
                    mesh.overrideRGBColors.set(1)
                    mesh.overrideColorRGB.set(
                        utils.get_random_color(surfacingObject)
                    )
                except:
                    logger.error('Could not set override color for: %s, might '
                                 'belong to a display layer'
                                 % mesh
                                 )


def set_materials_per_object():
    """Create a material per surfacing project and assigns it"""
    delete_materials()
    projects = surfacing_projects.get_surfacing_projects()
    for project in projects:
        for obj in surfacing_projects.get_surfacing_objects(project):
            shader, shading_group = materials.create_shader(
                type='blinn')
            pm.select(obj)
            meshes = pm.ls(sl=True)
            pm.sets(shading_group, forceElement=meshes)
            pm.select(None)
            shader.color.set(
                utils.get_random_color(obj)
            )
            pm.setAttr('%s.%s' % (shading_group, ATTR_MATERIAL),
                       'obj', force=True)
            pm.setAttr('%s.%s' %
                       (shading_group, ATTR_MATERIAL_ASSIGN), obj.name(), force=True)
            pm.setAttr('%s.%s' % (shading_group, ATTR_MATERIAL_VP),
                       'color', force=True)


def set_materials_per_project():
    """Create a material per surfacing project and assigns it"""
    delete_materials()
    projects = surfacing_projects.get_surfacing_projects()
    for project in projects:
        shader, shading_group = materials.create_shader(
            type='blinn')
        pm.select(project)
        meshes = pm.ls(sl=True)
        pm.sets(shading_group, forceElement=meshes)
        pm.select(None)
        shader.color.set(
            utils.get_random_color(project)
        )
        pm.setAttr('%s.%s' % (shading_group, ATTR_MATERIAL),
                   'project', force=True)
        pm.setAttr('%s.%s' %
                   (shading_group, ATTR_MATERIAL_ASSIGN), project.name(), force=True)
        pm.setAttr('%s.%s' % (shading_group, ATTR_MATERIAL_VP),
                   'color', force=True)


def delete_materials():
    """delete all material networks that have surfacing attributes"""
    all_shading_groups = pm.ls(type="shadingEngine")
    to_delete = []
    for shading_group in all_shading_groups:
        if pm.hasAttr(shading_group, ATTR_MATERIAL):
            to_delete.append(shading_group)
    pm.delete(to_delete)


def delete_materials_viewport(type=None):
    """
    delete all material networks that have surfacing attributes.

    Kwargs:
        type (str): type of vp material to delete, usually 'color', or 'pattern'

    """
    all_shading_groups = pm.ls(type="shadingEngine")
    to_delete = []
    for shading_group in all_shading_groups:
        if pm.hasAttr(shading_group, ATTR_MATERIAL_VP):
            to_delete.append(shading_group)
    pm.delete(to_delete)
