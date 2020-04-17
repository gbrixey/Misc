#!/usr/bin/env python3
import os
import jwt
import datetime
import requests
import sqlite3

# URL of the Ambient Essentials playlist
URL = 'https://api.music.apple.com/v1/catalog/us/playlists/pl.472dc0c5efe548bb9846e484378aa47b'
# Date format used in the Apple Music JSON
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
KEY_ID = os.environ['PM_KEY_ID']
TEAM_ID = os.environ['PM_TEAM_ID']
DATABASE = 'ambient_essentials.db'
BOLD = '\033[1m'
UNBOLD = '\033[0m'

def jwt_token():
    '''Creates a JWT token from the p8 file stored in the current directory. This function expects
    the p8 filename to be in the default format AuthKey_TEAM.p8 where TEAM is the team ID provided by Apple.'''
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
    '''Creates the playlist tracks table in the given database if it doesn't already exist.'''
    sql_create_table = '''
        create table if not exists tracks (
            track_id integer primary key,
            artist text,
            name text,
            versions text,
            last_index integer
        );
    '''
    db.cursor().execute(sql_create_table)

def update_entry(db, track_id, artist, name, current_date, index):
    '''Updates the database with the given parameters. If a row with a matching track_id already exists
    in the database, this function updates the artist, name, versions, and last_index columns for that row.
    Otherwise it inserts a new row.'''
    sql_upsert = '''
        insert into tracks (track_id, artist, name, versions, last_index) values (?, ?, ?, ?, ?)
            on conflict(track_id) do update set
                artist = excluded.artist,
                name = excluded.name,
                versions = tracks.versions || ',' || excluded.versions,
                last_index = excluded.last_index
            where instr(tracks.versions, excluded.versions) = 0;
    '''
    db.cursor().execute(sql_upsert, (track_id, artist, name, current_date, index))

def parse_date(date_string):
    '''Parse a date string to a datetime object, using the format found in the Apple Music JSON.'''
    return datetime.datetime.strptime(date_string, DATE_FORMAT)

def format_date(date):
    '''Format a datetime object as a string, using the format found in the Apple Music JSON.'''
    return datetime.datetime.strftime(date, DATE_FORMAT)

def get_playlist_tracks_from_database():
    '''Gets all tracks from the database.'''
    db = sqlite3.connect(DATABASE)
    ensure_table(db)
    sql_fetch = '''select * from tracks order by track_id desc'''
    tracks = db.cursor().execute(sql_fetch).fetchall()
    db.close()
    return tracks

def fetch_playlist_from_web():
    '''Fetches the Ambient Essentials playlist from the internet and returns the result in JSON format.'''
    token = jwt_token()
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    response = requests.get(URL, headers = headers)
    playlist = response.json()['data'][0]
    return playlist

def update_tracks_database():
    '''Fetches the Ambient Essentials playlist from the internet and updates the tracks in the database.'''
    db = sqlite3.connect(DATABASE)
    ensure_table(db)
    playlist = fetch_playlist_from_web()
    last_modified = playlist['attributes']['lastModifiedDate']
    tracks = playlist['relationships']['tracks']['data']
    for (index, track) in enumerate(tracks):
        track_id = track['id']
        artist = track['attributes']['artistName']
        name = track['attributes']['name']
        update_entry(db, track_id, artist, name, last_modified, index)
    db.commit()
    db.close()

def print_current_playlist():
    '''Prints all tracks currently on the playlist, based on the values in the tracks database table.
    The tracks added to the playlist in the latest update are highlighted.'''
    tracks = get_playlist_tracks_from_database()
    # Parse all the date strings in the database to figure out the date of the most recent version of the playlist.
    version_strings = ','.join([track[3] for track in tracks])
    version_dates = [parse_date(version_string) for version_string in version_strings.split(',')]
    deduped_version_dates = list(set(version_dates))
    sorted_version_dates = sorted(deduped_version_dates)
    latest_date = sorted_version_dates[-1]
    latest_date_string = format_date(latest_date)
    # The second most recent date is used to determine if a track was re-added to the playlist after being removed earlier.
    second_latest_date_string = None
    if len(sorted_version_dates) > 1:
        second_latest_date_string = format_date(sorted_version_dates[-2])
    # Current tracks will have the most recent date in the versions string.
    current_tracks = [track for (index, track) in enumerate(tracks) if latest_date_string in track[3]]
    # Sort tracks by playlist order
    current_tracks = sorted(current_tracks, key = lambda track: track[4])
    max_artist_name_length = max([len(track[1]) for track in current_tracks])
    # Print a header
    print('{0}\nAMBIENT ESSENTIALS PLAYLIST{1}'.format(BOLD, UNBOLD))
    print('Updated {0}\n'.format(datetime.datetime.strftime(latest_date, '%d %B %Y')))
    # Then print all the tracks in the playlist
    for track in current_tracks:
        # The track is brand-new if it only has one date in the versions string (i.e. the most recent date)
        is_new = len(track[3].split(',')) == 1
        is_readded = not is_new and second_latest_date_string != None and second_latest_date_string not in track[3]
        pre_prefix = BOLD if is_new else ''
        prefix = 'NEW' if is_new else 'RE-ADDED' if is_readded else ''
        suffix = UNBOLD if is_new else ''
        length = max_artist_name_length + 2
        print('{0}{1:10}{2:{length}}{3}{4}'.format(pre_prefix, prefix, track[1], track[2], suffix, length = length))

if __name__ == "__main__":
    update_tracks_database()
    print_current_playlist()
