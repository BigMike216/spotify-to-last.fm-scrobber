import csv

lines_per_file = 2500
with open("output.csv", newline='', encoding="utf-8") as infile:
    reader = list(csv.reader(infile, skipinitialspace=True))
    header = reader[0]
    rows = reader[1:]

for i in range(0, len(rows), lines_per_file):
    chunk = rows[i:i + lines_per_file]
    fname = f"part{i//lines_per_file}.csv"
    with open(fname, "w", newline='', encoding="utf-8") as outfile:
        # Write header with quotes and space after comma
        outfile.write(', '.join(f'"{col}"' for col in header) + '\n')
        # Write each row
        for row in chunk:
            outfile.write(', '.join(f'"{cell}"' for cell in row) + '\n')
    print(f"Created {fname} with {len(chunk)} rows")
