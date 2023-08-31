filenametemp = ('temp.csv')
def delete_first_line_in_csv(filenametemp):
    with open(filenametemp, 'r') as file:
        lines = file.readlines()  # Read all lines into a list

    with open(filenametemp, 'w') as file:
        file.writelines(lines[1:])  # Write all lines except the first one

delete_first_line_in_csv(filenametemp)
