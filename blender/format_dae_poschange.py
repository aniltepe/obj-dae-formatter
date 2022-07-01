#get specific vertex's position before and after change

import bpy

obj = bpy.data.objects['unamed']
dg = bpy.context.evaluated_depsgraph_get()
obj_dg = obj.evaluated_get(dg)
mesh = obj_dg.to_mesh(preserve_all_data_layers=True, depsgraph=dg)

for i in [8]:
   print("old value: ", obj.data.vertices[i].co)
   print("new value: ", mesh.vertices[i].co)
