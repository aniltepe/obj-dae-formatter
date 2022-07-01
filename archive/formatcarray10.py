import os
import math
from statistics import mean

FILE_NAME = "male.obj"

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

def cross(a, b): #a:vector, b:vector
    return vector(a.y * b.z - a.z * b.y,
                  a.z * b.x - a.x * b.z,
                  a.x * b.y - a.y * b.x)
def normalize(a): #a:vector
    length = math.sqrt(pow(a.x, 2) + pow(a.y, 2) + pow(a.z, 2)) 
    return vector(a.x / length, a.y / length, a.z / length)
def add(a, b): #a:vector, b:vector
    return vector(a.x + b.x, a.y + b.y, a.z + b.z)


script_dir = os.path.dirname(__file__)
file  = open(script_dir + "/obj/" + FILE_NAME, "r")
rows = file.read().split("\n")
vertices = []
triangles = []

for row in rows:
    if row.startswith("v"):
        splittedrow = row.split(" ")
        newVertex = vertex()
        newVertex.position = vector(float(splittedrow[1]), float(splittedrow[2]), float(splittedrow[3]))
        vertices.append(newVertex)

    if row.startswith("f"):
        splittedrow = row.split(" ")
        splittedrow = splittedrow[1:]
        new_triangle = triangle()
        new_triangle.child_indexes.append(int(splittedrow[0]) - 1)
        new_triangle.child_indexes.append(int(splittedrow[1]) - 1)
        new_triangle.child_indexes.append(int(splittedrow[2]) - 1)
        triangles.append(new_triangle)

for i in range(len(triangles)):
    triangle = triangles[i]
    triangle_vertices = []
    for child in triangle.child_indexes:
        vertices[child].parent_indexes.append(i)
        triangle_vertices.append(vertices[child])
    for j in range(len(triangle_vertices)):
        curr_vertice = triangle_vertices[j]
        next_vertice = triangle_vertices[(j + 1) % 3]
        triangle.edge_vectors.append(vector(curr_vertice.position.x - next_vertice.position.x, curr_vertice.position.y - next_vertice.position.y, curr_vertice.position.z - next_vertice.position.z))

    c = cross(triangle.edge_vectors[0], triangle.edge_vectors[1])
    triangle.normal = normalize(c)

min_y = min([v.position.y for v in vertices])
max_y = max([v.position.y for v in vertices])

for vertice in vertices:
    vertice.normal = vector(0.0, 0.0, 0.0)
    for parent in vertice.parent_indexes:
        vertice.normal = add(vertice.normal, triangles[parent].normal)
    vertice.normal = normalize(vertice.normal)

    vertice.position.y -= min_y
    vertice.position.x /= (max_y - min_y) / 100
    vertice.position.y /= (max_y - min_y) / 100
    vertice.position.z /= (max_y - min_y) / 100


min_x = min([v.position.x for v in vertices])
max_x = max([v.position.x for v in vertices])
min_z = min([v.position.z for v in vertices])
max_z = max([v.position.z for v in vertices])

for vertice in vertices:
    vertice.position.x -= (max_x - (max_x - min_x) / 2)
    vertice.position.z -= (max_z - (max_z - min_z) / 2)


new_file = open(script_dir + "/obj/scenetest_" + FILE_NAME.split(".")[0] + ".txt", "w+")
lines = []

# for triangle in triangles:
#     for child in triangle.child_indexes:
#         new_line = str(vertices[child].position.x) + " " + str(vertices[child].position.y) + " " + str(vertices[child].position.z) + " " + str(vertices[child].normal.x) + " " + str(vertices[child].normal.y) + " " + str(vertices[child].normal.z) + " "
#         new_line.strip()
#         lines.append(new_line)

for v in vertices:
    new_line = str(v.position.x) + " " + str(v.position.y) + " " + str(v.position.z) + " " + str(v.normal.x) + " " + str(v.normal.y) + " " + str(v.normal.z) + " "
    new_line.strip()
    lines.append(new_line)

new_file.writelines(lines)
new_file.close()

print("wait")