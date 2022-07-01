import os
import math

MAX_FLOAT = 1.0
FILE_NAME = "skeleton.obj"

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
class group:
    def __init__(self):
        self.vertices = [] #vertex[] 
        self.triangles = [] #triangle[]

def cross(a, b): #a:vector, b:vector
    return vector(a.y * b.z - a.z * b.y,
                  a.z * b.x - a.x * b.z,
                  a.x * b.y - a.y * b.x)
    
def normalize(a): #a:vector
    length = math.sqrt(pow(a.x, 2) + pow(a.y, 2) + pow(a.z, 2)) 
    if length == 0.0:
        return vector(0.0, 0.0, 0.0)
    return vector(a.x / length, a.y / length, a.z / length)

def add(a, b): #a:vector, b:vector
    return vector(a.x + b.x, a.y + b.y, a.z + b.z)


script_dir = os.path.dirname(__file__)
file  = open(script_dir + "/obj/" + FILE_NAME, "r")
rows = file.read().split("\n")

groups = []
for i in range(len(rows)):
    if rows[i].startswith("g "):
        new_group = group()
        groups.append(new_group)
    if rows[i].startswith("v "):
        splitted_row = rows[i].split(" ")
        new_vertex = vertex()
        new_vertex.position = vector(float(splitted_row[1]), float(splitted_row[2]), float(splitted_row[3]))
        groups[-1].vertices.append(new_vertex)
    if rows[i].startswith("f "):
        splitted_row = rows[i].split(" ")
        splitted_row = splitted_row[1:-1]
        new_triangle = triangle()
        new_triangle.child_indexes.append(int(splitted_row[0].split('/')[0]) if int(splitted_row[0].split('/')[0]) < 0 else int(splitted_row[0].split('/')[0]) - 1)
        new_triangle.child_indexes.append(int(splitted_row[1].split('/')[0]) if int(splitted_row[1].split('/')[0]) < 0 else int(splitted_row[1].split('/')[0]) - 1)
        new_triangle.child_indexes.append(int(splitted_row[2].split('/')[0]) if int(splitted_row[2].split('/')[0]) < 0 else int(splitted_row[2].split('/')[0]) - 1)
        groups[-1].triangles.append(new_triangle)

for group in groups:
    for i in range(len(group.triangles)):
        triangle_vertices = []
        for child in group.triangles[i].child_indexes:
            group.vertices[child].parent_indexes.append(i)
            triangle_vertices.append(group.vertices[child])
        for j in range(len(triangle_vertices)):
            curr_vertice = triangle_vertices[j]
            next_vertice = triangle_vertices[(j + 1) % 3]
            group.triangles[i].edge_vectors.append(vector(curr_vertice.position.x - next_vertice.position.x, curr_vertice.position.y - next_vertice.position.y, curr_vertice.position.z - next_vertice.position.z))

        c = cross(group.triangles[i].edge_vectors[0], group.triangles[i].edge_vectors[1])
        group.triangles[i].normal = normalize(c)
    
    for vertice in group.vertices:
        vertice.normal = vector(0.0, 0.0, 0.0)
        for parent in vertice.parent_indexes:
            vertice.normal = add(vertice.normal, group.triangles[parent].normal)
        vertice.normal = normalize(vertice.normal)


new_file = open(script_dir + "/obj/formatted_" + FILE_NAME.split(".")[0] + ".txt", "w+")
lines = ["float vertices[] = {\r"]

for group in groups:
    for triangle in group.triangles:
        for child in triangle.child_indexes:
            new_line = "\t" + str(group.vertices[child].position.x) + ", " + str(group.vertices[child].position.y) + ", " + str(group.vertices[child].position.z) + ", "
            new_line += str(group.vertices[child].normal.x) + ", " + str(group.vertices[child].normal.y) + ", " + str(group.vertices[child].normal.z) + ",\r" 
            lines.append(new_line)

lines.append("};")
new_file.writelines(lines)
new_file.close()

print("wait")