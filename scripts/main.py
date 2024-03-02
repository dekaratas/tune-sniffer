import os
import json
import time
import sys
import subprocess
from dotenv import load_dotenv
from spotify_create_playlist import search_tracks, create_playlist_and_add_tracks, start_playing_playlist

# Load environmental variables from .env file
load_dotenv()

def generate_tracks_json(style="prog+rock"):
    try:
        subprocess.run(["python", "discogs.py", style], check=True, timeout=7)
        print("Tracks JSON file generated successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error while generating tracks JSON: {e}")
    except subprocess.TimeoutExpired:
        print("discogs.py script finished executing")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_playlist_from_json():
    try:
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tracks.json')
        with open(data_path, 'r') as file:
            data = json.load(file)
        if not data:
            print("No data received")
            return

        tracks_uris = search_tracks(data)
        if not tracks_uris:
            print("No tracks found on Spotify")
            return

        playlist_id = create_playlist_and_add_tracks(tracks_uris)
        print("Playlist ID: ", playlist_id)
        time.sleep(7)
        start_playing_playlist(playlist_id)

        print("Playlist created and started playing")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    style = "prog+rock"
    if len(sys.argv) > 1:
        style = sys.argv[1]
    generate_tracks_json(style)
    create_playlist_from_json()