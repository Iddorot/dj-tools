import sqlite3
import os
from datetime import datetime

def get_playlist_id(cursor, date):
    """Fetches the playlist ID for a given date."""
    query = "SELECT id FROM playlists WHERE hidden = 2 AND name = ?"
    cursor.execute(query, (date,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_tracklist(cursor, playlist_id):
    """Retrieves the tracklist for a given playlist ID."""
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

def export_tracklist(date, tracks):
    """Exports the tracklist to a text file."""
    filename = f"tracklist_{date}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Tracklist:\n")
        for artist, title in tracks:
            artist = artist.replace("_", " ") if artist.isupper() else artist.title().replace("_", " ")
            title = title.replace("_", " ") if title.isupper() else title.title().replace("_", " ")
            f.write(f"{artist} - {title}\n")
    print(f"Tracklist saved as {filename}")

def main():
    """Main function to handle user input and generate tracklist export."""
    default_db_path = os.path.expandvars(r"%USERPROFILE%\Local Settings\Application Data\Mixxx\mixxxdb.sqlite")
    today_date = datetime.today().strftime('%Y-%m-%d')

    db_path = input(f"Enter the database path (Press Enter to use default: {default_db_path}): ") or default_db_path

    if not os.path.exists(db_path):
        print("Error: Database file not found.")
        return

    date_input = input(f"Enter the set date (YYYY-MM-DD) (Press Enter to use the current date: {today_date}): ") or today_date

    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")
        return

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        playlist_id = get_playlist_id(cursor, date_input)
        if not playlist_id:
            print("No playlist found for this date.")
            return

        tracks = get_tracklist(cursor, playlist_id)
        if not tracks:
            print("No tracks found for this playlist.")
            return

        export_tracklist(date_input, tracks)

if __name__ == "__main__":
    main()
