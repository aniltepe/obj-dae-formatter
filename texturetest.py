import math
from statistics import mean

FILE_NAMES = ["MOD_V_Right_Eye_Mesh_Low_Poly.txt", "MOD_VN_Right_Eye_Mesh_Low_Poly.txt", "MOD_F_Right_Eye_Mesh_Low_Poly.txt"]
FILE_DIRECTORY = "/Users/nazimaniltepe/Documents/3D Models/Realistic_White_Male_Low_Poly/"

class vector:
    def __init__(self, x, y, z):
        self.x = x #float
        self.y = y #float
        self.z = z #float
class vertex:
    def __init__(self):
        self.position = None #vector
        self.normal = None #vector
        self.texCoord = [] #float[]
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


new_model = model()

for file in FILE_NAMES:
    f = open(FILE_DIRECTORY + file, "r")
    floats = f.read().split(" ")
    if file.split("_")[1] == "V":
        print(str(len(floats) / 3) + " vertices")
        for i in range(0, len(floats), 3):
            new_vertex = vertex()
            new_vertex.position = vector(float(floats[i]), float(floats[i + 1]), float(floats[i + 2]))
            new_model.vertices.append(new_vertex)

    if file.split("_")[1] == "VN":
        print(str(len(floats) / 3) + " normals")
        for i in range(0, len(floats), 3):
            indice = int(i / 3)
            new_model.vertices[indice].normal = vector(float(floats[i]), float(floats[i + 1]), float(floats[i + 2]))
    
    if file.split("_")[1] == "F":
        print(str(len(floats) / 3) + " triangles")
        for i in range(0, len(floats), 3):
            new_triangle = triangle()
            new_triangle.child_indexes.append(int(floats[i]))
            new_triangle.child_indexes.append(int(floats[i + 1]))
            new_triangle.child_indexes.append(int(floats[i + 2]))
            new_model.triangles.append(new_triangle)
    

centerIndice = -1
testV = "-0.033873 1.68546 0.110758"
for i in range(len(new_model.vertices)):
    v = new_model.vertices[i]
    if abs(v.position.x - float(testV.split(" ")[0])) < 0.00001 and abs(v.position.y - float(testV.split(" ")[1])) < 0.00001 and abs(v.position.z - float(testV.split(" ")[2])) < 0.00001:
        centerIndice = i

print("vertice #" + str(centerIndice) + ":", new_model.vertices[centerIndice].position.x, new_model.vertices[centerIndice].position.y, new_model.vertices[centerIndice].position.z)

closeToCenter = []
limitDistance = 0.0065
for i in range(len(new_model.vertices)):
    if i == centerIndice:
        continue
    v = new_model.vertices[i]
    sum = 0.0
    sum += (new_model.vertices[centerIndice].position.x - v.position.x) ** 2
    sum += (new_model.vertices[centerIndice].position.y - v.position.y) ** 2
    sum += (new_model.vertices[centerIndice].position.z - v.position.z) ** 2
    distance = math.sqrt(sum)
    if distance < limitDistance:
        closeToCenter.append(i)

print("number of vertices located limited distance to center:", len(closeToCenter))

min_x = min([new_model.vertices[i].position.x for i in closeToCenter])
max_x = max([new_model.vertices[i].position.x for i in closeToCenter])
min_y = min([new_model.vertices[i].position.y for i in closeToCenter])
max_y = max([new_model.vertices[i].position.y for i in closeToCenter])
# print("\n max x: " + str(max_x) + ", min x: " + str(min_x) + ", max y: " + str(max_y) + ", min y: " + str(min_y))
closeToCenter.append(centerIndice)
for i in closeToCenter:
    v = new_model.vertices[i]
    texCoordX = (v.position.x - min_x) / (max_x - min_x)
    texCoordY = (v.position.y - min_y) / (max_y - min_y)
    new_model.vertices[i].texCoord.append(texCoordX)
    new_model.vertices[i].texCoord.append(texCoordY)

duplicatedIndices = []
addedVertices = []
for triangleIndex in range(len(new_model.triangles)):
    tr = new_model.triangles[triangleIndex]
    texturedTriangle = True
    outOfTexTriangle = True
    for i in tr.child_indexes:
        if i in closeToCenter:
            outOfTexTriangle = False
        else:
            texturedTriangle = False
    
    if outOfTexTriangle:
        for i in tr.child_indexes:
            new_model.vertices[i].texCoord.append(0.0)
            new_model.vertices[i].texCoord.append(0.0)
    
    elif not outOfTexTriangle and not texturedTriangle:
        for j in range(len(tr.child_indexes)):
            i = tr.child_indexes[j]
            if i in closeToCenter:
                if i not in duplicatedIndices:
                    add_vertex = vertex()
                    add_vertex.position = new_model.vertices[i].position
                    add_vertex.normal = new_model.vertices[i].normal
                    add_vertex.texCoord.append(0.0)
                    add_vertex.texCoord.append(0.0)
                    addedVertices.append(add_vertex)
                    duplicatedIndices.append(i)
                    tr.child_indexes[j] = len(new_model.vertices) + len(duplicatedIndices) - 1
                else:
                    addedVerticeIndex = duplicatedIndices.index(i)
                    tr.child_indexes[j] = len(new_model.vertices) + addedVerticeIndex

                
    
new_model.vertices.extend(addedVertices)
print("wait")



def exportObjFromModel(mdl):
    new_file = open(FILE_DIRECTORY + "MODTEXTURE_" + mdl.name, "w+")
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
    new_file = open(FILE_DIRECTORY + "MODTEX_V_" + mdl.name.split(".")[0] + ".txt", "w+")
    new_line = ""
    for v in mdl.vertices:
        new_line += str(v.position.x) + " " + str(v.position.y) + " " + str(v.position.z) + " "
    new_file.write(new_line[:-1])
    new_file.close()
    
    new_file = open(FILE_DIRECTORY + "MODTEX_VN_" + mdl.name.split(".")[0] + ".txt", "w+")
    new_line = ""
    for v in mdl.vertices:
        new_line += str(v.normal.x) + " " + str(v.normal.y) + " " + str(v.normal.z) + " "
    new_file.write(new_line[:-1])
    new_file.close()

    new_file = open(FILE_DIRECTORY + "MODTEX_VT_" + mdl.name.split(".")[0] + ".txt", "w+")
    new_line = ""
    for v in mdl.vertices:
        new_line += str(v.texCoord[0]) + " " + str(v.texCoord[1]) + " "
    new_file.write(new_line[:-1])
    new_file.close()
    
    new_file = open(FILE_DIRECTORY + "MODTEX_F_" + mdl.name.split(".")[0] + ".txt", "w+")
    new_line = ""
    for t in mdl.triangles:
        new_line += str(t.child_indexes[0]) + " " + str(t.child_indexes[1]) + " " + str(t.child_indexes[2]) + " "
    new_file.write(new_line[:-1])
    new_file.close()
        
    
# exportObjFromModel(new_model)
exportTxtFromModel(new_model)


