# Mixxx Tracklist Generator

## Overview
This utility exports a tracklist from the [Mixxx](https://mixxx.org/) open-source DJ software's database. It retrieves the tracks from a playlist based on a specified date and generates a formatted text file.

## Features
- Queries the Mixxx database for a playlist created on a specific date.
- Extracts track details (artist and title) from the playlist and saves the tracklist in a `tracklist_<date>.txt` file.

## Requirements
- Python 3
- SQLite3 (or another compatible database system if configured)

## Usage
1. Run the script:
   ```sh
   python generate_tracklist.py
   ```
2. Enter the database path when prompted (or press Enter to use the default Mixxx database location: `%USERPROFILE%\Local Settings\Application Data\Mixxx\mixxxdb.sqlite`).
3. Enter the set date in `YYYY-MM-DD` format.
4. The script will generate a text file containing the tracklist.

## Example Output
```
Tracklist:
Artist 1 - Track 1
Artist 2 - Track 2
...
```
