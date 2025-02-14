import sqlite3
import datetime
import os

def get_playlist_id(cursor, date):
    query = """
    SELECT id FROM playlists WHERE hidden = 2 AND name = ?
    """
    cursor.execute(query, (date,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_tracklist(cursor, playlist_id):
    query = """
    SELECT l.artist, l.title
    FROM library l
    JOIN PlaylistTracks pt ON l.id = pt.track_id
    WHERE pt.playlist_id = ?
    ORDER BY pt.position;
    """
    cursor.execute(query, (playlist_id,))
    return cursor.fetchall()

def export_tracklist(date, tracks):
    filename = f"tracklist_{date}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Tracklist:\n")
        for artist, title in tracks:
            f.write(f"{artist} - {title}\n")
    print(f"Tracklist saved as {filename}")

def main():
    default_db_path = os.path.expandvars(r"%USERPROFILE%\Local Settings\Application Data\Mixxx\mixxxdb.sqlite")
    db_path = input(f"Enter the database path (Press Enter to use default: {default_db_path}): ") or default_db_path

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    date_input = input("Enter the set date (YYYY-MM-DD): ")
    try:
        datetime.datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return
    
    playlist_id = get_playlist_id(cursor, date_input)
    if not playlist_id:
        print("No playlist found for this date.")
        return
    
    tracks = get_tracklist(cursor, playlist_id)
    if not tracks:
        print("No tracks found for this playlist.")
        return
    
    export_tracklist(date_input, tracks)
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
