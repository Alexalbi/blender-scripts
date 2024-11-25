import bpy

def select_directly_connected_nodes_to_group_input_socket(socket_name):
    # Ensure an active object with geometry nodes is selected
    obj = bpy.context.active_object
    if obj is None or obj.modifiers is None:
        print("No active object with modifiers found.")
        return

    # Find the active geometry nodes modifier
    geo_nodes_modifier = None
    for mod in obj.modifiers:
        if mod.type == 'NODES' and mod.node_group:
            geo_nodes_modifier = mod
            print(mod.name)
            break
        
    object = bpy.context.active_object
    geo_nodes_modifier = object.modifiers.active
    print(geo_nodes_modifier.name)

    if not geo_nodes_modifier:
        print("No active geometry nodes modifier found.")
        return
    
    # Access the node tree of the geometry nodes
    node_tree = geo_nodes_modifier.node_group

    # Deselect all nodes initially
    for node in node_tree.nodes:
        node.select = False

    # Set to store all nodes to be selected
    nodes_to_select = set()

    # Iterate over all Group Input nodes
    for node in node_tree.nodes:
        if node.type == 'GROUP_INPUT':
            # Check each output socket of the Group Input node
            for socket in node.outputs:
                if socket.name == socket_name:
                    # Select nodes directly connected to this socket
                    for link in socket.links:
                        connected_node = link.to_node
                        if connected_node:
                            nodes_to_select.add(connected_node)

    # Select all identified nodes
    for node in nodes_to_select:
        node.select = True
        print(node.name)

    print(f"Selected {len(nodes_to_select)} nodes directly connected to '{socket_name}' across all Group Input nodes.")

# Usage example
socket_name = "UV Scale"  # Replace with the name of your target socket
select_directly_connected_nodes_to_group_input_socket(socket_name)
