import discord
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client = 'SPOTIFY_BOT_CLIENT_ID'
secret = 'SPOTIFY_BOT_SECRET'
redirect_url = 'http://localhost:8888/callback'
scope = 'playlist-modify-public, playlist-modify-private'

userID = 'SPOTIFY_USER_ID'
playlistID = "PLAYLIST_URI" # spotify:playlist:someNUMBER

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client, client_secret=secret, scope=scope, redirect_uri=redirect_url))

TOKEN = "DISCORD_BOT_OAUTH_TOKEN"

client = discord.Client()

def addTrackToPlaylist(trackID):
    playlist = sp.user_playlist(userID, playlist_id=playlistID)
    currentTracks = playlist['tracks']['items']
    alreadyInPlaylist = False

    for i in range(0, len(currentTracks)):
        playlistTrackID = currentTracks[i]['track']['uri']
        if trackID == playlistTrackID:
            alreadyInPlaylist = True

    if not alreadyInPlaylist:
        sp.user_playlist_add_tracks(userID, playlist_id=playlistID, tracks=[trackID])

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif 'open.spotify' in message.content:

        if 'track' in message.content:
            trackID = "spotify:track:" + message.content.split("/")[4].split("?")[0]
            addTrackToPlaylist(trackID)
        elif 'album' in message.content:
            albumID = message.content.split("/")[4].split("?")[0]
            albumTracks = sp.album_tracks(album_id=albumID)['items']

            for i in range(0, len(albumTracks)):
                addTrackToPlaylist(albumTracks[i]['uri'])

client.run(TOKEN)
