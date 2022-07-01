import bpy
import math

FILE_DIRECTORY = "/Users/nazimaniltepe/Documents/3D Models/Realistic_White_Male_Low_Poly/valid20220420/"
FILE_NAME = "Praying"
OBJECT_NAME = "unamed"
ARMATURE_NAME = "Armature"
FRAME_COUNT = bpy.context.scene.frame_end
FRAME_DURATION = 1 / 24

obj = bpy.data.objects[OBJECT_NAME]
obj_verts = obj.data.vertices
sorted_bones = bpy.context.object.pose.bones.values()
sorted_bones.sort(key=lambda x:len(x.parent_recursive))

def export_lines(b):
    lines = ""
    indent = len(b.parent_recursive) + 1
    str_indent = ""
    for i in range(indent):
        str_indent += "    "
    name = b.name.split("_")[1].lower()
    jhl = bpy.data.armatures[ARMATURE_NAME].bones[b.name].head_local
    pos = str_indent + "    v: " + str(jhl[0]) + " " + str(jhl[1]) + " " + str(jhl[2])
    if len(b.children) > 0:
        gidx = obj.vertex_groups[b.name].index
        bone_verts = [v for v in obj_verts if gidx in [g.group for g in v.groups]]
        bone_weights = [g.weight for g in [gg for v in bone_verts for gg in v.groups] if g.group == gidx]
        i_v = str_indent + "    i: " + ' '.join([str(v.index) for v in bone_verts])
        w_v = str_indent + "    w: " + ' '.join([str(w) for w in bone_weights])
    jme = bpy.data.armatures[ARMATURE_NAME].bones[b.name].matrix_local.to_euler()[1]
    roll = str_indent + "    ipos: " + str(math.degrees(jme)) + " 0.0 0.0 0.0 0.0 0.0 0.0"
    rot = str_indent + "    animdegr: "
    loc = str_indent + "    animoffs: "
    anim_ts = ' '.join([str(i * FRAME_DURATION) for i in range(FRAME_COUNT)])
    for i in range(FRAME_COUNT):
        bpy.context.scene.frame_set(i)
        jrot = b.rotation_quaternion.to_euler()
        rot += str(math.degrees(jrot[0])) + " " + str(math.degrees(jrot[1])) + " " + str(math.degrees(jrot[2])) + " "
        loc += str(b.location[0]) + " " + str(b.location[1]) + " " + str(b.location[2]) + " "
    lines += str_indent + name + "\n"
    lines += str_indent + "    type: 4\n"
    lines += pos + "\n"
    if len(b.children) > 0:
        lines += i_v + "\n"
        lines += w_v + "\n"
        lines += roll + "\n"
        lines += rot[:-1] + "\n"
        lines += str_indent + "    animdegrts: " + anim_ts + "\n"
        if name == 'hips':
            lines += loc[:-1] + "\n"
            lines += str_indent + "    animoffsts: " + anim_ts + "\n"
    for c in b.children:
        lines += export_lines(c)
    lines += str_indent + "/" + name + "\n"
    return lines

new_file = open(FILE_DIRECTORY + FILE_NAME + "_blender.txt", "w+")
lines = export_lines(sorted_bones[0])
new_file.write(lines)
new_file.close()