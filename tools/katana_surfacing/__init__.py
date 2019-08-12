from Katana import Widgets, FnGeolib, Nodes3DAPI, NodegraphAPI
import tools.common.utilities as common_utilities

def get_locations_hasattr(node, search_location, cel_expression):
    """Get all locations matching a cel_expression, at a location generated at a given
    a node"""
    collector = Widgets.CollectAndSelectInScenegraph(cel_expression, search_location)
    matchedLocationPaths = collector.collectAndSelect(select=False, node=node)
    return matchedLocationPaths


def get_attribute_values(node, locations, attribute_name):
    """Gets a list of unique values for the attribute_name, cooking the locations"""
    runtime = FnGeolib.GetRegisteredRuntimeInstance()
    txn = runtime.createTransaction()
    client = txn.createClient()
    op = Nodes3DAPI.GetOp(txn, NodegraphAPI.GetNode(node.getName()))
    txn.setClientOp(client, op)
    runtime.commit(txn)

    attribute_values = []

    for location in locations:
        cooked_location = client.cookLocation(location)
        attrs = cooked_location.getAttrs()
        attribute = attrs.getChildByName(attribute_name)
        attribute_value = attribute.getChildByName("value").getValue()
        if attribute_value not in attribute_values:
            attribute_values.append(attribute_value)
    return attribute_values


def get_objects_attribute_values(node, attribute_name):
    """Lists EZSurfacing_objects at a given view node"""
    cel_expression = '//*{ hasattr("%s") }' % attribute_name
    search_location = "/root/world"
    attribute_locations = get_locations_hasattr(node, search_location, cel_expression)
    return get_attribute_values(node, attribute_locations, attribute_name)


def add_node_to_group_last(group_node, node, inputPort="in", outputPort="out"):
    """adds the node as the last before the group_node out"""
    node.setParent(group_node)
    node_inputPort = node.getInputPort(inputPort)
    node_outputPort = node.getOutputPort(outputPort)
    group_node_sendPort = group_node.getSendPort(inputPort)
    group_node_returnPort = group_node.getReturnPort(outputPort)

    last_out = group_node_returnPort.getConnectedPorts()[0]
    last_out.connect(node_inputPort)
    node_outputPort.connect(group_node_returnPort)


def create_EZ_collections(attribute_name):
    '''Creates a group stack with 1 collection create per attribute_name value found
    This can used to find values of EZSurf attributes as in
    #attribute_name = "geometry.arbitrary.EZSurfacing_object"
    #attribute_name = "geometry.arbitrary.EZSurfacing_project"'''
    rootNode = NodegraphAPI.GetRootNode()
    selected_node = get_selected_nodes(single=True)
    node_outPort = selected_node.getOutputPort("out")
    EZSurfacing_projects = get_objects_attribute_values(selected_node, attribute_name)
    group_stack = NodegraphAPI.CreateNode("GroupStack", rootNode)
    group_stack.setName("EZSurfacing_collections")
    group_stack_inputPort = group_stack.getInputPort("in")
    node_outPort.connect(group_stack_inputPort)
    collections_name_list = []
    position_y = 0
    for EZSurfacing_project in EZSurfacing_projects:
        collection_create = NodegraphAPI.CreateNode("CollectionCreate", rootNode)
        collection_name = "EZ%s" % EZSurfacing_project
        collection_create.setName(collection_name)
        collections_name_list.append(EZSurfacing_project)
        # collection_create_location = collection_create.getParameter('/')
        # collection_create_location.setValue(location,0)
        collection_create_name = collection_create.getParameter("name")
        collection_create_name.setValue("EZ%s" % EZSurfacing_project, 0)
        collection_create_cel = collection_create.getParameter("CEL")
        collection_create_cel.setValue(
            '/root/world//*{attr("%s.value") == "%s"}'
            % (attribute_name, EZSurfacing_project),
            0,
        )
        add_node_to_group_last(group_stack, collection_create)

        NodegraphAPI.SetNodePosition(collection_create, (0, position_y))
        position_y = position_y - 50
    return collections_name_list


def get_selected_nodes(single=False):
    nodes = NodegraphAPI.GetAllSelectedNodes()
    if single:
        if len(nodes) != 1:
            raise RuntimeError("Please select 1 node.")
        return nodes[0]
    else:
        return nodes


def create_EZ_viewer_settings(attribute_name):
    rootNode = NodegraphAPI.GetRootNode()
    material_stack = NodegraphAPI.CreateNode("GroupStack", rootNode)
    material_stack.setName("EZSurfacing_viewer_settings")
    selected_node = get_selected_nodes(single=True)
    attribute_values = get_objects_attribute_values(selected_node, attribute_name)
    position_y = 0

    for attribute_value in attribute_values:
        random_color = common_utilities.get_random_color(attribute_value)
        viewer_settings = NodegraphAPI.CreateNode("ViewerObjectSettings", rootNode)
        viewer_settings.setName("viewerColor_%s" % attribute_value)
        add_node_to_group_last(material_stack, viewer_settings, inputPort="input")

        viewer_settings_value = viewer_settings.getParameter(
            "args.viewer.default.drawOptions.color"
        )
        viewer_settings_value.getChild("value").getChild("i0").setValue(
            random_color[0], 0
        )
        viewer_settings_value.getChild("value").getChild("i1").setValue(
            random_color[1], 0
        )
        viewer_settings_value.getChild("value").getChild("i2").setValue(
            random_color[2], 0
        )
        viewer_settings_value.getChild("enable").setValue(True, 0)

        cel_statement = '/root/world//*{attr("%s.value") == "%s"}' % (
            attribute_name,
            attribute_value,
        )
        viewer_settings.getParameter("CEL").setValue(cel_statement, 0)

        NodegraphAPI.SetNodePosition(viewer_settings, (0, position_y))
        position_y = position_y - 50


def create_EZ_materials(attribute_name, assign_random_color=False):
    rootNode = NodegraphAPI.GetRootNode()
    material_stack = NodegraphAPI.CreateNode("GroupStack", rootNode)
    material_stack.setName("EZSurfacing_materials")
    selected_node = get_selected_nodes(single=True)
    attribute_values = get_objects_attribute_values(selected_node, attribute_name)
    position_y = 0
    for attribute_value in attribute_values:
        material_group = NodegraphAPI.CreateNode("Group", rootNode)
        material_group.setName("EZMtl_%s" % attribute_value)
        material_group_inputPort = material_group.addInputPort("in")
        material_group_outputPort = material_group.addOutputPort("out")

        material_group_sendPort = material_group.getSendPort("in")
        material_group_returnPort = material_group.getReturnPort("out")
        material_group_sendPort.connect(material_group_returnPort)

        add_node_to_group_last(material_stack, material_group)
        NodegraphAPI.SetNodePosition(material_group, (0, position_y))

        material_merge = NodegraphAPI.CreateNode("Merge", rootNode)
        material_merge.setName("Mtl_merge_%s" % attribute_value)
        material_merge_inputPort = material_merge.addInputPort("in")
        material_merge_materialPort = material_merge.addInputPort("material")

        add_node_to_group_last(material_group, material_merge)
        NodegraphAPI.SetNodePosition(material_merge, (0, -150))

        material_network = NodegraphAPI.CreateNode("NetworkMaterial", rootNode)
        material_network.getParameter("name").setValue(
            "Mtl_network_%s" % attribute_value, 0
        )
        material_network_bxdf = material_network.addShaderInputPort("prman", "bxdf")
        material_network_outputPort = material_network.getOutputPort("out")
        material_network.setParent(material_group)
        material_network_outputPort.connect(material_merge_materialPort)

        NodegraphAPI.SetNodePosition(material_network, (250, -100))

        random_color = common_utilities.get_random_color(attribute_value)

        PxrSurface = NodegraphAPI.CreateNode("PrmanShadingNode", rootNode)
        PxrSurface_nodeType = PxrSurface.getParameter("nodeType")
        PxrSurface_nodeType.setValue("PxrSurface", 0)
        PxrSurface.checkDynamicParameters()
        PxrSurface_nodeType_name = PxrSurface.getParameter("name")
        PxrSurface_nodeType_name.setExpression(
            '"PxrSurface_"+getParent().getNodeName()', 0
        )
        PxrSurface_nodeType_name.setExpressionFlag(True)
        if assign_random_color:
            PxrSurface.getParameter("parameters.diffuseColor").getChild(
                "enable"
            ).setValue(True, 0)
            PxrSurface.getParameter("parameters.diffuseColor.value.i0").setValue(
                random_color[0], 0
            )
            PxrSurface.getParameter("parameters.diffuseColor.value.i1").setValue(
                random_color[1], 0
            )
            PxrSurface.getParameter("parameters.diffuseColor.value.i2").setValue(
                random_color[2], 0
            )

        PxrSurface.setParent(material_group)
        PxrSurface_outputPort = PxrSurface.getOutputPort("out")
        PxrSurface_outputPort.connect(material_network_bxdf)
        NodegraphAPI.SetNodePosition(PxrSurface, (250, -50))

        material_assign = NodegraphAPI.CreateNode("MaterialAssign", rootNode)

        add_node_to_group_last(material_group, material_assign, inputPort="input")

        cel_statement = '/root/world//*{attr("%s.value") == "%s"}' % (
            attribute_name,
            attribute_value,
        )
        material_assign.getParameter("CEL").setValue(cel_statement, 0)
        assignment = material_assign.getParameter("args.materialAssign.value")
        assignment.setExpression(
            'scenegraphLocationFromNode(getNode("%s"))' % material_network.getName()
        )

        NodegraphAPI.SetNodePosition(material_assign, (0, -200))

        position_y = position_y - 50
