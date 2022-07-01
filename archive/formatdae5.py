from contextlib import suppress
import xml.etree.ElementTree as ET
import numpy as np
import math

np.set_printoptions(suppress=True)
FILE_DIRECTORY = "/Users/nazimaniltepe/Documents/3D Models/Realistic_White_Male_Low_Poly/valid20220420/"
FILE_NAME = "Praying.dae"

def parse_arrays(element):
    if element.tag == "float_array" and element.attributes.get("id") == "unamed-lib-Position-array":
        pos_strs = element.text.strip().split(" ")
        pos_floats = [float(s) for s in pos_strs]
        for i in range(0, len(pos_floats), 3):
            new_vertex = vertex(len(vertices), pos_floats[i], pos_floats[i + 1], pos_floats[i + 2])
            vertices.append(new_vertex)
    
    if element.tag == "Name_array" and element.attributes.get("id") == "unamedController-Joints-array":
        joint_strs = element.text.strip().split(" ")
        joint_simplified = [s.split("_")[-1] for s in joint_strs]
        for j in joint_simplified:
            new_joint = joint(j)
            joints.append(new_joint)
    
    if element.tag == "float_array" and element.attributes.get("id") == "unamedController-Weights-array":
        weight_strs = element.text.strip().split(" ")
        weight_floats = [float(s) for s in weight_strs]
        for w in weight_floats:
            weights.append(w)
    
    if element.tag == "float_array" and element.attributes.get("id") == "unamedController-Matrices-array":
        invbind_strs = element.text.strip().split(" ")
        invbind_floats = [float(s) for s in invbind_strs]
        for b in invbind_floats:
            invbinds.append(b)


    if element.tag == "vcount" and element.parent.tag == "vertex_weights":
        vcount_strs = element.text.strip().split(" ")
        vcount_ints = [int(s) for s in vcount_strs]
        for i in range(len(vcount_ints)):
            vertices[i].dual_count = vcount_ints[i]

    if element.tag == "v" and element.parent.tag == "vertex_weights":
        v_strs = element.text.strip().split(" ")
        v_ints = [int(s) for s in v_strs]
        cursor = 0
        for vertice in vertices:
            vertex_related = v_ints[cursor : cursor + vertice.dual_count * 2]
            for i in range(0, len(vertex_related), 2):
                vertice.joints.append(vertex_related[i])
                vertice.weights.append(vertex_related[i + 1])
            cursor = cursor + vertice.dual_count * 2

    for child in element.children:
        parse_arrays(child)

def parse_elements(node, level, parent):
    el = element_()
    el.level = level
    el.tag = node.tag[node.tag.index("}") + 1:]
    el.text = "" if node.text == None else node.text.strip().replace("\n", " ")
    el.attributes = node.attrib
    if level == 0:
        parent.append(el)
    else:
        el.parent = parent
        parent.children.append(el)
    for child in node:
        parse_elements(child, level + 1, el)

def adjust_hierarchy(j):
    jo_name = j.attributes["name"].split("_")[1]
    jos = [jj for jj in joints if jj.name == jo_name]
    if len(jos) == 1:
        jo = jos[0]
    else:
        jo = joint(jo_name)
        joints.append(jo)
    for n in [c for c in j.children if c.tag == "node"]:
        subjo = adjust_hierarchy(n)
        subjo.parent = jo
        jo.children.append(subjo)
    jo.intend = j.level - INTEND_FACTOR
    jo.nodematrix_np = np.array([float(f) for f in [c for c in j.children if c.tag == "matrix"][0].text.strip().split(" ")]).reshape((4,4))
    return jo

def export_txt_file(j):
    if len(j.pos) == 0:
        return ""

    lines = ""
    new_line = ""
    for i in range(j.intend):
        new_line += "    "
    new_line += j.name + "\n"
    lines += new_line

    new_line = ""
    for i in range(j.intend + 1):
        new_line += "    "
    new_line += "type: 4\n"
    lines += new_line

    new_line = ""
    for i in range(j.intend + 1):
        new_line += "    "
    new_line += "v: " + str(j.pos[0]) + " " + str(j.pos[1]) + " " + str(j.pos[2]) + "\n"
    lines += new_line

    new_line = ""
    for i in range(j.intend + 1):
        new_line += "    "
    new_line += "i: "
    for v in j.vertices:
        new_line += str(v.index) + " "
    new_line = new_line[:-1]
    new_line += "\n"
    lines += new_line

    new_line = ""
    for i in range(j.intend + 1):
        new_line += "    "
    new_line += "w: "
    for w in j.weights:
        new_line += str(w) + " "
    new_line = new_line[:-1]
    new_line += "\n"
    lines += new_line

    for c in j.children:
        lines += export_txt_file(c)

    new_line = ""
    for i in range(j.intend):
        new_line += "    "
    new_line += "/" + j.name + "\n"
    lines += new_line

    return lines

def rotation_matrix_to_euler_angles(R):
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
    singular = sy < 1e-6
    if not singular:
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else:
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
    return [math.degrees(x), math.degrees(y), math.degrees(z)]

def euler_angles_to_quaternion(e):
    e0r = math.radians(e[0])
    e1r = math.radians(e[1])
    e2r = math.radians(e[2])
    cy = math.cos(e2r * 0.5)
    sy = math.sin(e2r * 0.5)
    cp = math.cos(e1r * 0.5)
    sp = math.sin(e1r * 0.5)
    cr = math.cos(e0r * 0.5)
    sr = math.sin(e0r * 0.5)

    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy

    return [w, x, y, z]

def export_invbind(j):
    if len(j.invbindmat) == 0:
        return ""

    intend = ""   
    for i in range(j.intend - 1):
        intend += "    "

    lines = ""
    new_line = intend
    new_line += j.name + "\n"
    lines += new_line

    new_line = ""
    new_line += intend + str(j.invbind_np[0][0]) + " " + str(j.invbind_np[0][1]) + " " + str(j.invbind_np[0][2]) + " " + str(j.invbind_np[0][3]) + "\n"
    new_line += intend + str(j.invbind_np[1][0]) + " " + str(j.invbind_np[1][1]) + " " + str(j.invbind_np[1][2]) + " " + str(j.invbind_np[1][3]) + "\n"
    new_line += intend + str(j.invbind_np[2][0]) + " " + str(j.invbind_np[2][1]) + " " + str(j.invbind_np[2][2]) + " " + str(j.invbind_np[2][3]) + "\n"
    new_line += intend + str(j.invbind_np[3][0]) + " " + str(j.invbind_np[3][1]) + " " + str(j.invbind_np[3][2]) + " " + str(j.invbind_np[3][3]) + "\n"
    lines += new_line + "\n"

    for c in j.children:
        lines += export_invbind(c)

    return lines

def export_armature(j):
    if len(j.invbindmat) == 0:
        return ""

    intend = ""   
    for i in range(j.intend - 1):
        intend += "    "

    lines = ""
    new_line = intend
    new_line += j.name + "\n"
    lines += new_line

    new_line = ""
    new_line += intend + "pos: " + str(j.bind_pos[0]) + " " + str(j.bind_pos[1]) + " " +str(j.bind_pos[2]) + "\n"
    new_line += intend + "roll: " + str(j.bind_eul[1]) + "\n"
    lines += new_line + "\n"

    for c in j.children:
        lines += export_armature(c)

    new_line = intend
    new_line += "/" + j.name + "\n"
    lines += new_line

    return lines



class element_:
    def __init__(self):
        self.tag = ""
        self.text = ""
        self.attributes = {}
        self.children = []
        self.parent = None
        self.level = None

class vertex:
    def __init__(self, index, x, y, z):
        self.index = index
        self.x = x
        self.y = y
        self.z = z
        self.dual_count = 0
        self.joints = []
        self.weights = []

class test_class:
    def __init__(self, desc, mat):
        self.desc = desc
        self.npmat = mat
        self.pos = [self.npmat[0][3], self.npmat[1][3], self.npmat[2][3]]
        self.eul = rotation_matrix_to_euler_angles(self.npmat[0:3, 0:3])
        self.qua = euler_angles_to_quaternion(self.eul)

class joint:
    def __init__(self, name):
        self.name = name
        self.vertices = []
        self.weights = []
        self.invbindmat = []
        self.anims = []
        self.children = []
        self.parent = None
        self.intend = None
        self.invbind_np = None
        self.bind_np = None
        self.anims_np = []
        self.bind_pos = []
        self.bind_eul = []
        self.nodematrix_np = None
        self.test_classes = []




tree = ET.parse(FILE_DIRECTORY + FILE_NAME)
root = tree.getroot()

vertices = []
joints = []
weights = []
invbinds = []

elements = []
parse_elements(root, 0, elements)

parse_arrays(elements[0])

for vertice in vertices:
    for i in range(vertice.dual_count):
        joints[vertice.joints[i]].vertices.append(vertice)
        joints[vertice.joints[i]].weights.append(weights[vertice.weights[i]])

for i in range(0, len(invbinds), 16):
    idx = int(i / 16)
    joints[idx].invbindmat = invbinds[i:i+16]

lib_anims = [c for c in elements[0].children if c.tag == "library_animations"][0]
for anim in lib_anims.children:
    transf_sources = [c for c in anim.children if c.tag == "source"]
    transf_source = [s for s in transf_sources if s.attributes["id"].endswith("transform")][0]
    transf_array = [c for c in transf_source.children if c.tag == "float_array"][0]
    jo_name = transf_source.attributes["id"].split("_")[1].split("-")[0]
    jo = [j for j in joints if j.name == jo_name][0]
    jo.anims = [float(f) for f in transf_array.text.strip().split(" ")]

lib_vscene = [c for c in elements[0].children if c.tag == "library_visual_scenes"][0]
root_joint = [c for c in lib_vscene.children[0].children if len([cc for cc in c.children if cc.tag == "matrix"]) > 0][0]

INTEND_FACTOR = 2
r_joint = adjust_hierarchy(root_joint)

for j in joints:
    if len(j.invbindmat) == 16:
        j.invbind_np = np.array(j.invbindmat).reshape((4, 4))
        j.bind_np = np.linalg.inv(j.invbind_np)
        j.bind_pos = [j.bind_np[0][3], j.bind_np[1][3], j.bind_np[2][3]]
        j.anims_np = [np.array(j.anims[a:a+16]).reshape((4, 4)) for a in range(0, len(j.anims), 16)]
        j.bind_eul = rotation_matrix_to_euler_angles(j.bind_np[0:3,0:3])

def adjust_cummulative_values(j):
    if len(j.invbindmat) == 0:
        return
    if j.parent == None:
        j.test_classes.append(test_class("cummulative animation", np.matmul(j.invbind_np, j.nodematrix_np)))
    else:
        j.test_classes.append(test_class("cummulative animation", np.matmul(j.parent.test_classes[0].npmat, j.nodematrix_np)))
    for sj in j.children:
        adjust_cummulative_values(sj)

adjust_cummulative_values(r_joint)

for j in joints:
    if len(j.invbindmat) == 0:
        continue
    if j.parent == None:
        j.test_classes.append(test_class("j.parent.bind * j.anim", np.matmul(j.invbind_np, j.nodematrix_np)))
        j.test_classes.append(test_class("j.parent.bind * j.anim * j.invbind", np.matmul(j.invbind_np, j.nodematrix_np)))
        j.test_classes.append(test_class("j.invbind * j.parent.bind * j.anim", np.matmul(j.invbind_np, j.nodematrix_np)))
    else:
        j.test_classes.append(test_class("j.parent.bind * j.anim", np.matmul(j.parent.bind_np, j.nodematrix_np)))
        j.test_classes.append(test_class("j.parent.bind * j.anim * j.invbind", np.matmul(np.matmul(j.parent.bind_np, j.nodematrix_np), j.invbind_np)))
        j.test_classes.append(test_class("j.invbind * j.parent.bind * j.anim", np.matmul(j.invbind_np, np.matmul(j.parent.bind_np, j.nodematrix_np))))
        
            
    

# new_file = open(FILE_DIRECTORY + "invbind_" + FILE_NAME.split(".")[0] + ".txt", "w+")
# new_file.write(export_invbind(r_joint))
# new_file.close()

# new_file = open(FILE_DIRECTORY + "armature_" + FILE_NAME.split(".")[0] + ".txt", "w+")
# new_file.write(export_armature(r_joint))
# new_file.close()

def export_test():
    lines = ""
    for j in joints:
        if len(j.invbindmat) == 0:
            continue
        new_bind = [1.0, 0.0, 0.0, j.bind_pos[0], 0.0, 1.0, 0.0, j.bind_pos[1], 0.0, 0.0, 1.0, j.bind_pos[2], 0.0, 0.0, 0.0, 1.0]
        new_invbind = np.linalg.inv(np.array(new_bind).reshape((4,4)))
        lines += str(new_invbind[0][0]) + " " + str(new_invbind[0][1]) + " " + str(new_invbind[0][2]) + " " + str(new_invbind[0][3]) + " "
        lines += str(new_invbind[1][0]) + " " + str(new_invbind[1][1]) + " " + str(new_invbind[1][2]) + " " + str(new_invbind[1][3]) + " "
        lines += str(new_invbind[2][0]) + " " + str(new_invbind[2][1]) + " " + str(new_invbind[2][2]) + " " + str(new_invbind[2][3]) + " "
        lines += str(new_invbind[3][0]) + " " + str(new_invbind[3][1]) + " " + str(new_invbind[3][2]) + " " + str(new_invbind[3][3]) + "\n"
    return lines

new_file = open(FILE_DIRECTORY + "collada_" + FILE_NAME.split(".")[0] + ".txt", "w+")
new_file.write(export_test())
new_file.close()

# new_file = open(FILE_DIRECTORY + "sce_" + FILE_NAME.split(".")[0] + ".txt", "w+")
# new_file.write(export_txt_file(r_joint))
# new_file.close()