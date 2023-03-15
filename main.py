import argparse

import spotipy
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyOAuth


def main(num=None, playlist_name=None):
    # Spotify connection
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope="playlist-modify-public user-library-read"))

    try:
        num = num if num is not None else 69
        playlist_name = playlist_name if playlist_name is not None else f"latest {num} liked"

        tracks_dict = sp.current_user_saved_tracks(limit=num)
        tracks = list(map(lambda x: x['track']['id'], tracks_dict['items']))

        playlist_id = get_playlist_id_by_name(sp, playlist_name)
        if playlist_id is None:
            playlist_id = sp.user_playlist_create(sp.me()['id'], playlist_name)['id']

        sp.playlist_replace_items(playlist_id, tracks)
    except SpotifyException:
        print("Error!")


def get_playlist_id_by_name(sp, name):
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == name:
            return playlist['id']
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Latest X Liked',
        description='Stores the latest x liked songs in a playlist'
    )
    parser.add_argument('-c', '--count', required=False)
    parser.add_argument('-n', '--name', required=False)
    args = parser.parse_args()
    main(num=args.count, playlist_name=args.name)
