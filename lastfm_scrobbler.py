#!/usr/bin/env python3
import pylast
import time
import os
import sys
import glob
import re
from datetime import datetime
from dotenv import load_dotenv
import json
import csv

# Load environment variables
load_dotenv()


class LastFMScrobbler:
    def __init__(self):
        """Initialize Last.fm connection"""
        try:
            # Get credentials from .env file
            API_KEY = os.getenv('LASTFM_API_KEY')
            API_SECRET = os.getenv('LASTFM_API_SECRET')
            USERNAME = os.getenv('LASTFM_USERNAME')
            PASSWORD = os.getenv('LASTFM_PASSWORD')

            if not all([API_KEY, API_SECRET, USERNAME, PASSWORD]):
                raise ValueError("Missing credentials in .env file!")

            # Generate password hash
            password_hash = pylast.md5(PASSWORD)

            # Create network object
            self.network = pylast.LastFMNetwork(
                api_key=API_KEY,
                api_secret=API_SECRET,
                username=USERNAME,
                password_hash=password_hash
            )

            print(f"✅ Connected to Last.fm as {USERNAME}")

        except Exception as e:
            print(f"❌ Failed to connect to Last.fm: {e}")
            sys.exit(1)

    def list_part_indices(self, directory="MusicCSV"):
        """Return sorted list of available part indices from MusicCSV/part*.csv"""
        files = glob.glob(os.path.join(directory, "part*.csv"))
        indices = []
        for p in files:
            m = re.match(r"^part(\d+)\.csv$", os.path.basename(p))
            if m:
                indices.append(int(m.group(1)))
        return sorted(indices)

    def read_csv_file(self, filepath):
        """Read CSV file and return list of songs with better error handling"""
        songs = []
        problematic_lines = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                # Try standard CSV reader first
                csv_reader = csv.reader(
                    file, quotechar='"', skipinitialspace=True)

                for line_num, row in enumerate(csv_reader, 1):
                    try:
                        if len(row) >= 2:
                            # Take first two elements as artist and track
                            artist = row[0].strip().strip('"').strip()
                            track = row[1].strip().strip('"').strip()

                            # Skip header-like entries and empty
                            if artist and track and not (
                                artist.lower() == "artist" and track.lower() == "track"
                            ):
                                songs.append(
                                    {'artist': artist, 'track': track})
                        elif len(row) == 1 and ',' in row[0]:
                            # Try to split manually if CSV reader failed
                            parts = row[0].split(',', 1)
                            if len(parts) == 2:
                                artist = parts[0].strip().strip('"').strip()
                                track = parts[1].strip().strip('"').strip()
                                if artist and track and not (
                                    artist.lower() == "artist" and track.lower() == "track"
                                ):
                                    songs.append(
                                        {'artist': artist, 'track': track})
                    except Exception as e:
                        problematic_lines.append({
                            'line': line_num,
                            'content': str(row),
                            'error': str(e)
                        })
                        continue

            print(f"📁 Successfully loaded {len(songs)} songs from {filepath}")

            if problematic_lines:
                print(f"⚠️ Skipped {len(problematic_lines)} problematic lines")
                # Save problematic lines for review
                problem_file = f"problematic_lines_{os.path.basename(filepath)}.json"
                with open(problem_file, 'w') as f:
                    json.dump(problematic_lines, f, indent=2)
                print(f"💾 Problematic lines saved to: {problem_file}")

            return songs

        except FileNotFoundError:
            print(f"❌ File not found: {filepath}")
            return []
        except Exception as e:
            print(f"❌ Error reading file {filepath}: {e}")

            # Try alternative parsing method
            print("🔄 Attempting alternative parsing method...")
            return self.read_csv_alternative(filepath)

    def read_csv_alternative(self, filepath):
        """Alternative method to read CSV with manual parsing"""
        songs = []
        problematic_lines = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()

            print(f"📄 File has {len(lines)} lines total")

            for line_num, line in enumerate(lines, 1):
                try:
                    line = line.strip()
                    if not line:
                        continue

                    # Handle different possible formats
                    if '", "' in line:
                        # Format: "artist", "track"
                        parts = line.split('", "')
                        if len(parts) == 2:
                            artist = parts[0].strip().strip('"').strip()
                            track = parts[1].strip().strip('"').strip()
                        else:
                            continue
                    elif '","' in line:
                        # Format: "artist","track"
                        parts = line.split('","')
                        if len(parts) == 2:
                            artist = parts[0].strip().strip('"').strip()
                            track = parts[1].strip().strip('"').strip()
                        else:
                            continue
                    elif ',' in line:
                        # Try to intelligently split
                        # If line starts and ends with quotes, find the middle separation
                        if line.startswith('"') and line.endswith('"'):
                            # Remove outer quotes
                            line = line[1:-1]
                            # Find the separator pattern
                            if '", "' in line:
                                parts = line.split('", "', 1)
                            elif '","' in line:
                                parts = line.split('","', 1)
                            else:
                                parts = line.split(',', 1)
                        else:
                            parts = line.split(',', 1)

                        if len(parts) == 2:
                            artist = parts[0].strip().strip('"').strip()
                            track = parts[1].strip().strip('"').strip()
                        else:
                            continue
                    else:
                        continue

                    # Skip header-like entries and empty
                    if artist and track and not (
                        artist.lower() == "artist" and track.lower() == "track"
                    ):
                        songs.append({'artist': artist, 'track': track})

                except Exception as e:
                    problematic_lines.append({
                        'line': line_num,
                        'content': line[:100],  # First 100 chars
                        'error': str(e)
                    })
                    continue

            print(f"✅ Alternative parsing loaded {len(songs)} songs")

            if problematic_lines:
                print(f"⚠️ Could not parse {len(problematic_lines)} lines")
                problem_file = f"problematic_lines_alt_{os.path.basename(filepath)}.json"
                with open(problem_file, 'w') as f:
                    json.dump(problematic_lines, f, indent=2)
                print(f"💾 Problematic lines saved to: {problem_file}")

            return songs

        except Exception as e:
            print(f"❌ Alternative parsing also failed: {e}")
            return []

    def scrobble_batch(self, songs_batch, batch_num, total_batches):
        """Scrobble a batch of songs (max 50)"""
        try:
            # Calculate timestamps (scrobbling backwards in time)
            current_time = int(time.time())

            # Prepare batch for scrobbling
            scrobbles = []
            for i, song in enumerate(songs_batch):
                # Each song 3 minutes apart going backwards
                timestamp = current_time - (i * 180)

                scrobbles.append({
                    'artist': song['artist'],
                    'title': song['track'],
                    'timestamp': timestamp
                })

            # Scrobble the batch
            self.network.scrobble_many(scrobbles)

            print(
                f"✅ Batch {batch_num}/{total_batches} scrobbled successfully ({len(songs_batch)} songs)")
            return True

        except Exception as e:
            print(f"❌ Error scrobbling batch {batch_num}: {e}")
            # Try to scrobble individually if batch fails
            print("🔄 Attempting individual scrobbles...")
            return self.scrobble_individually(songs_batch, batch_num)

    def scrobble_individually(self, songs_batch, batch_num):
        """Fallback method to scrobble songs one by one"""
        success_count = 0
        current_time = int(time.time())

        for i, song in enumerate(songs_batch):
            try:
                timestamp = current_time - (i * 180)
                self.network.scrobble(
                    artist=song['artist'],
                    title=song['track'],
                    timestamp=timestamp
                )
                success_count += 1
                print(f"  ✓ Scrobbled: {song['artist']} - {song['track']}")
                time.sleep(0.5)  # Small delay between individual scrobbles
            except Exception as e:
                print(f"  ✗ Failed: {song['artist']} - {song['track']} ({e})")

        print(
            f"📊 Batch {batch_num}: {success_count}/{len(songs_batch)} songs scrobbled individually")
        return success_count > 0

    def process_file(self, file_number):
        """Process a single CSV file"""
        # Construct file path
        filepath = f"MusicCSV/part{file_number}.csv"

        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return False

        print(f"\n{'='*50}")
        print(f"📂 Processing: {filepath}")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        # Read songs from CSV
        songs = self.read_csv_file(filepath)

        if not songs:
            print("❌ No songs to scrobble!")
            return False

        # Show sample of what will be scrobbled
        print("\n📋 Sample of songs to be scrobbled:")
        print("-" * 50)
        for i, song in enumerate(songs[:5]):
            print(f"{i+1}. {song['artist']} - {song['track']}")
        if len(songs) > 5:
            print(f"... and {len(songs) - 5} more songs")
        print("-" * 50)

        # Process in batches of 50
        batch_size = 50
        total_batches = (len(songs) + batch_size - 1) // batch_size
        successful_batches = 0
        failed_songs = []

        print(f"\n📊 Total songs: {len(songs)}")
        print(f"📦 Total batches: {total_batches} (up to 50 songs each)\n")

        # Confirm before proceeding
        confirm = input("Do you want to proceed? (yes/no): ").lower()
        if confirm != 'yes':
            print("❌ Cancelled by user")
            return False

        print("\n🚀 Starting scrobbling process...\n")

        # Process each batch
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(songs))
            batch = songs[start_idx:end_idx]

            print(f"Processing songs {start_idx + 1} to {end_idx}...")

            # Scrobble the batch
            success = self.scrobble_batch(batch, batch_num + 1, total_batches)

            if success:
                successful_batches += 1
            else:
                failed_songs.extend(batch)

            # Wait between batches to avoid rate limiting
            if batch_num < total_batches - 1:
                print("⏳ Waiting 3 seconds before next batch...")
                time.sleep(3)

        # Print summary
        print(f"\n{'='*50}")
        print("📊 SUMMARY")
        print(f"{'='*50}")
        print(f"✅ Successful batches: {successful_batches}/{total_batches}")
        print(
            f"✅ Songs scrobbled: {(successful_batches * batch_size) - (batch_size - len(songs) % batch_size if len(songs) % batch_size != 0 else 0)}")
        print(f"❌ Failed songs: {len(failed_songs)}")

        # Save failed songs if any
        if failed_songs:
            failed_file = f"failed_songs_part{file_number}.json"
            with open(failed_file, 'w') as f:
                json.dump(failed_songs, f, indent=2)
            print(f"💾 Failed songs saved to: {failed_file}")

        # Save progress
        self.save_progress(file_number)

        return True

    def save_progress(self, file_number):
        """Save progress to track which files have been processed"""
        progress_file = "scrobble_progress.json"

        try:
            if os.path.exists(progress_file):
                with open(progress_file, 'r') as f:
                    progress = json.load(f)
            else:
                progress = {'completed': [], 'last_run': {}}

            if file_number not in progress['completed']:
                progress['completed'].append(file_number)

            progress['last_run'] = {
                'file': f"part{file_number}.csv",
                'date': datetime.now().isoformat(),
                'timestamp': int(time.time())
            }

            with open(progress_file, 'w') as f:
                json.dump(progress, f, indent=2)

        except Exception as e:
            print(f"⚠️ Could not save progress: {e}")

    def check_progress(self):
        """Check which files have been processed dynamically"""
        progress_file = "scrobble_progress.json"
        available = self.list_part_indices()

        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                progress = json.load(f)
        else:
            progress = {'completed': [], 'last_run': {}}

        completed = sorted(set(progress.get('completed', [])))
        remaining = [i for i in available if i not in completed]

        print("\n📊 PROGRESS STATUS:")
        print(f"{'='*50}")
        print(f"Available files: {[f'part{i}.csv' for i in available]}")
        print(f"Completed files: {completed}")
        if remaining:
            print(
                f"Remaining files: {', '.join([f'part{i}.csv' for i in remaining])}")
        else:
            print("All files completed!")
        if 'last_run' in progress:
            print(
                f"Last run: {progress['last_run'].get('file', 'N/A')} on {progress['last_run'].get('date', 'N/A')}")
        print(f"{'='*50}\n")

        return completed


def main():
    """Main function"""
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║   Last.fm Batch Scrobbler v2.0 by BIG MIKE >~<    ║
    ╚═══════════════════════════════════════════════════╝
    """)

    # Create scrobbler instance
    scrobbler = LastFMScrobbler()

    # Find available part files dynamically
    available = scrobbler.list_part_indices()
    if not available:
        print("❌ No part*.csv files found in MusicCSV/")
        return

    # Check progress
    completed = scrobbler.check_progress()
    remaining = [i for i in available if i not in completed]

    # Get next file to process
    if not remaining:
        print("✅ All files have been processed!")
        return

    next_file = remaining[0]

    print(f"📌 Next file to process: part{next_file}.csv")
    print("\nOptions:")
    print("1. Process next file automatically")
    print("2. Choose a specific file")
    print("3. Check a CSV file for issues")
    print("4. Exit")

    nums_list = ", ".join(str(i) for i in available)
    choice = input("\nEnter your choice (1-4): ")

    if choice == '1':
        scrobbler.process_file(next_file)
    elif choice == '2':
        try:
            file_num = int(input(f"Enter file number ({nums_list}): "))
        except ValueError:
            print("❌ Invalid number!")
            return
        if file_num in available:
            scrobbler.process_file(file_num)
        else:
            print("❌ Invalid file number!")
    elif choice == '3':
        try:
            file_num = int(
                input(f"Enter file number to check ({nums_list}): "))
        except ValueError:
            print("❌ Invalid number!")
            return
        if file_num in available:
            filepath = f"MusicCSV/part{file_num}.csv"
            songs = scrobbler.read_csv_file(filepath)
            if songs:
                print(
                    f"\n✅ File is readable! Contains {len(songs)} valid songs")
                print("\nFirst 10 songs:")
                for i, song in enumerate(songs[:10], 1):
                    print(f"{i}. {song['artist']} - {song['track']}")
        else:
            print("❌ Invalid file number!")
    elif choice == '4':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice!")


if __name__ == "__main__":
    main()
