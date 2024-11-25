import bpy

def copy_group_sockets(subgroup_name, parent_group_name, connect_sockets=False):
    # Get the node trees for the parent and subgroup
    parent_group = bpy.data.node_groups.get(parent_group_name)
    subgroup = bpy.data.node_groups.get(subgroup_name)

    if not parent_group or not subgroup:
        print(f"Node groups '{parent_group_name}' or '{subgroup_name}' not found.")
        return
    
    # Find the subgroup node within the parent group
    subgroup_node = None
    for node in parent_group.nodes:
        if node.type == 'GROUP' and node.node_tree == subgroup:
            subgroup_node = node
            break

    if not subgroup_node:
        print(f"No node found in '{parent_group_name}' that uses '{subgroup_name}'.")
        return
    print(parent_group.nodes["Group Input"].inputs)
    # Copy input sockets from subgroup to parent group
    for input_socket in subgroup_node.inputs:
        new_input = parent_group.interface.new_socket(description='',socket_type=input_socket.socket_type, name=input_socket.name)
        # Copy default values and other properties
        if hasattr(input_socket, 'default_value'):
            if input_socket.bl_idname!='NodeSocketMenu':
                new_input.default_value = input_socket.default_value

    # Copy panel hierarchy (if any)
    def copy_panels(source_panels, target_node_tree):
        for panel in source_panels:
            new_panel = target_node_tree.inputs.new_panel(panel.name)
            for input_socket in panel.inputs:
                new_input = target_node_tree.inputs.get(input_socket.name)
                if new_input:
                    new_input.panel = new_panel.name

    copy_panels(subgroup.inputs, parent_group)

    # Optionally connect the new inputs
    if connect_sockets:
        for input_socket in subgroup_node.inputs:
            new_input = parent_group.inputs.get(input_socket.name)
            if new_input:
                for node in parent_group.nodes:
                    for socket in node.inputs:
                        if socket.name == input_socket.name and not socket.is_linked:
                            parent_group.links.new(new_input, socket)

    print(f"Copied sockets from '{subgroup_name}' to '{parent_group_name}'.")

# Usage
copy_group_sockets('Select Hem Profile', 'Geometry Nodes.003', connect_sockets=True)
