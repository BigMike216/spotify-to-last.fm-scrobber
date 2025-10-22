import linecache
import re
import time
import glob


def main():
    print("Starting convert\n")
    start_time = time.perf_counter()

    # Find all files matching the pattern StreamingHistory_music_*.json
    files = glob.glob('StreamingHistory_music_*.json')

    if not files:
        print("No files found matching pattern 'StreamingHistory_music_*.json'")
        return

    # Sort files to process them in order (0, 1, 2, ...)
    files.sort()
    print(f"Found {len(files)} files to process: {files}\n")

    all_songs = []  # This will store songs from all files

    # Process each file
    for file_num, file in enumerate(files, 1):
        print(f"Processing file {file_num}/{len(files)}: {file}")
        songs_from_file = process_file(file)
        all_songs.extend(songs_from_file)
        print(
            f"  - Found {len(songs_from_file)} songs (>30 seconds) in this file\n")

    print(f"Total songs found across all files: {len(all_songs)}")

    # Save all songs to a single CSV file with quotes and space after comma
    if all_songs:
        with open('output.csv', 'w', encoding='utf-8') as f:
            for artist, track in all_songs:
                # Write with quotes and a space after the comma
                f.write(f'"{artist}", "{track}"\n')
        print(f"Saved {len(all_songs)} songs to output.csv")
    else:
        print("No songs found to save")

    print("\nConvert finished in " +
          str(time.perf_counter() - start_time), "seconds.")


def process_file(file):
    """Process a single JSON file and return list of songs"""
    num_lines = sum(1 for line in open(file, encoding="utf8"))

    lines = []
    for i in range(1, num_lines):  # convert json into lines
        line = linecache.getline(file, i)
        line = line.strip()
        lines.append(line)

    # Clear linecache for this file to free memory
    linecache.clearcache()

    i = 3
    songs = []
    while i < num_lines:
        indiv_song_clean = []
        indiv_song = lines[i:i+3]

        for j in indiv_song:
            strng = match(j)
            indiv_song_clean.append(strng)

        # Filter out songs that were listened to for less than 30 seconds.
        if indiv_song_clean[2] >= 30000:
            # Store as [artist, track] list
            songs.append([indiv_song_clean[0], indiv_song_clean[1]])
        i = i+6

    return songs


def match(strng):  # extract relevant info
    match_info = re.search(r":(.*)", strng).group()
    match_info = match_info[2:]
    if match_info[0] == "\"":  # artist or song title
        # Remove quotes and any trailing comma
        match_info = match_info.strip('"').rstrip(',').strip('"')
    else:  # song duration
        # Remove trailing comma if present
        match_info = match_info.rstrip(',')
        match_info = int(match_info)
    return match_info


if __name__ == "__main__":
    main()
