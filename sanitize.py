import csv

def sanitize_csv_file(input_file, output_file):
    # Open input file in text mode with UTF-8 encoding
    with open(input_file, mode='r', newline='') as infile:
        # Open output file in UTF-8 mode to write sanitized data
        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            # Loop through rows in input file and sanitize each cell
            for row in reader:
                sanitized_row = []
                for cell in row:
                    try:
                        # Try to decode cell as UTF-8
                        sanitized_cell = cell.encode('utf-8', 'replace').decode('utf-8')
                    except UnicodeDecodeError:
                        # Replace invalid byte sequence with a question mark
                        sanitized_cell = cell.encode('utf-8', 'replace').decode('utf-8', 'ignore')
                        sanitized_cell = sanitized_cell.replace('\ufffd', '?')
                    sanitized_row.append(sanitized_cell)
                
                writer.writerow(sanitized_row)

sanitize_csv_file("lyrics.csv", "output.csv")