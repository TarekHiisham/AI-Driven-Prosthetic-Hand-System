import bpy
import math
from queue import Queue
from threading import Thread
import time

communicationlayer = bpy.data.texts["communicationlayer.py"].as_module()

armature = bpy.data.objects['Armature']
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')
client_queue = Queue()

client_socket = communicationlayer.ClientSocket(client_queue = client_queue)
client_socket.start()

bone_order = [
    'thumb_bone2', 'thumb_bone3', 
    'index_bone1', 'index_bone2', 'index_bone3',
    'middle_bone1', 'middle_bone2', 'middle_bone3',
    'ring_bone1', 'ring_bone2', 'ring_bone3',
    'little_bone1', 'little_bone2', 'little_bone3'
]

frame = 1
def apply_pose():
    global frame
    if client_queue.empty():
        return 0.1  # Wait a bit, then check again
    
    row = client_queue.get()
    for i, angle in enumerate(row):
        bone_name = bone_order[i]
        bone = armature.pose.bones[bone_name]
        bone.rotation_mode = 'XYZ'
        bone.rotation_euler = (0, 0, math.radians(-angle))
        bone.keyframe_insert(data_path="rotation_euler", frame=frame)

    bpy.context.view_layer.update()
    frame += 30
    return .7

#Thread(target=rcv_data, daemon=True).start()
bpy.app.timers.register(apply_pose, first_interval=0.3)

