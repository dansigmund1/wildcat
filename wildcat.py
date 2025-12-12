import spotipy
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8080/callback",
    scope="user-read-playback-state user-modify-playback-state"
))

user = sp.current_user()
print("Logged in as:", user["display_name"])