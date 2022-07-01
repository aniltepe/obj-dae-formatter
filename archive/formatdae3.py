import os
import xml.etree.ElementTree as ET

FILE_NAME = "male.dae"

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

class joint:
    def __init__(self, name):
        self.name = name
        self.vertices = []
        self.weights = []


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

script_dir = os.path.dirname(__file__)
tree = ET.parse(script_dir + "/obj/" + FILE_NAME)
root = tree.getroot()

vertices = []
joints = []
weights = []

elements = []
parse_elements(root, 0, elements)

new_file = open(script_dir + "/obj/test.txt", "w+")
lines = []

parse_arrays(elements[0])

for vertice in vertices:
    for i in range(vertice.dual_count):
        joints[vertice.joints[i]].vertices.append(vertice)
        joints[vertice.joints[i]].weights.append(weights[vertice.weights[i]])

sum_vertices = 0
for joint in joints:
    new_line = "{0} => v_count: {1}, x max: {2}, x min: {3}, y max: {4}, y min: {5}, z max: {6}, z min: {7}\n\n"
    xmax = max([v.x for v in joint.vertices])
    xmin = min([v.x for v in joint.vertices])
    ymax = max([v.y for v in joint.vertices])
    ymin = min([v.y for v in joint.vertices])
    zmax = max([v.z for v in joint.vertices])
    zmin = min([v.z for v in joint.vertices])
    lines.append(new_line.format(joint.name, len(joint.vertices), xmax, xmin, ymax, ymin, zmax, zmin))
    sum_vertices += len(joint.vertices)

print(sum_vertices)
new_file.writelines(lines)
new_file.close()