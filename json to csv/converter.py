#!/usr/bin/env python3
import json
import sys
import os
import glob
import time
import csv
from json.decoder import JSONDecodeError

# Config
MIN_MS_PLAYED = 30          # Only include plays >= 30s
OUTPUT_CSV = 'output.csv'   # Master CSV file
SPLIT_OUTPUT = True         # Split into parts after writing master CSV
LINES_PER_FILE = 2600       # Rows per part file


def csv_quote(value: str) -> str:
    """Quote a value for CSV output."""
    return '"' + str(value).replace('"', '""') + '"'


def iter_json_values(text):
    """Iteratively decode multiple top-level JSON values from a single string."""
    dec = json.JSONDecoder()
    i, n = 0, len(text)
    while i < n:
        while i < n and text[i].isspace():
            i += 1
        if i >= n:
            break
        try:
            obj, end = dec.raw_decode(text, i)
        except JSONDecodeError:
            # Try to resync to the next JSON object/array
            next_candidates = [x for x in (
                text.find('{', i+1), text.find('[', i+1)) if x != -1]
            if not next_candidates:
                break
            i = min(next_candidates)
            continue
        i = end
        yield obj


def iter_history_items(path):
    """Yield individual history items from a JSON file that may contain multiple top-level values."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()

        for val in iter_json_values(data):
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, dict):
                        yield item
            elif isinstance(val, dict):
                yield val
    except Exception:
        # Ignore unreadable/invalid files
        return


def _first_nonempty(d: dict, keys):
    for k in keys:
        v = d.get(k)
        if v not in (None, "", []):
            return v
    return None


def extract_pair(item):
    """Extract (artist, track) from a history item across multiple export formats."""
    artist = _first_nonempty(item, [
        'master_metadata_album_artist_name',  # endsong
        'artistName',                         # StreamingHistory
        'artist',                             # generic fallback
    ])
    track = _first_nonempty(item, [
        'master_metadata_track_name',         # endsong
        'trackName',                          # StreamingHistory
        'track',                              # generic fallback
        'song',                               # some exports
    ])

    if artist and track:
        return str(artist), str(track)
    return None


def extract_duration_ms(item):
    """Best-effort extraction of play duration in ms across formats."""
    for k in ('ms_played', 'msPlayed', 'playback_duration_ms', 'playbackDurationMs', 'duration_ms'):
        if k in item and item[k] is not None:
            try:
                return int(item[k])
            except (TypeError, ValueError):
                pass
    return None


def find_spotify_history_files():
    """Find Spotify history JSON files in the current directory."""
    patterns = [
        'StreamingHistory_music_*.json',
        'StreamingHistory*.json',
        'Streaming_History_Audio_*.json',
        'Streaming_History_*.json',
        'endsong_*.json',
        '*History*.json',
    ]

    found_files = []
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            found_files.extend(matches)

    # If no pattern matches, just use all JSON files
    if not found_files:
        json_files = [f for f in glob.glob('*.json') if os.path.isfile(f)]
        found_files = json_files

    # Remove duplicates while preserving order and only keep real files
    seen = set()
    unique_files = []
    for f in found_files:
        if f not in seen and os.path.isfile(f):
            seen.add(f)
            unique_files.append(f)

    return sorted(unique_files)


def write_output_csv(files, out_path):
    """Write the master CSV with header and return number of data rows written."""
    rows = 0
    with open(out_path, 'w', encoding='utf-8', newline='') as out:
        # Data rows
        for path in files:
            try:
                for item in iter_history_items(path):
                    pair = extract_pair(item)
                    if not pair:
                        continue
                    duration = extract_duration_ms(item)
                    if duration is not None and duration >= MIN_MS_PLAYED:
                        artist, track = pair
                        out.write(f'{csv_quote(artist)}, {csv_quote(track)}\n')
                        rows += 1
            except Exception:
                # Skip unreadable/corrupt files
                continue
    return rows


def split_csv_into_parts(in_path, lines_per_file):
    """Split the master CSV into partN.csv files with the same header."""
    if lines_per_file <= 0:
        return 0

    parts_created = 0
    try:
        with open(in_path, newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile, skipinitialspace=True)
            header = next(reader, None)
            if not header:
                return 0

            outfile = None
            part_idx = 0
            cur_rows = 0
            cur_name = None

            for idx, row in enumerate(reader):
                # Start a new part file at boundaries
                if idx % lines_per_file == 0:
                    if outfile:
                        outfile.close()
                        print(f"Created {cur_name} with {cur_rows} rows")
                    cur_name = f"part{part_idx}.csv"
                    outfile = open(cur_name, "w", newline='', encoding="utf-8")
                    # Write header with quotes and space after comma
                    outfile.write(', '.join(csv_quote(col)
                                  for col in header) + '\n')
                    part_idx += 1
                    parts_created += 1
                    cur_rows = 0

                # Write row with quotes and space after comma
                outfile.write(', '.join(csv_quote(cell)
                              for cell in row) + '\n')
                cur_rows += 1

            if outfile:
                outfile.close()
                print(f"Created {cur_name} with {cur_rows} rows")
    except FileNotFoundError:
        return 0
    return parts_created


def main(argv):
    print("Converting Spotify history to CSV...")
    start_time = time.perf_counter()

    # Determine files: use CLI args if given, else auto-discover
    files = argv if argv else find_spotify_history_files()

    if not files:
        print("No JSON files found in current directory.")
        sys.exit(1)

    try:
        rows = write_output_csv(files, OUTPUT_CSV)
    except Exception as e:
        print(f"Error creating output file: {e}")
        sys.exit(1)

    elapsed = time.perf_counter() - start_time
    if rows > 0:
        print(
            f"Conversion completed! {rows} tracks saved to {OUTPUT_CSV} ({elapsed:.1f}s)")
    else:
        print(f"No tracks found to convert. ({elapsed:.1f}s)")

    # Optionally split into parts
    if SPLIT_OUTPUT and rows > 0:
        split_csv_into_parts(OUTPUT_CSV, LINES_PER_FILE)


if __name__ == '__main__':
    main(sys.argv[1:])
