import bpy
import os

# Define a custom property to store scene names
bpy.types.WindowManager.scene_names = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)

# Operator to add the current scene name to the list
class AddSceneNameToList(bpy.types.Operator):
    bl_idname = "scene.add_scene_name_to_list"
    bl_label = "Add Scene Name to List"
    
    def execute(self, context):
        scene_name = bpy.context.scene.name
        if scene_name not in bpy.context.window_manager.scene_names:
            item = bpy.context.window_manager.scene_names.add()
            item.name = scene_name
            self.report({'INFO'}, f"Added '{scene_name}' to the list")
        else:
            self.report({'WARNING'}, f"Scene '{scene_name}' already exists in the list")
        return {'FINISHED'}

# Operator to remove a scene name from the list
class RemoveSceneNameFromList(bpy.types.Operator):
    bl_idname = "scene.remove_scene_name_from_list"
    bl_label = "Remove Scene Name from List"
    
    index: bpy.props.IntProperty()

    def execute(self, context):
        scene_names = bpy.context.window_manager.scene_names
        if 0 <= self.index < len(scene_names):
            scene_name = scene_names[self.index].name
            scene_names.remove(self.index)
            self.report({'INFO'}, f"Removed '{scene_name}' from the list")
        else:
            self.report({'WARNING'}, "Invalid index")
        return {'FINISHED'}

# Operator to move a scene name up in the list
class MoveSceneNameUp(bpy.types.Operator):
    bl_idname = "scene.move_scene_name_up"
    bl_label = "Move Scene Name Up"
    
    index: bpy.props.IntProperty()

    def execute(self, context):
        scene_names = bpy.context.window_manager.scene_names
        if 0 < self.index < len(scene_names):
            scene_names.move(self.index, self.index - 1)
            self.report({'INFO'}, f"Moved scene up")
        else:
            self.report({'WARNING'}, "Invalid operation")
        return {'FINISHED'}

# Operator to move a scene name down in the list
class MoveSceneNameDown(bpy.types.Operator):
    bl_idname = "scene.move_scene_name_down"
    bl_label = "Move Scene Name Down"
    
    index: bpy.props.IntProperty()

    def execute(self, context):
        scene_names = bpy.context.window_manager.scene_names
        if 0 <= self.index < len(scene_names) - 1:
            scene_names.move(self.index, self.index + 1)
            self.report({'INFO'}, f"Moved scene down")
        else:
            self.report({'WARNING'}, "Invalid operation")
        return {'FINISHED'}

# Panel to display the list of scene names
class SCENE_PT_scene_list_panel(bpy.types.Panel):
    bl_label = "Batch Render Scenes"
    bl_idname = "SCENE_PT_scene_list_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Scene Names:")

        for i, item in enumerate(bpy.context.window_manager.scene_names):
            row = layout.row(align=True)
            row.label(text=item.name)
            row.operator("scene.move_scene_name_up", icon='TRIA_UP', text="").index = i
            row.operator("scene.move_scene_name_down", icon='TRIA_DOWN', text="").index = i
            row.operator("scene.remove_scene_name_from_list", text="", icon='X').index = i
        
        row = layout.row()
        row.operator("scene.add_scene_name_to_list", text="Add Current Scene")
        row = layout.row()
        row.operator("scene.launch_scenes_render", text="Launch Scenes Render")

# Operator to launch render
class LaunchScenesRender(bpy.types.Operator):
    bl_idname = "scene.launch_scenes_render"
    bl_label = "Launch Scene Render"
    
    def execute(self, context):
        arguments = ["--background", "-a", "-S"]
        filepath = bpy.data.filepath
        blenderpath = bpy.app.binary_path
        scenes = bpy.context.window_manager.scene_names
        commands = []
        for scene in scenes:
            commands.append(f"\"{blenderpath}\" --background \"{filepath}\" --scene \"{scene.name}\" -a")
        command = ' & '.join(commands)
        command = "start /B start cmd.exe @cmd /k \"" + command + "\""
        os.system(command) 
        print(command)
        return {'FINISHED'}

# Register the addon
def register():
    bpy.utils.register_class(AddSceneNameToList)
    bpy.utils.register_class(RemoveSceneNameFromList)
    bpy.utils.register_class(MoveSceneNameUp)
    bpy.utils.register_class(MoveSceneNameDown)
    bpy.utils.register_class(SCENE_PT_scene_list_panel)
    bpy.utils.register_class(LaunchScenesRender)

def unregister():
    bpy.utils.unregister_class(AddSceneNameToList)
    bpy.utils.unregister_class(RemoveSceneNameFromList)
    bpy.utils.unregister_class(MoveSceneNameUp)
    bpy.utils.unregister_class(MoveSceneNameDown)
    bpy.utils.unregister_class(SCENE_PT_scene_list_panel)
    bpy.utils.unregister_class(LaunchScenesRender)

if __name__ == "__main__":
    register()
