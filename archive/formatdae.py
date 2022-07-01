import os
import xml.etree.ElementTree as ET

FILE_NAME = "male.dae"

class nazim_element:
    def __init__(self):
        self.tag = ""
        self.text = ""
        self.attributes = {}
        self.children = []
        self.parent = None
        self.level = None

# def print_elements(root, level):
#     offset = ""
#     for i in range(level):
#         offset += "\t"
#     lines.append(offset + root.tag[root.tag.index("}") + 1:] + "\n")
#     for child in root:
#         print_elements(child, level + 1)

def print_nazim_elements(element):
    offset = ""
    for i in range(element.level):
        offset += "\t"
    text = ": " + element.text if not element.text == "" else ""
    if element.tag == "p" or element.tag == "v":
        tag = element.tag + "(count:" + str(len(element.text.split(" "))) + ", max: " + str(max([int(i) for i in element.text.split(" ")])) + ")"
    elif element.tag == "vcount":
        tag = element.tag + "(count:" + str(len(element.text.split(" "))) + ", sum: " + str(sum([int(i) for i in element.text.split(" ")])) + ")"
    else:
        tag = element.tag
    # tag = element.tag + "(count:" + str(len(element.text.split(" "))) + ")" if element.tag == "p" or element.tag == "v" else element.tag + "(count:" + str(len(element.text.split(" "))) + ", sum: " + str(sum([int(i) for i in element.text.split(" ")])) + ")" if element.tag == "vcount" else element.tag
    lines.append(offset + tag + text + "\n")
    for attr in element.attributes.keys():
        lines.append(offset + "\t+ " + attr + ": " + element.attributes[attr] + "\n")
    for child in element.children:
        print_nazim_elements(child)

def parse_elements(node, level, parent):
    nazim = nazim_element()
    nazim.level = level
    nazim.tag = node.tag[node.tag.index("}") + 1:]
    nazim.text = "" if node.text == None else node.text.strip().replace("\n", " ")
    nazim.attributes = node.attrib
    if level == 0:
        parent.append(nazim)
    else:
        nazim.parent = parent
        parent.children.append(nazim)
    for child in node:
        parse_elements(child, level + 1, nazim)

script_dir = os.path.dirname(__file__)
tree = ET.parse(script_dir + "/obj/" + FILE_NAME)
root = tree.getroot()

nazim_elements = []
parse_elements(root, 0, nazim_elements)

new_file = open(script_dir + "/obj/formatted_" + FILE_NAME.split(".")[0] + ".txt", "w+")
lines = []

# print_elements(root, 0)

print_nazim_elements(nazim_elements[0])

new_file.writelines(lines)
new_file.close()