import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# ----------------------------------------Auth Process & Variables-----------------------------------------------------
# Create environment Variables SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user_id = sp.current_user()["id"]
date = input("Which year do you want to travel back to? Format: YYYY-MM-DD")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"


# ----------------------------------------------Web scrapping----------------------------------------------------------
response = requests.get(URL)
website_data = response.text
soup = BeautifulSoup(website_data, "html.parser")
song_names = soup.select(selector="li h3", class_="c-title")
list_of_song_names = []
for song in song_names:
    text = song.getText().strip()
    list_of_song_names.append(text)
del list_of_song_names[-7:]


# ------------------------------------------Locating songs in Spotify---------------------------------------------------
song_uris = []
year = date.split("-")[0]
for song in list_of_song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


# -------------------------------------------Playlist Creation---------------------------------------------------------
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
playlist_id = playlist["id"]

sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
