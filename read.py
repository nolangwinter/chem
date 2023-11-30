#pip install regex
import re
import matplotlib.pyplot as plt
import fnmatch
import os
import csv


# this function will read the file and split each line into a dictionary 
def readFile(filename):
    f = open(filename, "r")
    lines = f.readlines()

    # keeps track of what loop in the file it is on
    cur_loop = ""

    for line in lines:
        line = line.strip()
        if (line == ''):
            pass
        elif (line == "loop_"):
            if (cur_loop == ""):
                cur_loop = "loop1"
            else:
                cur_loop = "loop2"
        elif(line[0] == '_'):
            pass
        else:
            split_line = line.split()
            if (cur_loop == "loop1"):
                #gets the error connected to the bond distance
                res = re.findall(r'\(.*?\)', split_line[2])
                #removes the parenthesis around the value
                err = res[0].strip("()")
                #removes the error from the bond distance
                distance = re.sub(r'\([^)]*\)', "", split_line[2])

                # creates a dictionary with all of the values of the line stored in it
                line_dict = {"atom1": split_line[0], "atom2": split_line[1], "bond_dist": distance, "error": err, "site_sym1": split_line[3], "site_sym2": split_line[4]}

                # adds the dictionary to the first loop list
                loop1.append(line_dict)
            else:
                #gets the error connected to the geo angle
                res = re.findall(r'\(.*?\)', split_line[3])
                #removes the parenthesis around the value
                err = res[0].strip("()")
                #removes the error from the bond distance
                angle = re.sub(r'\([^)]*\)', "", split_line[3])

                # creates a dictionary with all of the values of the line stored inside
                line_dict = {"atom1": split_line[0], "atom2": split_line[1], "atom3": split_line[2], "geom_angle": angle, "error": err, "site_sym1": split_line[4], "site_sym2": split_line[5], "site_sym3": split_line[6]}

                #adds the dictionary to the second loop
                loop2.append(line_dict)


def FindDistance(test_distance, list_dict, dist_values):
    for dict in list_dict:
        for pair in test_distance:
            if (dict["atom1"] == pair[0] and dict["atom2"] == pair[1]):
                dist_values.append(float(dict["bond_dist"]))
    return dist_values


def FindAngles(atoms, list_dict, values):
    angle_values = []
    for dict in list_dict:
        for pair in atoms:
            if (dict["atom1"] == pair[0] and dict["atom2"] == pair[1] and dict["atom3"] == pair[2]):
                values.append(float(dict["geom_angle"]))
    return values



test_distance = [["Zn1", "O4"], ["Zn1", "O3"], ["V1", "O3"]]
test_angle = [["O3", "Zn1", "O2"], ["O2", "Zn1", "O2"]]


# Code execution starts here

# **************************************************************
# THIS IS WHERE YOU WOULD AJUST THE VALUES THAT YOU WANT TO GET
#***************************************************************
distances = [["Zn1", "O4"], ["Zn1", "O3"], ["V1", "O3"]]
angles = [["O3", "Zn1", "O2"], ["O2", "Zn1", "O2"]]

# creating the header for the csv file
with open('results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["tempurature"]

    for i in range(len(distances)):
        index = 0
        atoms = ""
        while (index <= 1):
            atoms += distances[i][index]
            if (index != 1):
                atoms += " and "
            index += 1
        field.append(atoms)

    for i in range(len(angles)):
        index = 0
        atoms = ""
        while (index <= 2):
            atoms += angles[i][index]
            if (index != 2):
                atoms += " and "
            index += 1
        field.append(atoms)

    writer.writerow(field)
    
# looping through the .CIF files and adding the desired results to results.csv
current_temp = 500
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.CIF'):
        print(file)
        loop1 = []
        loop2 = []
        values = [current_temp]
        readFile(file)
        values = FindDistance(distances, loop1, values)
        values = FindAngles(angles, loop2, values)
        print(values)
        print("\n")
        with open('results.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(values)

        current_temp += 50


        

