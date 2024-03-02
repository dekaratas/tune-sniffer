import os
import spotipy
import time
import threading
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
from dotenv import load_dotenv

#* Loading environmental variable from .env file
load_dotenv()

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = os.getenv('SPOTIFY_SECRET_KEY')

#* Check whether track is already in "Your Music"
def is_track_saved(track_uri):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri="http://localhost:5000/callback",
            scope='user-library-read playlist-modify-public playlist-modify-private user-modify-playback-state user-read-playback-state'
        ))
        saved_status = sp.current_user_saved_tracks_contains(tracks=[track_uri])[0]
        return saved_status
    except Exception as e:
        print(f"Error checking saved track: {e}")
        return False

#* Skip to next song and count down time
def fn_skip_to_next_song():
    while True:
        try:
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                redirect_uri="http://localhost:5000/callback",
                scope='user-library-read playlist-modify-public playlist-modify-private user-modify-playback-state user-read-playback-state'
            ))
            sp.next_track()
            print("Song skipped")
            current_playback = sp.current_playback()
            saved_status = is_track_saved(current_playback['item']['uri'])
            if saved_status:
                print("Track is saved")
            else:
                print("Track is not saved")
            print()
            print(current_playback['item']['name'])
            for i in range(5, 0, -1):
                print(f"Skipping song in {i} seconds...", end="\r")
                time.sleep(1)
        except Exception as e:
            print(f"Couldn't skip song: {e}")
            time.sleep(5)
            continue

#* Start thread on script execution
if __name__ == "__main__":
    print("Thread started")
    skip_thread = threading.Thread(target=fn_skip_to_next_song)
    skip_thread.daemon = True
    skip_thread.start()

app.run(port=5001)