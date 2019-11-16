#!/usr/bin/env python3
import os
import jwt
import datetime
import requests
import sqlite3

# URL of the Ambient Essentials playlist
URL = 'https://api.music.apple.com/v1/catalog/us/playlists/pl.472dc0c5efe548bb9846e484378aa47b'
KEY_ID = os.environ['PM_KEY_ID']
TEAM_ID = os.environ['PM_TEAM_ID']
DATABASE = 'ambient_essentials.db'

def jwt_token():
    # Using the default p8 file name
    with open('AuthKey_{0}.p8'.format(KEY_ID)) as key_file:
        key = key_file.read()
    iat = datetime.datetime.utcnow()
    exp = iat + datetime.timedelta(seconds = 30)
    headers = {'alg': 'ES256', 'kid': KEY_ID}
    payload = {'iss': TEAM_ID, 'iat': iat, 'exp': exp}
    byte_token = jwt.encode(payload, key, algorithm = 'ES256', headers = headers)
    token = byte_token.decode('utf-8')
    return token

def ensure_table(db):
    sql_create_table = '''
        create table if not exists tracks (
            track_id integer primary key,
            artist text,
            name text,
            last_seen text
        );
    '''
    db.cursor().execute(sql_create_table)

def update_entry(db, track_id, artist, name, date_string):
    sql_upsert = '''
        insert into tracks (track_id, artist, name, last_seen) values (?, ?, ?, ?)
            on conflict(track_id) do update set
                artist = excluded.artist,
                name = excluded.name,
                last_seen = excluded.last_seen;
    '''
    db.cursor().execute(sql_upsert, (track_id, artist, name, date_string))

def fetch_playlist():
    token = jwt_token()
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    response = requests.get(URL, headers = headers)
    playlist = response.json()['data'][0]
    return playlist

def update_tracks():
    db = sqlite3.connect(DATABASE)
    ensure_table(db)
    playlist = fetch_playlist()
    last_modified = playlist['attributes']['lastModifiedDate']
    tracks = playlist['relationships']['tracks']['data']
    for track in tracks:
        track_id = track['id']
        artist = track['attributes']['artistName']
        name = track['attributes']['name']
        update_entry(db, track_id, artist, name, last_modified)
    db.commit()
    db.close()

if __name__ == "__main__":
    update_tracks()
