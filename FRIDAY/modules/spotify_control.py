import os
import sys
sys.path.append(os.path.expanduser("~") + "/FRIDAY")

def get_spotify():
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyOAuth
        from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-modify-playback-state user-read-playback-state user-read-currently-playing"
        ))
        return sp
    except Exception as e:
        return None

def play_song(song_name):
    try:
        sp = get_spotify()
        if not sp:
            return "Spotify not connected"

        results = sp.search(q=song_name, limit=1, type='track')
        tracks = results['tracks']['items']

        if not tracks:
            return f"Song {song_name} not found"

        track = tracks[0]
        sp.start_playback(uris=[track['uri']])
        return f"Playing {track['name']} by {track['artists'][0]['name']}"

    except Exception as e:
        return f"Spotify error: {e}"

def pause_music():
    try:
        sp = get_spotify()
        if not sp:
            return "Spotify not connected"
        sp.pause_playback()
        return "Music paused"
    except Exception as e:
        return f"Error: {e}"

def resume_music():
    try:
        sp = get_spotify()
        if not sp:
            return "Spotify not connected"
        sp.start_playback()
        return "Music resumed"
    except Exception as e:
        return f"Error: {e}"

def next_song():
    try:
        sp = get_spotify()
        if not sp:
            return "Spotify not connected"
        sp.next_track()
        return "Next song"
    except Exception as e:
        return f"Error: {e}"

def previous_song():
    try:
        sp = get_spotify()
        if not sp:
            return "Spotify not connected"
        sp.previous_track()
        return "Previous song"
    except Exception as e:
        return f"Error: {e}"

def current_song():
    try:
        sp = get_spotify()
        if not sp:
            return "Spotify not connected"
        track = sp.current_playback()
        if track and track['is_playing']:
            name = track['item']['name']
            artist = track['item']['artists'][0]['name']
            return f"Playing {name} by {artist}"
        return "Nothing playing right now"
    except Exception as e:
        return f"Error: {e}"

def set_volume(level):
    try:
        sp = get_spotify()
        if not sp:
            return "Spotify not connected"
        sp.volume(level)
        return f"Volume set to {level}"
    except Exception as e:
        return f"Error: {e}"