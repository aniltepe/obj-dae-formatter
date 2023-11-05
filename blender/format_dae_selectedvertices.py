import bpy
import bmesh

obj=bpy.context.object
if obj.mode == 'EDIT':
    bm=bmesh.from_edit_mesh(obj.data)
    for v in bm.verts:
        if v.select:
            print(v.index, v.co)
    for v in bm.faces:
        if v.select:
            print(v.index, v.verts[0].index, v.verts[1].index, v.verts[2].index)
