#!/usr/bin/env python3
import os
import jwt
import datetime
import requests
import sqlite3
import argparse
import textwrap

PLAYLIST_NAME = {
    1: 'Ambient Essentials',
    2: 'Pure Focus'
}
PLAYLIST_URL = {
    1: 'https://api.music.apple.com/v1/catalog/us/playlists/pl.472dc0c5efe548bb9846e484378aa47b',
    2: 'https://api.music.apple.com/v1/catalog/us/playlists/pl.dbd712beded846dca273d5d3259d28aa'
}
# Date format used in the Apple Music JSON
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
NICE_DATE_FORMAT = '%d %B %Y'
KEY_ID = os.environ['PM_KEY_ID']
TEAM_ID = os.environ['PM_TEAM_ID']
BOLD = '\033[1m'
UNBOLD = '\033[0m'

def snake_case(string):
    return string.lower().replace(' ', '_')

def filename(key, extension):
    playlist_name = PLAYLIST_NAME[key]
    return '{0}.{1}'.format(snake_case(playlist_name), extension)

def database(key):
    return filename(key, 'db')

def csv_filename(key):
    return filename(key, 'csv')

def jwt_token():
    '''Creates a JWT token from the p8 file stored in the current directory. This function expects
    the p8 filename to be in the default format AuthKey_TEAM.p8 where TEAM is the team ID provided by Apple.'''
    with open('AuthKey_{0}.p8'.format(KEY_ID)) as key_file:
        key = key_file.read()
    iat = datetime.datetime.now(datetime.UTC)
    exp = iat + datetime.timedelta(seconds = 30)
    headers = {'alg': 'ES256', 'kid': KEY_ID}
    payload = {'iss': TEAM_ID, 'iat': iat, 'exp': exp}
    token = jwt.encode(payload, key, algorithm = 'ES256', headers = headers)
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

def format_date(date, nice = False):
    '''Format a datetime object as a string, using the format found in the Apple Music JSON.'''
    date_format = NICE_DATE_FORMAT if nice else DATE_FORMAT
    return datetime.datetime.strftime(date, date_format)

def get_playlist_tracks_from_database(key):
    '''Gets all tracks from the database.'''
    db = sqlite3.connect(database(key))
    ensure_table(db)
    sql_fetch = '''select * from tracks order by track_id desc'''
    tracks = db.cursor().execute(sql_fetch).fetchall()
    db.close()
    return tracks

def fetch_playlist_from_web(key):
    '''Fetches the playlist from the internet and returns the result in JSON format.'''
    token = jwt_token()
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    response = requests.get(PLAYLIST_URL[key], headers = headers)
    playlist = response.json()['data'][0]
    return playlist

def update_tracks_database(key):
    '''Fetches the playlist from the internet and updates the tracks in the database.'''
    db = sqlite3.connect(database(key))
    ensure_table(db)
    playlist = fetch_playlist_from_web(key)
    last_modified = playlist['attributes']['lastModifiedDate']
    tracks = playlist['relationships']['tracks']['data']
    for (index, track) in enumerate(tracks):
        track_id = track['id']
        artist = track['attributes']['artistName']
        name = track['attributes']['name']
        update_entry(db, track_id, artist, name, last_modified, index)
    db.commit()
    db.close()

def playlist_update_dates(key):
    '''Returns a list of dates the playlist was updated, based on the data in the database.'''
    tracks = get_playlist_tracks_from_database(key)
    all_date_strings = ','.join([track[3] for track in tracks]).split(',')
    return sorted(list(set(all_date_strings)))

def print_current_playlist(key, show_removed):
    '''Prints all tracks currently on the playlist, based on the values in the tracks database table.
    The tracks added to the playlist in the latest update are highlighted.'''
    tracks = get_playlist_tracks_from_database(key)
    # Parse all the date strings in the database to figure out the date of the most recent version of the playlist.
    date_strings = playlist_update_dates(key)
    latest_date_string = date_strings[-1]
    latest_date = parse_date(latest_date_string)
    # The second most recent date is used to determine if a track was re-added to the playlist after being removed earlier.
    second_latest_date_string = 'NONE'
    if len(date_strings) > 1:
        second_latest_date_string = date_strings[-2]
    # Current tracks will have the most recent date in the versions string.
    current_tracks = [track for (index, track) in enumerate(tracks) if latest_date_string in track[3]]
    # Sort tracks by playlist order
    current_tracks = sorted(current_tracks, key = lambda track: track[4])
    max_artist_name_length = max([len(track[1]) for track in current_tracks])
    # Print a header
    print('{0}\n{1} PLAYLIST{2}'.format(BOLD, PLAYLIST_NAME[key].upper(), UNBOLD))
    print('Updated {0}\n'.format(format_date(latest_date, nice = True)))
    # Then print all the tracks in the playlist
    for track in current_tracks:
        # The track is brand-new if it only has one date in the versions string (i.e. the most recent date)
        is_new = len(track[3].split(',')) == 1
        is_readded = not is_new and second_latest_date_string not in track[3]
        print_track(track, max_artist_name_length, is_new = is_new, is_readded = is_readded)
    # Then print the tracks that were removed
    if show_removed:
        was_removed = lambda track: second_latest_date_string in track[3] and latest_date_string not in track[3]
        removed_tracks = [track for (index, track) in enumerate(tracks) if was_removed(track)]
        removed_title = 'REMOVED:' if len(removed_tracks) > 0 else 'NO TRACKS WERE REMOVED.\n'
        print('\n{0}{1}{2}'.format(BOLD, removed_title, UNBOLD))
        for track in removed_tracks:
            print_track(track, max_artist_name_length)

def print_track(track, max_artist_name_length, is_new = False, is_readded = False):
    pre_prefix = BOLD if is_new else ''
    prefix = 'NEW' if is_new else 'RE-ADDED' if is_readded else ''
    suffix = UNBOLD if is_new else ''
    length = max_artist_name_length + 2
    print('{0}{1:10}{2:{length}}{3}{4}'.format(pre_prefix, prefix, track[1], track[2], suffix, length = length))

def export_csv(key):
    '''Saves a CSV file with all tracks in the database and the dates of their inclusion in the playlist.'''
    tracks = get_playlist_tracks_from_database(key)
    date_strings = playlist_update_dates(key)
    update_dates = [parse_date(ds) for ds in date_strings]
    # Create headers for the CSV columns
    header_line_components = ['Track ID', 'Artist', 'Song Title']
    header_line_components.extend([format_date(ud, nice = True) for ud in update_dates])
    header_line = ','.join(header_line_components)
    csv_lines = [header_line]
    for track in tracks:
        quoted_artist = '"{0}"'.format(track[1])
        quoted_song_title = '"{0}"'.format(track[2])
        components = [str(track[0]), quoted_artist, quoted_song_title]
        components.extend([('TRUE' if ds in track[3] else 'FALSE') for ds in date_strings])
        csv_lines.append(','.join(components))
    with open(csv_filename(key), 'w') as csv_file:
        csv_file.write('\n'.join(csv_lines))
    print('Wrote {0} lines'.format(len(csv_lines)))

def create_parser():
    '''Creates and returns the argument parser for this script.'''
    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = textwrap.dedent('''\
            Monitor a playlist. Pass in a key to select the playlist:
              1 - Ambient Essentials (default)
              2 - Pure Focus
            '''))
    parser.add_argument(
        '-k',
        dest = 'key',
        default = 1,
        type = int,
        help = 'Key that determines which playlist to monitor.'
        )
    parser.add_argument(
        '--show-removed',
        action = 'store_true',
        help = 'Show tracks that were removed from the playlist in the latest update.'
        )
    parser.add_argument(
        '--export',
        action = 'store_true',
        help = 'Export data to a CSV instead of printing to console.'
        )
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    key = args.key
    update_tracks_database(key)
    if args.export:
        export_csv(key)
    else:
        print_current_playlist(key, args.show_removed)

if __name__ == "__main__":
    main()
