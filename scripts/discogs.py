import os
import sys
import threading
from flask import Flask, jsonify
import requests
import random
import json

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def get_random_prog_tracks():
    style = "prog+rock"
    if len(sys.argv) > 1:
        style = sys.argv[1]

    discogs_url = "https://api.discogs.com/database/search"

    params = {
        "style": style,
        "page": random.randint(1, 100),
        "per_page": 10,
        "key": os.getenv('DISCOGS_SECRET_KEY'),
        "secret": os.getenv('DISCOGS_CLIENT_SECRET')
    }

    try:
        # Make API request
        response = requests.get(discogs_url, params=params)
        response.raise_for_status() # Raise an error IF there is one

        # Extract release IDs from response
        release_ids = [result['master_id'] for result in response.json()['results']]

        # Randomly select 10 release IDs
        random_release_ids = random.sample(release_ids, min(10, len(release_ids)))

        # List to store the track information
        random_tracks = []

        # Iterate over selected release IDs
        for release_id in random_release_ids:
            # Discogs API URL for retrieving tracklist of a release
            tracklist_url = f"https://api.discogs.com/masters/{release_id}"

            # Make request to get the tracklist
            tracklist_response = requests.get(tracklist_url)
            tracklist_response.raise_for_status() # Raise an error IF there is one

            # Extract a random track from the tracklist
            tracklist = tracklist_response.json()['tracklist']
            random_track = random.choice(tracklist)

            # Extract artist name from tracklist response
            artist_name = tracklist_response.json()['artists'][0]['name']

            # Append track information to the list
            random_tracks.append({
                'title': random_track['title'],
                'artist': artist_name
            })

        # Save the JSON data to a local file
        with open('../data/tracks.json', 'w') as f:
            json.dump(random_tracks, f)

        print("Tracks fetched and saved to JSON file")
    except requests.RequestException as e:
        print(f"Error: {e}")

def run_function_in_thread():
    thread = threading.Thread(target=get_random_prog_tracks)
    thread.start()

if __name__ == '__main__':
    run_function_in_thread()
    app.run()
