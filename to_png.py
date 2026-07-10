#!/usr/bin/env python
import os
import glob
import argparse
from PIL import Image

def to_png(filenames):
    '''Converts the given image files to PNG format.'''
    # Expand wildcards
    expanded_filenames = []
    for filename in filenames:
        expanded_filenames += glob.glob(filename)
    for filename in expanded_filenames:
        name, extension = os.path.splitext(filename)
        new_filename = name + '.png'
        image = Image.open(filename)
        image.save(new_filename, 'PNG')
        print(f'Created {new_filename}')

def create_parser():
    '''Creates and returns the argument parser for this script.'''
    parser = argparse.ArgumentParser(description='Converts image files to PNG format.')
    parser.add_argument('filenames', type=str, nargs='*', help='The image files to convert to PNG.')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    to_png(args.filenames)

if __name__ == '__main__':
    main()
