# import os
# import math
# from statistics import mean

# FILE_NAME = "sphere.obj"

# class vector:
#     def __init__(self, x, y, z):
#         self.x = x #float
#         self.y = y #float
#         self.z = z #float
# class vertex:
#     def __init__(self):
#         self.position = None #vector
#         self.normal = None #vector
#         self.parent_indexes = [] #int[]
# class triangle:
#     def __init__(self):
#         self.normal = None #vector
#         self.edge_vectors = [] #vector[]
#         self.child_indexes = [] #int[]

# def cross(a, b): #a:vector, b:vector
#     return vector(a.y * b.z - a.z * b.y,
#                   a.z * b.x - a.x * b.z,
#                   a.x * b.y - a.y * b.x)
# def normalize(a): #a:vector
#     length = math.sqrt(pow(a.x, 2) + pow(a.y, 2) + pow(a.z, 2)) 
#     return vector(a.x / length, a.y / length, a.z / length)
# def add(a, b): #a:vector, b:vector
#     return vector(a.x + b.x, a.y + b.y, a.z + b.z)


# script_dir = os.path.dirname(__file__)
# file  = open(script_dir + "/obj/" + FILE_NAME, "r")
# rows = file.read().split("\n")
# vertices = []
# triangles = []

# for row in rows:
#     if row.startswith("v "):
#         splittedrow = row.split(" ")
#         newVertex = vertex()
#         newVertex.position = vector(float(splittedrow[1]), float(splittedrow[2]), float(splittedrow[3]))
#         vertices.append(newVertex)

#     if row.startswith("f"):
#         splittedrow = row.split(" ")
#         splittedrow = splittedrow[1:]
#         if len(splittedrow) == 3:
#             new_triangle = triangle()
#             new_triangle.child_indexes.append(int(splittedrow[0].split("/")[0]) - 1)
#             new_triangle.child_indexes.append(int(splittedrow[1].split("/")[0]) - 1)
#             new_triangle.child_indexes.append(int(splittedrow[2].split("/")[0]) - 1)
#             triangles.append(new_triangle)
#         elif len(splittedrow) == 4:
#             new_triangle = triangle()
#             new_triangle.child_indexes.append(int(splittedrow[0].split("/")[0]) - 1)
#             new_triangle.child_indexes.append(int(splittedrow[1].split("/")[0]) - 1)
#             new_triangle.child_indexes.append(int(splittedrow[3].split("/")[0]) - 1)
#             triangles.append(new_triangle)
#             new_triangle = triangle()
#             new_triangle.child_indexes.append(int(splittedrow[1].split("/")[0]) - 1)
#             new_triangle.child_indexes.append(int(splittedrow[2].split("/")[0]) - 1)
#             new_triangle.child_indexes.append(int(splittedrow[3].split("/")[0]) - 1)
#             triangles.append(new_triangle)

# new_file = open(script_dir + "/obj/nscenetest_" + FILE_NAME.split(".")[0] + ".txt", "w+")
# lines = []

# for triangle in triangles:
#     for child in triangle.child_indexes:
#         new_line = str(vertices[child].position.x) + " " + str(vertices[child].position.y) + " " + str(vertices[child].position.z) + "\n"
#         lines.append(new_line)

# new_file.writelines(lines)
# new_file.close()

# print("wait")




from formatcarray12 import FILE_NAME
import math
from statistics import mean

# FILE_NAMES = ["Realistic_White_Male_Low_Poly.obj", "Eye_Mesh_Low_Poly.obj", "Left_Eye_Mesh_Low_Poly.obj", "Right_Eye_Mesh_Low_Poly.obj", "Teeth_Mesh_Low_Poly.obj", "Lower_Teeth_Mesh_Low_Poly.obj", "Upper_Teeth_Mesh_Low_Poly.obj"]
FILE_NAMES = ["sphere.obj"]
# FILE_DIRECTORY = "/Users/nazimaniltepe/Documents/3D Models/Realistic_White_Male_Low_Poly/"
FILE_DIRECTORY = "/Users/nazimaniltepe/Documents/Projects/PythonScripts/obj/"
MAX_Y_FOR_SCALE = 1.0

class vector:
    def __init__(self, x, y, z):
        self.x = x #float
        self.y = y #float
        self.z = z #float
class vertex:
    def __init__(self):
        self.position = None #vector
        self.normal = None #vector
        self.parent_indexes = [] #int[]
class triangle:
    def __init__(self):
        self.normal = None #vector
        self.edge_vectors = [] #vector[]
        self.child_indexes = [] #int[]
class model:
    def __init__(self):
        self.name = ""
        self.triangles = []
        self.vertices = []

def cross(a, b): #a:vector, b:vector
    return vector(a.y * b.z - a.z * b.y,
                  a.z * b.x - a.x * b.z,
                  a.x * b.y - a.y * b.x)
def normalize(a): #a:vector
    length = math.sqrt(pow(a.x, 2) + pow(a.y, 2) + pow(a.z, 2)) 
    return vector(a.x / length, a.y / length, a.z / length)
def add(a, b): #a:vector, b:vector
    return vector(a.x + b.x, a.y + b.y, a.z + b.z)


models = []
maxXs = []
maxYs = []
maxZs = []
minXs = []
minYs = []
minZs = []
for file in FILE_NAMES:
    newModel = model()
    f = open(FILE_DIRECTORY + file, "r")
    rows = f.read().split("\n")
    for row in rows:
        if row.startswith("v "):
            splittedrow = row.split(" ")
            newVertex = vertex()
            # if double whitespace exists in v and x y z
            if splittedrow[1] == "":
                newVertex.position = vector(float(splittedrow[2]), float(splittedrow[3]), float(splittedrow[4]))
            else:
                newVertex.position = vector(float(splittedrow[1]), float(splittedrow[2]), float(splittedrow[3]))
            newModel.vertices.append(newVertex)

        if row.startswith("f"):
            splittedrow = row.strip().split(" ")
            splittedrow = splittedrow[1:]
            for i in range(len(splittedrow)):
                if "/" in splittedrow[i]:
                    splittedrow[i] = splittedrow[i].split("/")[0]
            if len(splittedrow) == 4:
                if splittedrow[3] != "":
                    new_triangle = triangle()
                    new_triangle.child_indexes.append(int(splittedrow[0]) - 1)
                    new_triangle.child_indexes.append(int(splittedrow[1]) - 1)
                    new_triangle.child_indexes.append(int(splittedrow[3]) - 1)
                    newModel.triangles.append(new_triangle)
                    new_triangle = triangle()
                    new_triangle.child_indexes.append(int(splittedrow[1]) - 1)
                    new_triangle.child_indexes.append(int(splittedrow[2]) - 1)
                    new_triangle.child_indexes.append(int(splittedrow[3]) - 1)
                    newModel.triangles.append(new_triangle)
                else:
                    new_triangle = triangle()
                    new_triangle.child_indexes.append(int(splittedrow[0]) - 1)
                    new_triangle.child_indexes.append(int(splittedrow[1]) - 1)
                    new_triangle.child_indexes.append(int(splittedrow[2]) - 1)
                    newModel.triangles.append(new_triangle)
            elif len(splittedrow) == 3:
                new_triangle = triangle()
                new_triangle.child_indexes.append(int(splittedrow[0]) - 1)
                new_triangle.child_indexes.append(int(splittedrow[1]) - 1)
                new_triangle.child_indexes.append(int(splittedrow[2]) - 1)
                newModel.triangles.append(new_triangle)
    for i in range(len(newModel.triangles)):
        tri = newModel.triangles[i]
        triangle_vertices = []
        for child in tri.child_indexes:
            newModel.vertices[child].parent_indexes.append(i)
            triangle_vertices.append(newModel.vertices[child])
        for j in range(len(triangle_vertices)):
            curr_vertice = triangle_vertices[j]
            next_vertice = triangle_vertices[(j + 1) % 3]
            tri.edge_vectors.append(vector(curr_vertice.position.x - next_vertice.position.x, curr_vertice.position.y - next_vertice.position.y, curr_vertice.position.z - next_vertice.position.z))
        c = cross(tri.edge_vectors[0], tri.edge_vectors[1])
        tri.normal = normalize(c)
    min_x = min([v.position.x for v in newModel.vertices])
    max_x = max([v.position.x for v in newModel.vertices])
    min_y = min([v.position.y for v in newModel.vertices])
    max_y = max([v.position.y for v in newModel.vertices])
    min_z = min([v.position.z for v in newModel.vertices])
    max_z = max([v.position.z for v in newModel.vertices])
    maxYs.append(max_y)
    minYs.append(min_y)
    print("\n" + file + "=> max x: " + str(max_x) + ", min x: " + str(min_x) + 
            ", max y: " + str(max_y) + ", min y: " + str(min_y) + 
            ", max z: " + str(max_z) + ", min z: " + str(min_z))
    newModel.name = file
    models.append(newModel)
    


ultimateMaxY = max(maxYs)
ultimateMinY = min(minYs)
for m in models:
    for vertice in m.vertices:
        vertice.normal = vector(0.0, 0.0, 0.0)
        for parent in vertice.parent_indexes:
            vertice.normal = add(vertice.normal, m.triangles[parent].normal)
        vertice.normal = normalize(vertice.normal)
        vertice.position.y -= ultimateMinY
        vertice.position.x /= (ultimateMaxY - ultimateMinY) / MAX_Y_FOR_SCALE
        vertice.position.y /= (ultimateMaxY - ultimateMinY) / MAX_Y_FOR_SCALE
        vertice.position.z /= (ultimateMaxY - ultimateMinY) / MAX_Y_FOR_SCALE
    min_x = min([v.position.x for v in m.vertices])
    max_x = max([v.position.x for v in m.vertices])
    min_z = min([v.position.z for v in m.vertices])
    max_z = max([v.position.z for v in m.vertices])
    maxXs.append(max_x)
    minXs.append(min_x)
    maxZs.append(max_z)
    minZs.append(min_z)

ultimateMaxX = max(maxXs)
ultimateMinX = min(minXs)
ultimateMaxZ = max(maxZs)
ultimateMinZ = min(minZs)
for m in models:
    for vertice in m.vertices:
        vertice.position.x -= (ultimateMaxX - (ultimateMaxX - ultimateMinX) / 2)
        vertice.position.z -= (ultimateMaxZ - (ultimateMaxZ - ultimateMinZ) / 2)

print("\nAfter Transformation")
for m in models:
    min_x = min([v.position.x for v in m.vertices])
    max_x = max([v.position.x for v in m.vertices])
    min_y = min([v.position.y for v in m.vertices])
    max_y = max([v.position.y for v in m.vertices])
    min_z = min([v.position.z for v in m.vertices])
    max_z = max([v.position.z for v in m.vertices])
    print("\n" + m.name + "=> max x: " + str(max_x) + ", min x: " + str(min_x) + 
            ", max y: " + str(max_y) + ", min y: " + str(min_y) + 
            ", max z: " + str(max_z) + ", min z: " + str(min_z))


def exportObjFromModel(mdl):
    new_file = open(FILE_DIRECTORY + "MOD_" + mdl.name, "w+")
    lines = []
    for v in mdl.vertices:
        new_line = "v " + str(v.position.x) + " " + str(v.position.y) + " " + str(v.position.z) + "\n"
        lines.append(new_line)

    for t in mdl.triangles:
        new_line = "f " + str(t.child_indexes[0] + 1) + " " + str(t.child_indexes[1] + 1) + " " + str(t.child_indexes[2] + 1) + "\n"
        lines.append(new_line)
    new_file.writelines(lines)
    new_file.close()

def exportTxtFromModel(mdl):
    new_file = open(FILE_DIRECTORY + "MOD_V_" + mdl.name.split(".")[0] + ".txt", "w+")
    new_line = ""
    for v in mdl.vertices:
        new_line += str(v.position.x) + " " + str(v.position.y) + " " + str(v.position.z) + " "
    new_file.write(new_line[:-1])
    new_file.close()
    
    new_file = open(FILE_DIRECTORY + "MOD_VN_" + mdl.name.split(".")[0] + ".txt", "w+")
    new_line = ""
    for v in mdl.vertices:
        new_line += str(v.normal.x) + " " + str(v.normal.y) + " " + str(v.normal.z) + " "
    new_file.write(new_line[:-1])
    new_file.close()
    
    new_file = open(FILE_DIRECTORY + "MOD_F_" + mdl.name.split(".")[0] + ".txt", "w+")
    new_line = ""
    for t in mdl.triangles:
        new_line += str(t.child_indexes[0]) + " " + str(t.child_indexes[1]) + " " + str(t.child_indexes[2]) + " "
    new_file.write(new_line[:-1])
    new_file.close()
        
    
# exportObjFromModel(models[0])
exportTxtFromModel(models[0])


