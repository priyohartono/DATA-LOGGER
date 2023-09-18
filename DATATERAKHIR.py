import csv

# File paths
csv_file_path = 'your_file.csv'

# Read the existing CSV data into memory
def read_csv_file(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

# Write data to the CSV file
def write_to_csv_file(file_path, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

# Append a new line and limit to 10 lines
def append_to_csv(file_path, new_line):
    data = read_csv_file(file_path)

    # Append the new line
    data.append(new_line)

    # Check line count and remove the first line if needed
    if len(data) > 10:
        data.pop(0)

    # Write the updated data to the CSV file
    write_to_csv_file(file_path, data)

# Example usage
new_line_data = ['New Data 1', 'New Data 2', 'New Data 3']
append_to_csv(csv_file_path, new_line_data)
