#!/usr/bin/env python3
import json, sys, os, glob
from json.decoder import JSONDecodeError

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
            next_candidates = [x for x in (text.find('{', i+1), text.find('[', i+1)) if x != -1]
            if not next_candidates:
                break
            i = min(next_candidates)
            continue
        i = end
        yield obj

def iter_history_items(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    for val in iter_json_values(data):
        if isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    yield item
        elif isinstance(val, dict):
            yield val

def extract_pair(item):
    # Supports different Spotify export formats
    artist = (
        item.get('master_metadata_album_artist_name')
        or item.get('artistName')
        or item.get('artist')
    )
    track = (
        item.get('master_metadata_track_name')
        or item.get('trackName')
        or item.get('track')
        or item.get('song')
    )
    if artist and track:
        return str(artist), str(track)
    return None

def collect_files(inputs):
    files = []
    for p in inputs:
        matches = glob.glob(p, recursive=True)
        if not matches:
            matches = [p]
        for m in matches:
            if os.path.isdir(m):
                for root, _, filenames in os.walk(m):
                    for name in filenames:
                        if name.lower().endswith('.json'):
                            files.append(os.path.join(root, name))
            elif os.path.isfile(m):
                files.append(m)
    seen, unique = set(), []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique

def csv_quote(value: str) -> str:
    # Double any internal quotes to meet CSV escaping rules
    return '"' + value.replace('"', '""') + '"'

def main(argv):
    out_csv = 'output.csv'
    inputs = argv if argv else ['spotify_data.json']

    files = collect_files(inputs)
    if not files:
        sys.stderr.write('No input JSON files found.\n')
        sys.exit(1)

    rows = 0
    # newline='' avoids blank lines on Windows
    with open(out_csv, 'w', encoding='utf-8', newline='') as out:
        for path in files:
            for item in iter_history_items(path):
                pair = extract_pair(item)
                if not pair:
                    continue
                artist, track = pair
                # Produce: "Artist", "Track" (note the space after the comma)
                line = f'{csv_quote(artist)}, {csv_quote(track)}\n'
                out.write(line)
                rows += 1

    print(f'Wrote {rows} lines to {out_csv}')

if __name__ == '__main__':
    main(sys.argv[1:])