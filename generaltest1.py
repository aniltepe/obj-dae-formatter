import os

class vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

scriptdir = os.path.dirname(__file__)
file  = open(scriptdir + "/verticestest.txt", "r")
v = file.read().split(" ")
vertices = []
normals = []
for i in range(0, len(v), 3):
    if i % 2 == 0:
        vertices.append(vertex(float(v[i]), float(v[i + 1]), float(v[i + 2])))
    else:
        normals.append(vertex(float(v[i]), float(v[i + 1]), float(v[i + 2])))

# indice = 1056
# print(vertices[indice].x, vertices[indice].y, vertices[indice].z)
# print(normals[indice].x, normals[indice].y, normals[indice].z)

seeking = vertex(-1.429, 89.086, 6.717)
found = -1
for i in range(len(vertices)):
    vert = vertices[i]
    if abs(vert.x - seeking.x) < 0.001 and abs(vert.y - seeking.y) < 0.001 and abs(vert.z - seeking.z) < 0.001:
        found = i
        break

print(found)
print(vertices[found].x, vertices[found].y, vertices[found].z)
