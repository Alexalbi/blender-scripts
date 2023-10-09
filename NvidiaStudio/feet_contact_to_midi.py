import bpy
import os
from numpy import interp
from midiutil.MidiFile import MIDIFile

scene = bpy.context.scene

# get the object data
obj = bpy.data.objects["Feet Contact"]
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# initialize midi data
trackCount = 4
mf = MIDIFile(trackCount)

# set the start time to the origin
time = 0
# set the tempo so it syncs nicealy with the fps
fps = bpy.context.scene.render.fps
tempo = fps * 6

# add a track for each biome
trackNames = ["Dirt Track", "Wooden Bridge", "Rocky Track", "Bushes Track"]
for index, trackName in enumerate(trackNames):
    mf.addTrackName(index, time, trackName)
    mf.addTempo(index, time, tempo)

# we dont use channels here
channel = 0

# initilizes the contact detection
contact_L_old = True
contact_R_old = True

# iterate over all the frames
for frame in range(scene.frame_start, scene.frame_end + 1):
    # set the playhead to the current frame
    scene.frame_current = frame
    # realize the objects data
    obj_real = bpy.context.object.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    
    # get the attributes from the geonodes setup
    contact_R = obj_real.attributes['contact_R'].data[0].value
    contact_L = obj_real.attributes['contact_L'].data[0].value
    biome_R = obj_real.attributes['biome_R'].data[0].value
    biome_L = obj_real.attributes['biome_L'].data[0].value
    speed = obj_real.attributes['speed'].data[0].value

    # compute the new contact detection
    new_contact_R = contact_R and not(contact_R_old)
    new_contact_L = contact_L and not(contact_L_old)

    if new_contact_R or new_contact_L:
        pitch = 24 # note C1
        duration = 1
        # interpolates midi note volume depending on the animation speed
        volume = int(interp(speed, [1, 6], [10, 127]))
        time = (frame - scene.frame_start) / 10
        if new_contact_R:
            track = biome_R
        else:
            track = biome_L
        # add the midi note to the midifile object
        mf.addNote(track, channel, pitch, time, duration, volume)

    # set contact values for next iteration
    contact_R_old = contact_R
    contact_L_old = contact_L

# sets the filepath for the midi file in the blend file directory
filename = "nvidia miditrack.mid"
blendpath = bpy.data.filepath
directory = os.path.dirname(blendpath)
filepath = os.path.join(directory, filename)

# write the midifile to the output path
with open(filepath, 'wb') as outf:
    mf.writeFile(outf)
        
