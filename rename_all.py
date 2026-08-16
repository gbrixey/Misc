#!/usr/bin/env python
import argparse
from pathlib import Path

def rename_all(prefix):
    '''Rename all files in the current directory.
    The new filename for each file is created by appending an integer to the given prefix 
    such that the files remain in the same alphabetical order that they were in before being renamed.'''
    files = sorted([f for f in Path('.').iterdir() if f.is_file()])
    max_filename_length = max([len(str(file)) for file in files])
    digits = len(str(len(files)))
    old_filenames = []
    new_filenames = []
    for i in range(len(files)):
        file = files[i]
        old_filename = str(file)
        old_filenames.append(old_filename)
        components = old_filename.split('.')
        if len(components) <= 1:
            print(f'Unexpected filename: {old_filename}')
            break
        extension = components[-1]
        file_number = str(i + 1).rjust(digits, '0')
        new_filename = f'{prefix}{file_number}.{extension}'
        new_filenames.append(new_filename)
        # Give all the files a temporary filename first, 
        # in case a file with the new filename already exists in the directory.
        temp_filename = f'RENAME_TEMP{file_number}'
        file.rename(temp_filename)
    files = sorted([f for f in Path('.').iterdir() if f.is_file()])
    for i in range(len(files)):
        old_filename = old_filenames[i]
        new_filename = new_filenames[i]
        files[i].rename(new_filename)
        print(f'Renamed {old_filename.rjust(max_filename_length)} to {new_filename}')
    print(f'Renamed {len(files)} files.')

def create_parser():
    '''Creates and returns the argument parser for this script.'''
    parser = argparse.ArgumentParser(description='Renames all files in the current directory by appending numbers to a given prefix.')
    parser.add_argument('prefix', type=str, help='The prefix to use for the new filenames.')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    rename_all(args.prefix)

if __name__ == '__main__':
    main()
