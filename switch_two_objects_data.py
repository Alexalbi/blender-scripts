import bpy

objSources = bpy.context.selected_objects
objSources[0].data, objSources[1].data = bpy.data.meshes[objSources[1].data.name], bpy.data.meshes[objSources[0].data.name]
