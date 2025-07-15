import sqlite3
import os
import sys
import requests
from datetime import datetime
from termcolor import colored
import time

DJ_ICON = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢄⣀⠔⣋⣉⣝⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡴⠋⢉⣬⠮⡞⠁⠀⠉⢲⢿⡿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠜⡵⢫⢤⣇⠀⡇⠀⠀⠀⢸⠀⣿⡌⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡏⢲⠙⡛⢧⣀⢀⣠⠾⣗⡉⡎⠑⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡸⢠⡏⡜⣁⡤⠏⠉⠧⣄⡹⠘⠷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⠃⢰⡵⠊⠁⠀⠀⠀⠀⠀⠈⠳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⡀⠀⣀⡠⡆⠀⠀⠀⠀⠀⣆⠀⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠀⡇⠀⠀⠀⠀⠀⡏⢣⡀⠘⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⢸⠀⠙⢤⡈⢦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⠖⣒⣶⠖⠒⠒⠒⠲⠷⣒⠒⠒⠒⠒⣺⣶⠖⠒⠓⢤⣹⠶⣒⠲⡄⠀⠀
⠀⢠⠏⣞⣟⠉⠀⣖⠒⣲⠀⠀⠈⣳⠀⠀⡎⡞⠉⠀⣖⢒⣢⠀⠀⠈⡇⠹⡄⠀
⢠⠏⠀⠘⠪⢅⣀⣀⠉⣀⣀⡠⠔⠁⠀⠀⠙⠮⣇⣀⣀⠉⣀⣀⡤⠖⠁⠀⠹⡄
⡟⠒⠒⠒⠒⠒⠒⠓⠛⠚⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠚⠛⠛⠒⠒⠒⠒⠒⠒⢻
⣇⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣸
"""

MUSICBRAINZ_API_URL = "https://musicbrainz.org/ws/2/artist/"


def search_artist_online(track_title):
    params = {"query": track_title, "fmt": "json", "limit": 1}
    try:
        response = requests.get(MUSICBRAINZ_API_URL + "?", params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "artists" in data and len(data["artists"]) > 0:
            return data["artists"][0]["name"]
    except requests.RequestException:
        return None
    return None


def get_playlists_by_date(cursor, date):
    query = """
    SELECT id, name, date_created FROM playlists
    WHERE hidden = 2 AND date_created LIKE ?
    ORDER BY date_created;
    """
    cursor.execute(query, (f"%{date}%",))
    return cursor.fetchall()


def get_track_count(cursor, playlist_id):
    query = "SELECT COUNT(*) FROM PlaylistTracks WHERE playlist_id = ?"
    cursor.execute(query, (playlist_id,))
    return cursor.fetchone()[0]


def get_tracklist(cursor, playlist_id):
    query = """
    SELECT COALESCE(NULLIF(l.artist, ''), 'Unknown Artist'), 
           COALESCE(NULLIF(l.title, ''), 'Unknown') 
    FROM library l
    JOIN PlaylistTracks pt ON l.id = pt.track_id
    WHERE pt.playlist_id = ?
    ORDER BY pt.position;
    """
    cursor.execute(query, (playlist_id,))
    return cursor.fetchall()


def export_tracklist(date, tracks, playlist_id=None):
    filename = f"tracklist_{date}.txt" if playlist_id is None else f"tracklist_{date}_playlist_{playlist_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Tracklist:\n")
        for artist, title in tracks:
            if artist == "Unknown Artist":
                artist = search_artist_online(title) or "Unknown Artist"
            artist = (
                artist.replace("_", " ")
                if artist.isupper()
                else artist.title().replace("_", " ")
            )
            title = (
                title.replace("_", " ")
                if title.isupper()
                else title.title().replace("_", " ")
            )
            f.write(f"{artist} - {title}\n")
    print_wavy_text(f"🎶 Saved: {filename} 🎶")


def print_wavy_text(text, delay=0.02):
    colors = ["red", "yellow", "green", "blue", "magenta", "cyan"]
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        sys.stdout.write(colored(char, color))
        sys.stdout.flush()
        time.sleep(delay)
    print()


def main():
    default_db_path = os.path.expandvars(
        r"%USERPROFILE%\Local Settings\Application Data\Mixxx\mixxxdb.sqlite"
    )
    today_date = datetime.today().strftime("%Y-%m-%d")

    print(colored(DJ_ICON, "cyan"))
    print_wavy_text("Welcome to the DJ Tracklist Exporter! 🎧")
    print(colored("=====================================", "yellow"))

    db_path = (
        input(
            colored(
                f"Enter the database path (Press Enter to use default: {default_db_path}): ",
                "magenta",
            )
        )
        or default_db_path
    )

    if not os.path.exists(db_path):
        print(colored("❌ Error: Database file not found. ❌", "red"))
        return

    date_input = (
        input(
            colored(
                f"Enter the set date (YYYY-MM-DD) (Press Enter to use the current date: {today_date}): ",
                "magenta",
            )
        )
        or today_date
    )

    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print(colored("❌ Invalid date format. Please enter YYYY-MM-DD. ❌", "red"))
        return

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        playlists = get_playlists_by_date(cursor, date_input)
        if not playlists:
            print(colored("❌ No playlist found for this date. ❌", "red"))
            return

        if len(playlists) > 1:
            print(colored(f"\n📅 Multiple playlists found for {date_input}:\n", "cyan"))
            for idx, (pid, name, created) in enumerate(playlists, 1):
                track_count = get_track_count(cursor, pid)
                print(f"{idx}. Playlist ID {pid} — {name} — Created: {created} — Tracks: {track_count}")

            choice = input(colored("\nEnter playlist number to export or type 'all' to export all: ", "magenta")).strip().lower()
            if choice == "all":
                for pid, name, _ in playlists:
                    tracks = get_tracklist(cursor, pid)
                    if tracks:
                        export_tracklist(date_input, tracks, playlist_id=pid)
                    else:
                        print(colored(f"⚠️  Playlist {pid} has no tracks.", "yellow"))
                return
            try:
                choice = int(choice)
                if not (1 <= choice <= len(playlists)):
                    raise ValueError
                playlist_id, _, _ = playlists[choice - 1]
            except ValueError:
                print(colored("❌ Invalid selection. ❌", "red"))
                return
        else:
            playlist_id, _, _ = playlists[0]

        tracks = get_tracklist(cursor, playlist_id)
        if not tracks:
            print(colored("❌ No tracks found for this playlist. ❌", "red"))
            return

        export_tracklist(date_input, tracks)


if __name__ == "__main__":
    main()
