import bpy

# initializing the data of the five animation states of our character
animation_names = ["Walk Heavy", "Walk Normal", "Run Normal", "Run Fast", "Run Fastest"]
strips = []
for name in animation_names:
    armature = bpy.data.objects[name]
    strips.append(armature.animation_data.nla_tracks[name].strips[name])

# selecting the 02 Strip Time object
obj = bpy.data.objects["02 Strip Time"]
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

scene = bpy.context.scene

# iterate over all the frame in our animation
for frame in range(scene.frame_start, scene.frame_end + 2):
    # set the playhead to the current frame
    scene.frame_current = frame
    # realize the objects data
    obj_real = bpy.context.object.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    # get the attributes from the geonodes setup
    anim_factor = obj_real.attributes["anim_factor"].data[0].value

    # set the NLA evaluation time of each animation as keyframe
    for strip in strips:
        strip_length = strip.action_frame_end
        strip.strip_time = (strip_length - 1) * (anim_factor % 1) + 1
        strip.keyframe_insert(data_path="strip_time", frame=frame)
