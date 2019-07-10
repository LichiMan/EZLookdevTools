from Katana import Widgets, FnGeolib, Nodes3DAPI, NodegraphAPI

def get_locations_hasattr(node, search_location, cel_expression):
    '''Get all locations matching a cel_expression, at a location generated at a given
    a node'''
    collector = Widgets.CollectAndSelectInScenegraph(cel_expression, search_location)
    matchedLocationPaths = collector.collectAndSelect(select=False, node= node)
    return matchedLocationPaths 

def get_attribute_values(node, attribute_locations, attribute_name):
    '''Gets a list of values for the attribute_name, cooking the attribute locations'''
    runtime = FnGeolib.GetRegisteredRuntimeInstance()
    txn = runtime.createTransaction()
    client = txn.createClient()
    op = Nodes3DAPI.GetOp(txn, NodegraphAPI.GetNode(node.getName()))
    txn.setClientOp(client, op)
    runtime.commit(txn)

    EZ_attribute_values = []

    for location in attribute_locations:
        cooked_location = client.cookLocation(location)
        attrs = cooked_location.getAttrs()
        attribute = attrs.getChildByName(attribute_name)
        attribute_value = attribute.getChildByName('value').getValue()
        if attribute_value not in EZ_attribute_values:
            EZ_attribute_values.append (attribute_value)
    return EZ_attribute_values

def get_objects_attribute_values(node, attribute_name):
    '''Lists EZSurfacing_objects at a given view node'''
    cel_expression = '//*{ hasattr("%s") }' % attribute_name
    search_location = '/root/world'
    attribute_locations = get_locations_hasattr(node, search_location, cel_expression)
    return get_attribute_values(node, attribute_locations, attribute_name)

def add_node_to_group(group_node, node):
    '''adds the node as the last before the group_node out'''
    node.setParent(group_node)
    node_inputPort = node.getInputPort('in')
    node_outputPort = node.getOutputPort('out')
    group_node_sendPort = group_node.getSendPort('in')
    group_node_returnPort = group_node.getReturnPort('out')

    last_out = group_node_returnPort.getConnectedPorts()[0]
    last_out.connect(node_inputPort)
    node_outputPort.connect(group_node_returnPort)

def create_EZ_collections(attribute_name):
    '''Creates a group stack with 1 collection create per attribute_name value found
    This can used to find values of EZSurf attributes as in
    #attribute_name = "geometry.arbitrary.EZSurfacing_object"
    #attribute_name = "geometry.arbitrary.EZSurfacing_project"'''
    nodes = NodegraphAPI.GetAllSelectedNodes()
    if len(nodes)!=1:
       raise RuntimeError, 'Please select 1 node.'
    rootNode = NodegraphAPI.GetRootNode()
    node_outPort = nodes[0].getOutputPort('out')
    EZSurfacing_projects = get_objects_attribute_values(nodes[0],attribute_name) 
    group_stack = NodegraphAPI.CreateNode('GroupStack', rootNode)
    group_stack.setName('EZPrjs')
    group_stack_inputPort = group_stack.getInputPort('in')
    node_outPort.connect(group_stack_inputPort)
    for EZSurfacing_project in EZSurfacing_projects:
        collection_create = NodegraphAPI.CreateNode('CollectionCreate', rootNode)
        collection_create.setName('EZ%s' % EZSurfacing_project)
        #collection_create_location = collection_create.getParameter('/')
        #collection_create_location.setValue(location,0)
        collection_create_name = collection_create.getParameter('name')
        collection_create_name.setValue('EZ%s' % EZSurfacing_project,0)
        collection_create_cel = collection_create.getParameter('CEL')
        collection_create_cel.setValue('/root/world//*{attr("%s.value") == "%s"}' % (attribute_name, EZSurfacing_project),0)
        add_node_to_group(group_stack, collection_create)