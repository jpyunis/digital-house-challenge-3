import os
import sys
import json
import spotipy
from json.decoder import JSONDecodeError
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
username = config.get('SPOTIFY', 'username')
scope = config.get('SPOTIFY', 'scope')


def spotify():
    print('\n')
    print(f' SPOTIFY '.center(80, '*'))
    try:
        token = spotipy.util.prompt_for_user_token(username, scope)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = spotipy.util.prompt_for_user_token(username, scope)

    # Create Spotify object
    spotifyObject = spotipy.Spotify(auth=token)