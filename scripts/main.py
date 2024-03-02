import os
import json
import time
from dotenv import load_dotenv
from spotify_create_playlist import search_tracks, create_playlist_and_add_tracks, start_playing_playlist

# Load environmental variables from .env file
load_dotenv()

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
        time.sleep(5)
        start_playing_playlist(playlist_id)

        print("Playlist created and started playing")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    create_playlist_from_json()