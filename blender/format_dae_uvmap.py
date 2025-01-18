import bpy
import bmesh

print("\n\n\n")
obj=bpy.context.object
if obj.mode != 'EDIT':
    bpy.ops.object.editmode_toggle()
selected_faces = []
if obj.mode == 'EDIT':
    bm=bmesh.from_edit_mesh(obj.data)
    for f in bm.faces:
        if f.select:
            selected_faces.append({"idx":f.index, "v0": f.verts[0].index, "v1": f.verts[1].index, "v2": f.verts[2].index})
            
bpy.ops.object.editmode_toggle()
if obj.mode == 'OBJECT':
    for f in selected_faces:
        print("triangle index:", f["idx"])
        print(f["v0"], obj.data.uv_layers.active.data[f["idx"] * 3].uv)
        print(f["v1"], obj.data.uv_layers.active.data[f["idx"] * 3 + 1].uv)
        print(f["v2"], obj.data.uv_layers.active.data[f["idx"] * 3 + 2].uv)
