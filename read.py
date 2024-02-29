"""
SCRIPT 1 (read.py inside of each folder): python read.py

SCRIPT 2 (read.py stored in one location): python "the path the file is located at"/read.py
"""

#pip install regex
import re
# pip install matplotlib
import matplotlib.pyplot as plt
#pip install pandas
from pandas import *
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
                if (len(res) != 0):
                    err = res[0].strip("()")
                else:
                    err = 0
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
                if(len(res) != 0):
                    err = res[0].strip("()")
                else:
                    err = 0
                #removes the error from the bond distance
                angle = re.sub(r'\([^)]*\)', "", split_line[3])

                # creates a dictionary with all of the values of the line stored inside
                line_dict = {"atom1": split_line[0], "atom2": split_line[1], "atom3": split_line[2], "geom_angle": angle, "error": err, "site_sym1": split_line[4], "site_sym2": split_line[5], "site_sym3": split_line[6]}

                #adds the dictionary to the second loop
                loop2.append(line_dict)


def FindDistance(test_distance, list_dict, dist_values):
    
    for pair in test_distance:
        val = ""
        for dict in list_dict:
            if (dict["atom1"] == pair[0] and dict["atom2"] == pair[1]):
                if val != "":
                    val += ", "
                val += dict["bond_dist"]
        dist_values.append(val)
    return dist_values


def FindAngles(atoms, list_dict, values):

    for pair in atoms:
        val = ""
        for dict in list_dict:
            if (dict["atom1"] == pair[0] and dict["atom2"] == pair[1] and dict["atom3"] == pair[2]):
                if val != "":
                    val += ", "
                val += dict["geom_angle"]
        values.append(val)
    return values

def CreateGraphs(col, title, value_des):
    x = []
    y = []
    with open('results.csv','r') as csvfile: 
        lines = csv.reader(csvfile, delimiter=',')
        next(lines)
        for row in lines:
            if row[col].find(','):
                values = row[col].split(", ")
                for val in values:
                    x.append(row[0])
                    y.append(float(val))
            else:
                x.append(row[0])
                y.append(float(row[col])) 
    
    plt.scatter(x, y, c='g', s = 100) 
    
    plt.xticks(rotation = 25) 
    plt.xlabel('Temperature(°F)') 
    plt.ylabel(value_des) 
    plt.title(f'{title}', fontsize = 20) 
    plt.show()

#****************************
# Code execution starts here
#****************************
    
if __name__ == "__main__" :


    # **************************************************************
    # THIS IS WHERE YOU WOULD AJUST THE VALUES THAT YOU WANT TO GET
    #***************************************************************
    distances = [["Zn1", "Mg1"], ["Zn1", "O3"], ["V1", "O3"]]
    # distances = []

    angles = [["O3", "Zn1", "O2"], ["O2", "Zn1", "O2"]]

    # UNCOMMENT OUT THIS LINE AND COMMENT THE ABOVE LINE TO IGNORE ANGLE RESULTS
    # angles = []

    # creating the header for the csv file
    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["Temp"]

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
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*.CIF'):
            temp = re.findall(r'\_.*?\_', file)
            temp = temp[0].strip("_")
            # print(temp)
            loop1 = []
            loop2 = []
            values = [temp]
            readFile(file)
            values = FindDistance(distances, loop1, values)
            values = FindAngles(angles, loop2, values)

            with open('results.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(values)

    # creating the different graphs
    with open('results.csv','r') as csvfile: 
        lines = csv.reader(csvfile, delimiter=',')
        header = []
        for row in lines:
            header = row
            break
        i = 1
        for val in header:
            
            if ( i <= len(distances)):
                CreateGraphs(i, header[i], "Bond Distance")
            elif (i < len(header)):
                CreateGraphs(i, header[i], "Geom Angle")
            i += 1

