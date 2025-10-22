import json
import csv
import pandas as pd

# Method 1: Using pandas with quotes


def json_to_csv_pandas(input_file, output_file):
    """
    Convert JSON to CSV using pandas with quotes around all fields
    """
    # Read JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create DataFrame with only the columns we need
    df = pd.DataFrame(data)

    # Select and rename columns
    df_filtered = df[['master_metadata_album_artist_name',
                      'master_metadata_track_name']].copy()
    df_filtered.columns = ['Artist', 'Track']

    # Remove rows where either Artist or Track is None/null
    df_filtered = df_filtered.dropna()

    # Save to CSV with quotes around all fields
    df_filtered.to_csv(output_file, index=False, encoding='utf-8',
                       quoting=csv.QUOTE_ALL)
    print(
        f"Successfully converted {len(df_filtered)} records to {output_file}")

# Method 2: Using standard library with quotes


def json_to_csv_standard(input_file, output_file):
    """
    Convert JSON to CSV using standard library with quotes
    """
    with open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Open CSV file for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        # Configure writer to quote all fields
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

        # Write header
        writer.writerow(['Artist', 'Track'])

        # Write data rows
        count = 0
        for record in data:
            artist = record.get('master_metadata_album_artist_name')
            track = record.get('master_metadata_track_name')

            # Only write if both fields have values
            if artist and track:
                writer.writerow([artist, track])
                count += 1

        print(f"Successfully converted {count} records to {output_file}")

# Method 3: For extremely large files (streaming approach) with quotes


def json_to_csv_streaming(input_file, output_file):
    """
    Convert JSON to CSV using streaming for very large files
    """
    import ijson  # You'll need to install this: pip install ijson

    with open(input_file, 'rb') as json_file:
        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            # Configure writer to quote all fields
            writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

            # Write header
            writer.writerow(['Artist', 'Track'])

            # Parse JSON array items one by one
            parser = ijson.items(json_file, 'item')
            count = 0

            for record in parser:
                artist = record.get('master_metadata_album_artist_name')
                track = record.get('master_metadata_track_name')

                # Only write if both fields have values
                if artist and track:
                    writer.writerow([artist, track])
                    count += 1

                    # Print progress every 10000 records
                    if count % 10000 == 0:
                        print(f"Processed {count} records...")

            print(f"Successfully converted {count} records to {output_file}")

# Method 4: Simple version without header (if you don't want header row)


def json_to_csv_no_header(input_file, output_file):
    """
    Convert JSON to CSV without header row, with quotes
    """
    with open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

        count = 0
        for record in data:
            artist = record.get('master_metadata_album_artist_name')
            track = record.get('master_metadata_track_name')

            if artist and track:
                writer.writerow([artist, track])
                count += 1

        print(f"Successfully converted {count} records to {output_file}")


# Main execution
if __name__ == "__main__":
    # Specify your input and output file names
    input_json_file = "spotify_data.json"  # Replace with your JSON file name
    output_csv_file = "output.csv"  # Output CSV file name

    # Choose the method based on your needs:

    # With header row "Artist", "Track"
    try:
        json_to_csv_pandas(input_json_file, output_csv_file)
    except ImportError:
        print("pandas not installed. Using standard library method...")
        json_to_csv_standard(input_json_file, output_csv_file)

    # Without header row (just the data)
    # json_to_csv_no_header(input_json_file, output_csv_file)

    # For very large files where memory is a concern:
    # json_to_csv_streaming(input_json_file, output_csv_file)
