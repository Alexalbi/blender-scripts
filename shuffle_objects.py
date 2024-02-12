import bpy
from copy import copy
from random import shuffle

objSources = bpy.context.selected_objects
objTargetsTransform = [[copy(objSource.location), copy(objSource.rotation_euler)] for objSource in objSources]
shuffle(objTargetsTransform)

for objSource, objTargetTransform in zip(objSources, objTargetsTransform):
    objSource.location = objTargetTransform[0]
    objSource.rotation_euler = objTargetTransform[1]
    