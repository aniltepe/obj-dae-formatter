#hatalı çıktı üretiyor



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
vertices = []
triangles = []
ordered_faces = []
ordered_positions = []
ordered_normals = []

for row in rows:
    if row.startswith("v "):
        splittedrow = row.split(" ")
        newVertex = vertex()
        newVertex.position = vector(float(splittedrow[1]), float(splittedrow[2]), float(splittedrow[3]))
        vertices.append(newVertex)

    if row.startswith("f "):
        splittedrow = row.split(" ")
        splittedrow = splittedrow[1:-1]
        new_triangle = triangle()
        new_triangle.child_indexes.append(int(splittedrow[0].split('/')[0]) - 1)
        new_triangle.child_indexes.append(int(splittedrow[1].split('/')[0]) - 1)
        new_triangle.child_indexes.append(int(splittedrow[2].split('/')[0]) - 1)
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

    ordered_faces += triangle.child_indexes

for vertice in vertices:
    vertice.normal = vector(0.0, 0.0, 0.0)
    for parent in vertice.parent_indexes:
        vertice.normal = add(vertice.normal, triangles[parent].normal)
    vertice.normal = normalize(vertice.normal)

    ordered_positions.append(vertice.position.x)
    ordered_positions.append(vertice.position.y)
    ordered_positions.append(vertice.position.z)
    ordered_normals.append(vertice.normal.x)
    ordered_normals.append(vertice.normal.y)
    ordered_normals.append(vertice.normal.z)


#vertice'lerin en büyüğü 'MAX_FLOAT' olacak şekilde scale edilme işlemi
ordered_scale_positions = []
max_float = max(ordered_positions)
for pos in ordered_positions:
    ordered_scale_positions.append(pos * (MAX_FLOAT / max_float))
ordered_positions = ordered_scale_positions

#bütün vertice'lerin arasında minimum y değerinin 0'a eşitlenmesi işlemi
min_y = float('inf')
for i in range(1, len(ordered_positions), 3):
    if (ordered_positions[i] < min_y):
        min_y = ordered_positions[i]
for i in range(1, len(ordered_positions), 3):
    ordered_positions[i] += -1 * min_y


new_file = open(script_dir + "/obj/formatted_" + FILE_NAME.split(".")[0] + ".txt", "w+")
lines = ["float vertices[] = {\r"]

# for triangle in triangles:
#     new_line = "\t" + str(triangle.)   str(orderedfloats[f * 3 + 0]) + ", " + str(orderedfloats[f * 3 + 1]) + ", " + str(orderedfloats[f * 3 + 2]) + ", "
#     for child in triangle.child_indexes:
#         new_line = "\t" + str(vertices[child].position.x) + ", " + str(vertices[child].position.y) + ", " + str(vertices[child].position.z) + ", "
#         new_line += str(vertices[child].normal.x) + ", " + str(vertices[child].normal.y) + ", " + str(vertices[child].normal.z) + ",\r" 
#         lines.append(new_line)
# lines.append("};")

for i in range(len(ordered_faces)):
    f = ordered_faces[i]
    new_line = "\t" + str(ordered_positions[f * 3 + 0]) + ", " + str(ordered_positions[f * 3 + 1]) + ", " + str(ordered_positions[f * 3 + 2]) + ", "
    new_line += str(ordered_normals[f * 3 + 0]) + ", " + str(ordered_normals[f * 3 + 1]) + ", " + str(ordered_normals[f * 3 + 2]) + ",\r"
    lines.append(new_line)
lines.append("};")

new_file.writelines(lines)
new_file.close()

print("wait")