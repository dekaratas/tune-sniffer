import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Function to search for tracks on Spotify
def search_tracks(track_list):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri="http://localhost:5001/callback",
        scope='playlist-modify-public playlist-modify-private user-modify-playback-state user-read-playback-state'
    ))

    tracks_uris = []
    for track in track_list:
        query = f"{track['title']} artist:{track['artist']}"
        result = sp.search(query, limit=1, type='track')
        if result['tracks']['items']:
            tracks_uris.append(result['tracks']['items'][0]['uri'])
    return tracks_uris
    
# Function to create a new playlist and add tracks to it
def create_playlist_and_add_tracks(tracks_uris):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri="http://localhost:5001/callback",
        scope='playlist-modify-public playlist-modify-private user-modify-playback-state user-read-playback-state'
    ))

    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, 'My New Playlist')
    playlist_id = playlist['id']

    sp.playlist_add_items(playlist_id, tracks_uris)

    return playlist_id

# Function to start playing the created playlist
def start_playing_playlist(playlist_id):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri="http://localhost:5001/callback",
        scope='user-modify-playback-state user-read-playback-state'
    ))

    sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")