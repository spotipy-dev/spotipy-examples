# Removes tracks from playlist
import pprint
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

if len(sys.argv) > 2:
    playlist_id = sys.argv[1]
    track_ids = sys.argv[2:]
else:
    print(f"Usage: {sys.argv[0]} playlist_id track_id ...")
    sys.exit()

scope = 'playlist-modify-public'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.playlist_remove_all_occurrences_of_items(
    playlist_id, track_ids)
pprint.pprint(results)
