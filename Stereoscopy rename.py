import bpy
import os
import re

# get the current scene
scene = bpy.context.scene

# get the render path
renderPath = scene.render.filepath
renderPath = os.path.dirname(renderPath)

# list rendered files
files = os.listdir(renderPath)

# build the multi view dictionary
sceneViews = scene.render.views.keys()
viewsDict = {}
for viewName in sceneViews:
    viewSuffix = scene.render.views[viewName].camera_suffix
    viewsDict[viewSuffix] = viewName
    
print(viewsDict)

# set the files pattern
pattern = r"(.+)*(\d{4})(.+)(\..+)"

for file in files:
    # match the pattern
    matched = re.match(pattern, file)
    # if the current file matches the pattern
    if matched:
        groups = matched.groups()
        # if the suffix is in our dictionary
        if groups[2] in viewsDict.keys():
            # rename the file
            newfile = viewsDict[groups[2]] + "_" + (groups[0] or "") + groups[1] + groups[3]
            os.rename(os.path.join(renderPath, file), os.path.join(renderPath, newfile))
