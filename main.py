from bs4 import BeautifulSoup
import requests
import spotipy
client_id = "0ddb3a2303f044f8953c7481353eb812"
client_secret = "bf9691f7ef4745f98a668ddf28e1be04"
re_uri ="http://example.com"


from spotipy.oauth2 import SpotifyOAuth
#TODO Authentication in spotify
#  inorder to access a user account, we need get access token so follow the steps:
#  In developer spotify dashboard, create an app called billborad to spotify
#  in client details, we get clientid, secret
#  now import spotipy module which support spotify developing
#  Create a spotipy object
#  auth_manager is an object of spotifyOAuth class
#  auth_manager need parameters like client_id, client_secret, redirect_uri, scope, show_Dialog, cache_path
#  To get current user id
#  run the code
#  redirected to agree the terms and then to redirect URI, copy the link
#  in pycharm, paste the link to the prompt auto-created
#  with no error, token.txt generated

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=re_uri,
                                               scope= "playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               ))


user_id = sp.current_user()['id']
print(user_id)
# id = pwusk2lg2mj9t7lg54sksk8ot

from pprint import pprint
date_input = input("which year you want the playlist in format YYYY-MM-DD: " )
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date_input}/")
music_data = response.text

soup=BeautifulSoup(music_data, "html.parser")

songs = [song.getText().strip() for song in soup.select(selector="ul li #title-of-a-story")]
print(len(songs))
print(songs)
# TODO - 2 To search 100 songs in spotify using search method
#  we need to give query and try if uri is a NOne if so except print value is printed
songs_uri=[]
for song in songs:
    search = sp.search(q=f"track:{song}year:{date_input.split('-')[0]}")
    # pprint(search)
    try:
        uri = search["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f"The {song} is not available in spotify so skipped")

print(songs_uri)

# TODO -3 create a new playlist and to add songs
new_playlist = sp.user_playlist_create(user=user_id, name=f"{date_input} Billboard 100", public=False, description="College memories")
playlist_id = new_playlist['id']
print(playlist_id)
add_items = sp.playlist_add_items(playlist_id, items=songs_uri, position=None)
cover = sp.playlist_cover_image(playlist_id)
playlist_id="11EwlBK5HuKOba7Sto9uyW"
playlist_items = sp.playlist_items(playlist_id)
print(playlist_items)