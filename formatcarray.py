import os

MAX_FLOAT = 1.0
FILENAME = "Male_Low_Poly.obj"

scriptdir = os.path.dirname(__file__)
file  = open(scriptdir + "/obj/" + FILENAME, "r")
rows = file.read().split("\n")
orderedfloats = []
orderedfaces = []
for i in range(len(rows)):

    if rows[i].startswith("v"):
        splittedrow = rows[i].split(" ")
        for j in range(2, len(splittedrow)):
            orderedfloats.append(float(splittedrow[j]))

    if rows[i].startswith("f"):
        splittedrow = rows[i].split(" ")
        splittedrow = splittedrow[1:-1]
        orderedfaces.append(int(splittedrow[0]) - 1)
        orderedfaces.append(int(splittedrow[1]) - 1)
        orderedfaces.append(int(splittedrow[3]) - 1)
        orderedfaces.append(int(splittedrow[1]) - 1)
        orderedfaces.append(int(splittedrow[2]) - 1)
        orderedfaces.append(int(splittedrow[3]) - 1)

#vertice'lerin en büyüğü 'MAX_FLOAT' olacak şekilde scale edilme işlemi
orderedScaledFloats = []
maxFloat = max(orderedfloats)
for f in orderedfloats:
    orderedScaledFloats.append(f * (MAX_FLOAT / maxFloat))
orderedfloats = orderedScaledFloats

newfile = open(scriptdir + "/obj/formatted" + FILENAME.split(".")[0] + ".txt", "w+")
lines = ["float vertices[] = {\r"]
for i in range(0, len(orderedfloats), 3):
    #newline = "\t" + str(orderedfloats[i]) + ", " + str(orderedfloats[i + 1]) + ", " + str(orderedfloats[i + 2]) + ","
    newline = "\t" + '{:.20f}'.format(orderedfloats[i]) + ", " + '{:.20f}'.format(orderedfloats[i + 1]) + ", " + '{:.20f}'.format(orderedfloats[i + 2]) + ","
    if i + 3 == len(orderedfloats):
        newline = newline[:-1]
    newline += "\r"
    lines.append(newline)
lines.append("};")

lines.append("\r")
lines.append("\r")

lines.append("unsigned int indices[] = {\r")
for i in range(0, len(orderedfaces), 3):
    newline = "\t" + str(orderedfaces[i]) + ", " + str(orderedfaces[i + 1]) + ", " + str(orderedfaces[i + 2]) + ","
    if i + 3 == len(orderedfaces):
        newline = newline[:-1]
    newline += "\r"
    lines.append(newline)
lines.append("};")

newfile.writelines(lines)
newfile.close()

print("wait")