# blender'a .dae import edildikten sonra çalıştırılmalıdır, aksi halde triangle vertex index'leri yanlış görünecektir (blender vertex'leri reindex'liyor)
# .obj import edildikten sonra çalıştırıldığında triangle vertex index'ler farklı çıkıyor ama hem .dae hem .obj için triangle index'in kendisinde bir sorun yok

import bpy
import bmesh

obj=bpy.context.object
if obj.mode == 'EDIT':
    bm=bmesh.from_edit_mesh(obj.data)
    for v in bm.verts:
        if v.select:
            print(v.index, v.co)
            # print(v.index, v.normal)
    for v in bm.faces:
        if v.select:
            print(v.index, v.verts[0].index, v.verts[1].index, v.verts[2].index)
