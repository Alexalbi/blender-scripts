import bpy
import subprocess 
import re

#Get geometry nodes


object = bpy.context.active_object
active = object.modifiers.active
activename = active.node_group.name
item_tree = bpy.data.node_groups[activename].interface.items_tree
nodes = bpy.data.node_groups[activename].nodes

initialinputs = ("<!-- wp:heading --> \n"
    "<h2 class=\"wp-block-heading\">Inputs</h2> \n"
    "<!-- /wp:heading -->")
initialoutputs = ("<!-- wp:heading --> \n"
    "<h2 class=\"wp-block-heading\">Outputs</h2> \n"
    "<!-- /wp:heading -->")
inputs = [initialinputs]
outputs = [initialoutputs]

inoutnamestart = ("<!-- wp:heading {\"level\":4} --> \n"
                "<h4 class=\"wp-block-heading\">")
inoutnameend = ("</h4> \n"
                "<!-- /wp:heading -->")
inoutnamestartpanel = ("<!-- wp:heading {\"level\":6,\"style\":{\"spacing\":{\"padding\":{\"left\":\"var:preset|spacing|20\"}}}} --> \n"
                "<h6 class=\"wp-block-heading\" style=\"padding-left:var(--wp--preset--spacing--20)\">")
inoutnameendpanel = ("</h6> \n"
                "<!-- /wp:heading -->")
inoutdescriptionstart = ("<!-- wp:paragraph {\"style\":{\"spacing\":{\"padding\":{\"left\":\"var:preset|spacing|20\"}}}} --> \n"
                "<p style=\"padding-left:var(--wp--preset--spacing--20)\">")
inoutdescriptionstartpanel = ("<!-- wp:paragraph {\"style\":{\"spacing\":{\"padding\":{\"left\":\"var:preset|spacing|40\"}}}} --> \n"
                "<p style=\"padding-left:var(--wp--preset--spacing--40)\">")
inoutdescriptionend = ("</p> \n"
                "<!-- /wp:paragraph -->")


descriptionstart = "<!-- wp:paragraph -->\n"
descriptionend = "\n<!-- /wp:paragraph -->"
tooldescription = bpy.data.node_groups[activename].asset_data.description
description = [descriptionstart + tooldescription + descriptionend]

skipped = []

for item in item_tree:
    if item.item_type != 'PANEL' and not item.hide_in_modifier:
        if item.in_out == "INPUT":
            if item.description != "":
                if item.parent.name == "":
                    inputname = inoutnamestart + item.name + inoutnameend
                    inputdescription = inoutdescriptionstart + item.description + inoutdescriptionend
                    inputs.append(inputname)
                    inputs.append(inputdescription)
                else:
                    inputname = inoutnamestartpanel + item.name + inoutnameendpanel
                    inputdescription = inoutdescriptionstartpanel + item.description + inoutdescriptionend
                    inputs.append(inputname)
                    inputs.append(inputdescription)
            else:
                skipped.append(item.name)
                    
        else:
            if item.description != "":
                inputname = inoutnamestart + item.name + inoutnameend
                inputdescription = inoutdescriptionstart + item.description + inoutdescriptionend
                outputs.append(inputname)
                outputs.append(inputdescription)
                
    if item.item_type == 'PANEL':
        inputpanel = inoutnamestart + item.name + inoutnameend
        inputs.append(inputpanel)
        if item.description != "":
            inputdescription = inoutdescriptionstart + item.description + inoutdescriptionend
            inputs.append(inputdescription)

fulldoc = "\n\n".join(description + inputs + outputs)

print(skipped)
subprocess.run("clip", text=True, input=fulldoc)
