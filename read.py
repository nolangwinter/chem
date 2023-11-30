#pip install regex
import re

loop1 = []
loop2 = []

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

readFile("CA096_500_bonds.CIF")

# print("loop1")
# for dict1 in loop1:
#     print(dict1)
#     print('\n')


# print('\n')
# print('\n')

# print("loop2")
# for dict2 in loop2:
#     print(dict2)
#     print('\n')

test_distance = [["Zn1", "O4"], ["Zn1", "O3"], ["V1", "O3"]]
test_angle = [["O3", "Zn1", "O2"], ["O2", "Zn1", "O2"]]

def FindDistance(test_distance, list_dict):
    for dict in list_dict:
        for pair in test_distance:
            if (dict["atom1"] == pair[0] and dict["atom2"] == pair[1]):
                print(f"The bond distance between {dict['atom1']} and {dict['atom2']} is {dict['bond_dist']}")


def FindAngles(atoms, list_dict):
    for dict in list_dict:
        for pair in atoms:
            if (dict["atom1"] == pair[0] and dict["atom2"] == pair[1] and dict["atom3"] == pair[2]):
                print(f"The geom angle between {dict['atom1']}, {dict['atom2']} and {dict['atom3']} is {dict['geom_angle']}")
        
FindDistance(test_distance, loop1)
FindAngles(test_angle, loop2)

