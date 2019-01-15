import json

if __name__ == "__main__":
    with open("C:\\Users\\curti\\OneDrive\\Documents\\odds.txt", "r") as in_file:
        lines = in_file.readlines()

    column_names = lines[0].strip().split(',')
    column_names[0] = "DATE"
    la_counter = 0  # For distinguishing between LAC and LAL
    for i in range(len(column_names)):
        column_names[i] = column_names[i].split(' ')[0]
        if column_names[i] == "LA":
            if la_counter == 0:
                column_names[i] += "C"
                la_counter += 1
            else:
                column_names[i] += "L"

    records = []

    for i in range(31):
        new_column = []
        for line in lines[1:]:
            row_values = line.strip().split(',')
            for j in range(len(row_values)):
                if j == i:
                    if i > 0:
                        try:
                            appendee = int(row_values[j])
                        except ValueError:
                            appendee = round(float(row_values[j]), 9)
                    else:
                        appendee = row_values[j]
                    new_column.append(appendee)
        records.append(new_column)

    dictionary = dict(zip(column_names, records))

    json_string = json.dumps(dictionary, indent=4)
    print(json_string)

    with open("C:\\Users\\curti\\OneDrive\\Documents\\odds.json", "w") as out_file:
        out_file.write(json_string)
