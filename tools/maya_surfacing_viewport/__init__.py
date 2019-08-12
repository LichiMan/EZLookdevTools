import pymel.core as pm
import logging
import tools.maya_surfacing_projects as ldts_mayaSurfacing
import tools.maya_common as ldts_mayaCommon
import tools.common as ldts_common
import tools.common.utilities as ldts_utils
import random

def set_wifreframe_color_black():
    '''sets the wireframe color to black'''
    transforms = pm.ls(type="transform")
    shape_transforms = ldts_mayaSurfacing.get_mesh_transforms(transforms)
    for mesh in shape_transforms:
        mesh.overrideEnabled.set(1)
        mesh.overrideRGBColors.set(0)
        mesh.overrideColor.set(1)


def set_wifreframe_color_none():
    '''removes the wireframe color for all meshes'''
    transforms = pm.ls(type="transform")
    shape_transforms = ldts_mayaSurfacing.get_mesh_transforms(transforms)
    for mesh in shape_transforms:
        mesh.overrideEnabled.set(0)


def set_wireframe_colors_per_project():
    '''sets the wireframe color for all meshes per 
    surfacing project. Sets it to black to start with,
    this implies that the mesh has not be assigned
    to any surfacing object yet'''
    set_wifreframe_color_black()
    projects = ldts_mayaSurfacing.get_projects()
    for project in projects:
        random.seed(project)
        wire_color = random.randint(1, 31)
        for surfacingObject in ldts_mayaSurfacing.get_objects(project):
            for mesh in surfacingObject.members():
                try:
                    mesh.overrideEnabled.set(1)
                    mesh.overrideRGBColors.set(0)
                    mesh.overrideColor.set(wire_color)
                except:
                    logging.error(
                        "Could not set override color for: %s, might belong to a display layer"
                        % mesh
                    )


def set_wireframe_colors_per_object():
    '''sets the wireframe color for all meshes per 
    surfacing object'''
    set_wifreframe_color_black()
    projects = ldts_mayaSurfacing.get_projects()
    for project in projects:
        for surfacingObject in ldts_mayaSurfacing.get_objects(project):
            for mesh in surfacingObject.members():
                try:
                    mesh.overrideEnabled.set(1)
                    mesh.overrideRGBColors.set(1)
                    mesh.overrideColorRGB.set(
                        ldts_utils.get_random_color(surfacingObject)
                    )
                except:
                    logging.error(
                        "Could not set override color for: %s, might belong to a display layer"
                        % mesh
                    )

def set_materials_per_project():
    '''creates a material per surfacing project
    and assigns it'''
    delete_materials()
    projects = ldts_mayaSurfacing.get_projects()
    for project in projects:
        material = pm.shadingNode(
            "blinn",
            asShader=True,
            name=("surfMaterial_%s" % project),
        )
        pm.setAttr(
            "%s.surfMaterial" % material,
            str(project),
            force=True,
        )
        pm.select(project)
        pm.hyperShade(assign=material)
        material.color.set(
            ldts_utils.get_random_color(project)
        )

def set_materials_per_object():
    '''creates a material per surfacing object
    and assigns it'''
    delete_materials()
    projects = ldts_mayaSurfacing.get_projects()
    for project in projects:
        for surfacingObject in ldts_mayaSurfacing.get_objects(project):
            material = pm.shadingNode(
                "blinn",
                asShader=True,
                name=("surfMaterial_%s" % surfacingObject),
            )
            pm.setAttr(
                "%s.surfMaterial" % material,
                str(surfacingObject),
                force=True,
            )
            pm.select(surfacingObject)
            pm.hyperShade(assign=material)
            material.color.set(
                ldts_utils.get_random_color(surfacingObject)
            )

def delete_materials():
    '''deletes all materials that have surfMaterial attribute'''
    all_materials = pm.ls(type="blinn")
    materials = []
    for material in all_materials:
        if pm.hasAttr(material, "surfMaterial"):
            materials.append(material)
    pm.delete(materials)