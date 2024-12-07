# bot/spotify_integration.py

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

class SpotifyClient:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify credentials not found in environment variables.")

        self.client_credentials_manager = SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    def search_tracks(self, query, limit=10):
        results = self.sp.search(q=query, type='track', limit=limit)
        tracks = results['tracks']['items']
        return tracks

    def get_track(self, query):
        results = self.sp.search(q=query, type='track', limit=1)
        tracks = results['tracks']['items']
        if tracks:
            track = tracks[0]
            return {
                'id': track['id'],
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'preview_url': track['preview_url']  # 30-second preview
            }
        return None
