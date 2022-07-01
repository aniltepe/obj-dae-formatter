# get vertices' weights and position by iterate through

import bpy

obj = bpy.data.objects['unamed']
obj_verts = obj.data.vertices

for v in obj_verts:
    word = str(v.co[0]) + " " + str(v.co[1]) + " " + str(v.co[2]) + " vertice no. " + str(v.index)
    total = 0
    word_ = ""
    for g in v.groups:
        total += g.weight
        word_ += str(g.group) + ":" + str(g.weight) + " + "
    word_ = word_[:-3]
    word += " weights total = " + str(total) + " = " + word_
    print(word)