from Katana import Widgets, FnGeolib, Nodes3DAPI, NodegraphAPI

def get_locations_hasattr(node, search_location, cel_expression):
    """Get all locations matching a cel_expression, at a location generated at a given
    a node"""
    collector = Widgets.CollectAndSelectInScenegraph(cel_expression, search_location)
    matchedLocationPaths = collector.collectAndSelect(select=False, node=node)
    return matchedLocationPaths

def get_selected_nodes(single=False):
    """Get selected nodes from the node graph, if single is given will
    check if a single node is selected"""
    nodes = NodegraphAPI.GetAllSelectedNodes()
    if single:
        if len(nodes) != 1:
            raise RuntimeError("Please select 1 node.")
        return nodes[0]
    else:
        return nodes

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