import math

FILE_NAME = "scene19.sce"
FILE_DIRECTORY = "/Users/nazimaniltepe/Documents/Projects/opengl-scene/src/"
OBJECT_NAME = "human"

class vector:
    def __init__(self, x, y, z):
        self.x = x #float
        self.y = y #float
        self.z = z #float

def cross(a, b): #a:vector, b:vector
    return vector(a.y * b.z - a.z * b.y,
                  a.z * b.x - a.x * b.z,
                  a.x * b.y - a.y * b.x)
def normalize(a): #a:vector
    length = math.sqrt(pow(a.x, 2) + pow(a.y, 2) + pow(a.z, 2)) 
    return vector(a.x / length, a.y / length, a.z / length)
def add(a, b): #a:vector, b:vector
    return vector(a.x + b.x, a.y + b.y, a.z + b.z)


f = open(FILE_DIRECTORY + FILE_NAME, "r")
rows = f.read().split("\n")

start_idx = [i for i in range(len(rows)) if rows[i].strip() == OBJECT_NAME][0]
v_idx = start_idx
n_idx = start_idx
f_idx = start_idx
while not rows[v_idx].strip().startswith("v: "):
    v_idx += 1
while not rows[n_idx].strip().startswith("n: "):
    n_idx += 1
while not rows[f_idx].strip().startswith("f: "):
    f_idx += 1

vertices = [float(v) for v in rows[v_idx].strip().split(":")[1].strip().split(" ")]
faces = [int(f) for f in rows[f_idx].strip().split(":")[1].strip().split(" ")]
normals = []
new_vertices = []
new_normals = []

total = 0

for i_idx in range(0, len(vertices), 3):
    i = int(i_idx / 3)
    included_tri_idx = [int(t / 3) for t in range(0, len(faces), 3) if faces[t] == i or faces[t + 1] == i or faces[t + 2] == i]
    total += len(included_tri_idx)
    included_tri_nor_sum = vector(0.0, 0.0, 0.0)
    print("Vertex No. ", i, " is part of ", len(included_tri_idx), " triangles, total count: ", total)
    for j in range(len(included_tri_idx)):
        triidx = included_tri_idx[j] * 3
        if j != 0:
            new_vertices.append(vertices[i * 3])
            new_vertices.append(vertices[i * 3 + 1])
            new_vertices.append(vertices[i * 3 + 2])
            new_indice = int(len(vertices) / 3) + int(len(new_vertices) / 3) - 1
            if faces[triidx] == i:
                faces[triidx] = new_indice
            elif faces[triidx + 1] == i:
                faces[triidx + 1] = new_indice
            elif faces[triidx + 2] == i:
                faces[triidx + 2] = new_indice
            
            # sce'deki bütün indice property'leri listelenir
            indice_idxs = [r for r in range(len(rows)) if rows[r].strip().startswith("i: ")]

            # ilgili objenin altıdaki alt objenin joint'leri listeden çıkartılır
            for h in range(len(indice_idxs) - 1, -1, -1):
                temp_idx = indice_idxs[h]
                while not rows[temp_idx].strip().startswith("type: 1"):
                    temp_idx -= 1
                while ":" in rows[temp_idx]:
                    temp_idx -= 1
                if OBJECT_NAME != rows[temp_idx].strip():
                    indice_idxs.remove(indice_idxs[h])

            # ilgili vertice'e etkileyen indice property'leri filtrelenir
            included_indice_idx = [r for r in indice_idxs if str(i) in rows[r].split(":")[1].strip().split(" ")]
            for h in range(len(included_indice_idx)):
                r_idx = included_indice_idx[h]
                name_idx = r_idx
                while ":" in rows[name_idx]:
                    name_idx -= 1
                w_idx = name_idx
                while not rows[w_idx].strip().startswith("w: "):
                    w_idx += 1
                indice_row_index = [int(r) for r in rows[r_idx].split(":")[1].strip().split(" ")].index(i)
                new_weight = [float(w) for w in rows[w_idx].split(":")[1].strip().split(" ")][indice_row_index]
                rows[r_idx] = rows[r_idx].rstrip() + " " + str(new_indice)
                rows[w_idx] = rows[w_idx].rstrip() + " " + str(new_weight)

        v1_x = vertices[faces[triidx] * 3] if faces[triidx] * 3 < len(vertices) else new_vertices[faces[triidx] * 3 - len(vertices)]
        v1_y = vertices[faces[triidx] * 3 + 1] if faces[triidx] * 3 < len(vertices) else new_vertices[faces[triidx] * 3 - len(vertices) + 1]
        v1_z = vertices[faces[triidx] * 3 + 2] if faces[triidx] * 3 < len(vertices) else new_vertices[faces[triidx] * 3 - len(vertices) + 2]
        v2_x = vertices[faces[triidx + 1] * 3] if faces[triidx + 1] * 3 < len(vertices) else new_vertices[faces[triidx + 1] * 3 - len(vertices)]
        v2_y = vertices[faces[triidx + 1] * 3 + 1] if faces[triidx + 1] * 3 < len(vertices) else new_vertices[faces[triidx + 1] * 3 - len(vertices) + 1]
        v2_z = vertices[faces[triidx + 1] * 3 + 2] if faces[triidx + 1] * 3 < len(vertices) else new_vertices[faces[triidx + 1] * 3 - len(vertices) + 2]
        v3_x = vertices[faces[triidx + 2] * 3] if faces[triidx + 2] * 3 < len(vertices) else new_vertices[faces[triidx + 2] * 3 - len(vertices)]
        v3_y = vertices[faces[triidx + 2] * 3 + 1] if faces[triidx + 2] * 3 < len(vertices) else new_vertices[faces[triidx + 2] * 3 - len(vertices) + 1]
        v3_z = vertices[faces[triidx + 2] * 3 + 2] if faces[triidx + 2] * 3 < len(vertices) else new_vertices[faces[triidx + 2] * 3 - len(vertices) + 2]
        edge1 = vector(v1_x - v2_x, v1_y - v2_y, v1_z - v2_z)
        edge2 = vector(v2_x - v3_x, v2_y - v3_y, v2_z - v3_z)
        c = cross(edge1, edge2)
        included_tri_nor_sum = add(included_tri_nor_sum, normalize(c))
    
    ver_nor = normalize(included_tri_nor_sum)
    for j in range(len(included_tri_idx)):
        if j == 0:
            normals.append(ver_nor.x)
            normals.append(ver_nor.y)
            normals.append(ver_nor.z)
        else: 
            new_normals.append(ver_nor.x)
            new_normals.append(ver_nor.y)
            new_normals.append(ver_nor.z)

rows[v_idx] = rows[v_idx].rstrip() + " " + " ".join([str(v) for v in new_vertices])
rows[n_idx] = rows[n_idx].split(":")[0] + ": " + " ".join([str(n) for n in normals]) + " " + " ".join([str(n) for n in new_normals])
rows[f_idx] = rows[f_idx].split(":")[0] + ": " + " ".join([str(f) for f in faces])

new_file = open(FILE_DIRECTORY + FILE_NAME.split(".")[0] + "_separate.sce", "w+")
new_file.writelines("\n".join(rows) + "\n")
new_file.close()
