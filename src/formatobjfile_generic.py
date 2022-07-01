import math
from statistics import mean

FILE_NAMES = ["console.obj"]
# FILE_NAMES = ["male.obj"]
FILE_DIRECTORY = "/Users/nazimaniltepe/Downloads/"
# FILE_DIRECTORY = "/Users/nazimaniltepe/Documents/Projects/PythonScripts/obj/" 
MAX_Y_FOR_SCALE = 1.0

class vector:
    def __init__(self, x, y, z):
        self.x = x #float
        self.y = y #float
        self.z = z #float
class vec2:
    def __init__(self, x, y):
        self.x = x #float
        self.y = y #float
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
        self.vn_indexes = [] #int[]
class model:
    def __init__(self):
        self.name = ""
        self.triangles = []
        self.vertices = []
        self.normals = []

def cross(a, b): #a:vector, b:vector
    return vector(a.y * b.z - a.z * b.y,
                  a.z * b.x - a.x * b.z,
                  a.x * b.y - a.y * b.x)
def normalize(a): #a:vector
    length = math.sqrt(pow(a.x, 2) + pow(a.y, 2) + pow(a.z, 2)) 
    return vector(a.x / length, a.y / length, a.z / length) if length > 0.0 else vector(0.0, 0.0, 0.0)
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
        
        if row.startswith("vn "):
            splittedrow = row.split(" ")
            newModel.normals.append(vector(float(splittedrow[1]), float(splittedrow[2]), float(splittedrow[3])))

        if row.startswith("f "):
            splittedrow = row.strip().split(" ")
            splittedrow = splittedrow[1:]
            if len(splittedrow) == 4 and splittedrow[3] != "":
                new_triangle = triangle()
                new_triangle.child_indexes.append(int(splittedrow[0] if "/" not in splittedrow[0] else splittedrow[0].split("/")[0]) - (1 if splittedrow[0][0] != "-" else 0))
                new_triangle.child_indexes.append(int(splittedrow[1] if "/" not in splittedrow[1] else splittedrow[1].split("/")[0]) - (1 if splittedrow[1][0] != "-" else 0))
                new_triangle.child_indexes.append(int(splittedrow[3] if "/" not in splittedrow[3] else splittedrow[3].split("/")[0]) - (1 if splittedrow[3][0] != "-" else 0))
                new_triangle.vn_indexes.append(int(splittedrow[0] if "/" not in splittedrow[0] else splittedrow[0].split("/")[2]) - (1 if splittedrow[0].split("/")[2][0] != "-" else 0))
                new_triangle.vn_indexes.append(int(splittedrow[1] if "/" not in splittedrow[1] else splittedrow[1].split("/")[2]) - (1 if splittedrow[1].split("/")[2][0] != "-" else 0))
                new_triangle.vn_indexes.append(int(splittedrow[3] if "/" not in splittedrow[3] else splittedrow[3].split("/")[2]) - (1 if splittedrow[3].split("/")[2][0] != "-" else 0))
                newModel.triangles.append(new_triangle)
                new_triangle = triangle()
                new_triangle.child_indexes.append(int(splittedrow[1] if "/" not in splittedrow[1] else splittedrow[1].split("/")[0]) - (1 if splittedrow[1][0] != "-" else 0))
                new_triangle.child_indexes.append(int(splittedrow[2] if "/" not in splittedrow[2] else splittedrow[2].split("/")[0]) - (1 if splittedrow[2][0] != "-" else 0))
                new_triangle.child_indexes.append(int(splittedrow[3] if "/" not in splittedrow[3] else splittedrow[3].split("/")[0]) - (1 if splittedrow[3][0] != "-" else 0))
                new_triangle.vn_indexes.append(int(splittedrow[1] if "/" not in splittedrow[1] else splittedrow[1].split("/")[2]) - (1 if splittedrow[1].split("/")[2][0] != "-" else 0))
                new_triangle.vn_indexes.append(int(splittedrow[2] if "/" not in splittedrow[2] else splittedrow[2].split("/")[2]) - (1 if splittedrow[2].split("/")[2][0] != "-" else 0))
                new_triangle.vn_indexes.append(int(splittedrow[3] if "/" not in splittedrow[3] else splittedrow[3].split("/")[2]) - (1 if splittedrow[3].split("/")[2][0] != "-" else 0))
                newModel.triangles.append(new_triangle)
            elif (len(splittedrow) == 4 and splittedrow[3] == "") or len(splittedrow) == 3:
                new_triangle = triangle()
                new_triangle.child_indexes.append(int(splittedrow[0] if "/" not in splittedrow[0] else splittedrow[0].split("/")[0]) - (1 if splittedrow[0][0] != "-" else 0))
                new_triangle.child_indexes.append(int(splittedrow[1] if "/" not in splittedrow[1] else splittedrow[1].split("/")[0]) - (1 if splittedrow[1][0] != "-" else 0))
                new_triangle.child_indexes.append(int(splittedrow[2] if "/" not in splittedrow[2] else splittedrow[2].split("/")[0]) - (1 if splittedrow[2][0] != "-" else 0))
                new_triangle.vn_indexes.append(int(splittedrow[0] if "/" not in splittedrow[0] else splittedrow[0].split("/")[2]) - (1 if splittedrow[0].split("/")[2][0] != "-" else 0))
                new_triangle.vn_indexes.append(int(splittedrow[1] if "/" not in splittedrow[1] else splittedrow[1].split("/")[2]) - (1 if splittedrow[1].split("/")[2][0] != "-" else 0))
                new_triangle.vn_indexes.append(int(splittedrow[2] if "/" not in splittedrow[2] else splittedrow[2].split("/")[2]) - (1 if splittedrow[2].split("/")[2][0] != "-" else 0))
                newModel.triangles.append(new_triangle)
   
   

    # her bir üçgen için; onu oluşturan vertex'lere üçgenin index'ini yazma işlemi
    # ve üçgeni oluşturan noktalardan kenarları bulup üçgenin normal vektörünü bulma işlemi

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
# ultimateMaxY = 0.851135
# ultimateMinY = 0.0


for m in models:
    for tris in m.triangles:
        for vi in range(len(tris.child_indexes)):
            m.vertices[tris.child_indexes[vi]].normal = m.normals[tris.vn_indexes[vi]]

    # for vertice in m.vertices:

        # her bir vertex için; o vertex'in parçası olduğu üçgenlerin normal vektörlerinin ortalamasını alarak smooth'laştırma

        # vertice.normal = vector(0.0, 0.0, 0.0)
        # for parent in vertice.parent_indexes:
        #     vertice.normal = add(vertice.normal, m.triangles[parent].normal)
        # vertice.normal = normalize(vertice.normal)


        # vertice.position.y -= ultimateMinY
        # vertice.position.x /= (ultimateMaxY - ultimateMinY) / MAX_Y_FOR_SCALE
        # vertice.position.y /= (ultimateMaxY - ultimateMinY) / MAX_Y_FOR_SCALE
        # vertice.position.z /= (ultimateMaxY - ultimateMinY) / MAX_Y_FOR_SCALE
        # vertice.position.y += 0.75
        # vertice.position.x += 0.466875
        # vertice.position.z += -0.02
        # vertice.position.x += 0.01

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
# ultimateMaxX = 0.2544434835053954
# ultimateMinX = -0.2544434835053954
# ultimateMaxZ = 0.25064008750454525
# ultimateMinZ = -0.2506400875045452

# for m in models:
#     for vertice in m.vertices:
#         vertice.position.x -= (ultimateMaxX - (ultimateMaxX - ultimateMinX) / 2)
#         vertice.position.z -= (ultimateMaxZ - (ultimateMaxZ - ultimateMinZ) / 2)

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
        new_line += str(v.normal.x) + " " + str(v.normal.y) + " " + str(v.normal.z) + " " if v.normal != None else "0.0 0.0 0.0 "
    new_file.write(new_line[:-1])
    new_file.close()

    # new_file = open(FILE_DIRECTORY + "MOD_VT_" + mdl.name.split(".")[0] + ".txt", "w+")
    # new_line = ""
    # for v in mdl.vertices:
    #     new_line += "0.0 0.0 "
    # new_file.write(new_line[:-1])
    # new_file.close()
    
    new_file = open(FILE_DIRECTORY + "MOD_F_" + mdl.name.split(".")[0] + ".txt", "w+")
    new_line = ""
    for t in mdl.triangles:
        new_line += str(t.child_indexes[0]) + " " + str(t.child_indexes[1]) + " " + str(t.child_indexes[2]) + " "
    new_file.write(new_line[:-1])
    new_file.close()
        
    
# exportObjFromModel(models[0])
exportTxtFromModel(models[0])

# for m in models:
#     exportTxtFromModel(m)


