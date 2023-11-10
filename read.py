#pip install regex
import re

f = open("CA096_500_bonds.CIF", "r")
lines = f.readlines()
loop1 = []
loop2 = []
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
        print()
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

print("loop1")
for dict1 in loop1:
    print(dict1)
    print('\n')


# print('\n')
# print('\n')

# print("loop2")
# for dict2 in loop2:
#     print(dict2)
#     print('\n')

