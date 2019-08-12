import pymel.core as pm
import logging
import os
import maya.mel as mel
import maya.cmds as mc
from PySide2 import QtWidgets
import traceback
import sys
import random
import tools.maya_common as ldts_mayaCommon
import tools.common as ldts_common
import tools.common.utilities as ldts_utils

def surfacingInit():
    """ Initializes the scene by creating the surfacing root
    an surfacing object, and runs the validation to create and
    connect the partition"""
    root = create_project_root()
    if not root.members:
        surfProject = create_project("project")
        surfObject = create_object(
            surfProject, "default_object"
        )
    validate_scene()


def create_project_root_node():
    """create projects root node"""
    surfacing_root = pm.createNode(
        "objectSet", name="surfacing_root"
    )
    surfacing_root.setAttr(
        "surfacing_root", "", force=True
    )
    return surfacing_root


def create_project_root():
    """create projects root if it doesnt exist"""
    if not get_project_root():
        surfacing_root = create_project_root_node()
        return surfacing_root
    else:
        return get_project_root()


def create_project(name=None):
    """Creates a surfacing project"""
    if not name:
        name = "project"
    surfacing_project = pm.createNode(
        "objectSet", name=name
    )
    surfacing_project.setAttr(
        ldts_common.ATTR_SURFACING_PROJECT, "", force=True
    )
    create_object(surfacing_project)
    get_project_root().add(surfacing_project)
    update_partition()
    return surfacing_project


def create_object(project, name=None):
    """Creates a surfacing Object under a given project"""
    if get_project_root() and is_project(project):
        if not name:
            name = "object"
        surfacing_set = pm.createNode(
            "objectSet", name=name
        )
        surfacing_set.setAttr(
            ldts_common.ATTR_SURFACING_OBJECT, "", force=True
        )
        project.add(surfacing_set)
    else:
        raise Exception(
            "No project root, or project given is not valid"
        )


def update_partition():
    """Recreates the partition node, and reconnects to all the surfacing nodes"""
    partitions = [
        item
        for item in pm.ls(type="partition")
        if item.hasAttr("surfacing_partition")
    ]
    for each in partitions:
        logging.info(
            "disconnecting existing partition: %s" % each
        )
        each.sets.disconnect()
        pm.delete(each)
        logging.info("deleted partition")
    surfacing_partition = pm.createNode(
        "partition", name="surfacing_partition"
    )
    logging.info(
        "partition created: %s" % surfacing_partition
    )
    surfacing_partition.setAttr(
        "surfacing_partition", "", force=True
    )
    for project in get_projects():
        for object in get_objects(project):
            pm.connectAttr(
                "%s.partition" % object,
                surfacing_partition.sets,
                na=True,
            )
            logging.info(
                "partition connected: %s " % object
            )
    pass


def get_project_root():
    """Gets the project root node"""
    objSetLs = [
        item
        for item in pm.ls(type="objectSet")
        if item.hasAttr("surfacing_root")
    ]
    if len(objSetLs) == 0:
        logging.info(
            "surfacing_root node found, creating one"
        )
        return create_project_root_node()
    elif len(objSetLs) > 1:
        raise Exception(
            "more than 1 surfacing_root node found"
        )
    return objSetLs[0]


def get_projects():
    """Gets all surfacing Projects under the root"""
    objSetLs = [
        item
        for item in pm.ls(type="objectSet")
        if item.hasAttr(ldts_common.ATTR_SURFACING_PROJECT)
    ]
    return objSetLs


def delete_project(project):
    if is_project(project):
        pm.delete(project.members())


def get_objects(project):
    """Gets all surfacing Objects under the given project"""
    if is_project(project):
        return project.members()
    else:
        return []


def is_project(project):
    """Returns is project is of the type surfacing project"""
    if project.hasAttr(ldts_common.ATTR_SURFACING_PROJECT):
        return True
    else:
        return False


def is_texture_object(texture_object):
    """Returns is project is of the type surfacing Object"""
    if texture_object.hasAttr(ldts_common.ATTR_SURFACING_OBJECT):
        return True
    else:
        return False


def remove_invalid_members():
    """pops all not-allowd member types
    Allowed:
     objectSets inside the project_root
     objectSets inside each texture_project
     transforms (that have a mesh) inside texture_objects"""
    project_root = get_project_root()
    for project in project_root.members():
        if (
            not project.type() == "objectSet"
        ):  # add check for attr
            project_root.removeMembers([project])
    for project in get_projects():
        for object in get_objects(
            project
        ):  # add check for attr
            if not object.type() == "objectSet":
                project.removeMembers([object])
            else:
                for member in object.members():
                    if not member.type() == "transform":
                        logging.info(
                            "removing invalid member: %s"
                            % member
                        )
                        object.removeMembers([member])
                    elif not member.listRelatives(
                        type="mesh"
                    ):
                        logging.info(
                            "removing invalid member: %s"
                            % member
                        )
                        object.removeMembers([member])


def get_mesh_transforms(object_list):
    """Gets all the mesh shape transforms"""
    shapes_in_hierarchy = pm.listRelatives(
        object_list,
        allDescendents=True,
        path=True,
        f=True,
        type="mesh",
    )
    shapes_transforms = pm.listRelatives(
        shapes_in_hierarchy, p=True, path=True, f=True
    )
    return shapes_transforms


def add_member(texture_object, transform):
    """Adds the transform to the surfacing Object"""
    pm.sets(texture_object, transform, fe=True)


def add_mesh_transforms_to_object(
    texture_object, object_list
):
    """Adds all mesh shape transforms from the object list to a surfacing Object"""
    pm.select()
    if texture_object and object_list:
        if is_texture_object(texture_object):
            for item in object_list:
                for transform in get_mesh_transforms(item):
                    pm.select(transform)
                    add_member(texture_object, transform)

def validate_scene():
    """Removes not allowed or invalid members, updates the partition
    and the meshes attributes"""
    if get_project_root:
        remove_invalid_members()
        update_partition()
        update_mesh_attributes()
    # check all object sets of type texture_object contain only shapes
    pass


def abc_export(geo_list, file_path):
    if geo_list and file_path:
        roots = " -root |" + " -root |".join(
            [str(x) for x in geo_list]
        )
        mel_cmd = (
            r'AbcExport -j "-frameRange 0 0 -uvWrite -dataFormat ogawa -attrPrefix surfacing '
            + roots
            + " -file "
            + (file_path + '"')
        )
        mel.eval(mel_cmd)
        logging.info(
            "Succesful Alembic export to: %s" % file_path
        )

def export_project(project, subdiv=1, single_export=True, folder_path = False):
    """Export surfacing Project"""
    current_file = pm.sceneName()
    if single_export:
        check_scene_state()
    if not folder_path:
        folder_path = ldts_mayaCommon.get_folder_path()
    project_geo_list = []
    if ldts_utils.is_directory(folder_path) and is_project(project):
        for each in get_objects(project):
            merged_geo = merge_texture_object(each)
            if merged_geo:
                project_geo_list.append(merged_geo)
        if project_geo_list:
            if subdiv:
                for geo in project_geo_list:
                    logging.info(
                        "subdivision level: %s" % subdiv
                    )
                    logging.info(
                        "subdividing merged members: %s"
                        % geo
                    )
                    # -mth 0 -sdt 2 -ovb 1 -ofb 3 -ofc 0 -ost 0 -ocr 0 -dv 3 -bnr 1 -c 1 -kb 1
                    # -ksb 1 -khe 0 -kt 1 -kmb 1 -suv 1 -peh 0 -sl 1 -dpe 1 -ps 0.1 -ro 1 -ch 1
                    pm.polySmooth(
                        geo, mth=0, sdt=2, ovb=1, dv=subdiv
                    )
            export_file_path = os.path.join(
                folder_path, str(project) + ".abc"
            )
            abc_export(project_geo_list, export_file_path)
            export_surfacing_object_dir = os.path.join(
                folder_path, str(project)
            )
            ldts_utils.create_directoy(export_surfacing_object_dir)
            for geo in project_geo_list:
                export_root = " -root |" + geo
                export_surfacing_object_path = os.path.join(
                    export_surfacing_object_dir
                    + "/"
                    + geo
                    + ".abc"
                )
                abc_export(
                    [geo], export_surfacing_object_path
                )

    if single_export:
        pm.openFile(current_file, force=True)


def merge_texture_object(texture_object):
    """Merges all the meshs assigned to a surfacing Object for export"""
    try:
        members = texture_object.members()
        logging.info("Merging members: %s" % members)
        geo_name = "%s_geo" % str(texture_object)
        if len(members) > 1:
            geo = pm.polyUnite(*members, n=geo_name)
            return geo[0]
        else:
            logging.info(
                "single object found, skipping merge: %s"
                % members[0]
            )
            members[0].rename(geo_name)
            pm.parent(members[0], world=True)
            return members[0]
    except:
        traceback.print_exc(file=sys.stdout)
        logging.error(
            "Could not merge members of: %s"
            % texture_object
        )
        return False


def export_all_projects(subdiv=1, folder_path = None):
    """Export all surfacing Projects"""
    check_scene_state()
    if not folder_path:
        folder_path = ldts_mayaCommon.get_folder_path()
    current_file = pm.sceneName()
    for project in get_projects():
        export_project(
            project, subdiv=subdiv, single_export=False, folder_path = folder_path
        )
    pm.openFile(current_file, force=True)
    return True


def check_scene_state():
    '''check the scene state, if modified, will ask the
    user to save it'''
    if ldts_mayaCommon.unsaved_scene():
        if ldts_mayaCommon.save_scene_dialog():
            pm.saveFile(force=True)
        else:
            raise ValueError("Unsaved changes")


def update_mesh_attributes():
    """Adds the attributes to all the shapes transforms assigned to surfacing Objects
    This will be used later for quick shader/material creation and assignment"""
    for project in get_projects():
        project.setAttr(ldts_common.ATTR_SURFACING_PROJECT, project)
        logging.info(
            "Updating attributes for project: %s" % project
        )
        for texture_object_set in get_objects(project):
            logging.info(
                "----Updating attributes for object texture set: %s"
                % texture_object_set
            )
            texture_object_set.setAttr(
                ldts_common.ATTR_SURFACING_OBJECT, texture_object_set
            )
            members = texture_object_set.members()
            logging.info(
                "--------Updating mesh for meshes:"
            )
            logging.info("--------%s" % members)
            for member in members:
                member.setAttr(
                    ldts_common.ATTR_SURFACING_PROJECT,
                    project.name(),
                    force=True,
                )
                member.setAttr(
                    ldts_common.ATTR_SURFACING_OBJECT,
                    texture_object_set.name(),
                    force=True,
                )





