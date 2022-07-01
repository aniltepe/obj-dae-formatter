import os
import math
from statistics import mean

FILE_NAME = "lefteyebrow.obj"

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
    tri = triangles[i]
    triangle_vertices = []
    for child in tri.child_indexes:
        vertices[child].parent_indexes.append(i)
        triangle_vertices.append(vertices[child])
    for j in range(len(triangle_vertices)):
        curr_vertice = triangle_vertices[j]
        next_vertice = triangle_vertices[(j + 1) % 3]
        tri.edge_vectors.append(vector(curr_vertice.position.x - next_vertice.position.x, curr_vertice.position.y - next_vertice.position.y, curr_vertice.position.z - next_vertice.position.z))

    c = cross(tri.edge_vectors[0], tri.edge_vectors[1])
    tri.normal = normalize(c)

for ver in vertices:
    ver.normal = vector(0.0, 0.0, 0.0)
    for parent in ver.parent_indexes:
        ver.normal = add(ver.normal, triangles[parent].normal)
    ver.normal = normalize(ver.normal)
    # ver.position.x += ver.normal.x * 0.5
    # ver.position.y += ver.normal.y * 0.5
    # ver.position.z += ver.normal.z * 0.5

new_file = open(script_dir + "/obj/lefteyebrownormals.txt", "w+")
lines = []

for ver in vertices:
    new_line = "v " + str(ver.position.x) + " " + str(ver.position.y) + " " + str(ver.position.z) + " " + str(ver.normal.x) + " " + str(ver.normal.y) + " " + str(ver.normal.z) + "\n"
    lines.append(new_line)

for tri in triangles:
    new_line = "f " + str(tri.child_indexes[0]) + " " + str(tri.child_indexes[1]) + " " + str(tri.child_indexes[2]) + "\n"
    lines.append(new_line)


new_file.writelines(lines)
new_file.close()

print("wait")