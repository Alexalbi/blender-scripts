import bpy

#Get geometry nodes


object = bpy.context.active_object
active = object.modifiers.active
activename = active.node_group.name
nodes = bpy.data.node_groups[activename].nodes
    
#loop through nodes
for node in nodes:
    #if node has the same idetifier
    if node.bl_rna.identifier == "NodeGroupInput":
        #select it
        node.select = True
        for output in node.outputs:
            if not(output.is_linked):
                output.hide = True
            else:
                output.hide = False
    else: node.select = False
        




