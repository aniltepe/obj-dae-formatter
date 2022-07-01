import bpy

OBJECT_NAME = "unamed"

values = ""
for v in bpy.data.objects[OBJECT_NAME].data.vertices:
    values += str(v.normal[0]) + " " + str(v.normal[1]) + " " + str(v.normal[2]) + " "
print(values[:-1])