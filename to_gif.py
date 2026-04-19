#!/usr/bin/env python
import os
import glob
import argparse
from PIL import Image

def to_gif(filenames):
    '''Converts the given image files to GIF format.'''
    # Expand wildcards
    expanded_filenames = []
    for filename in filenames:
        expanded_filenames += glob.glob(filename)
    for filename in expanded_filenames:
        name, extension = os.path.splitext(filename)
        new_filename = name + '.gif'
        image = Image.open(filename)
        image.save(new_filename, "GIF", save_all = True)
        print(f'Created {new_filename}')

def create_parser():
    '''Creates and returns the argument parser for this script.'''
    parser = argparse.ArgumentParser(description='Converts image files to GIF format.')
    parser.add_argument('filenames', type=str, nargs='*', help='The image files to convert to GIF.')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    to_gif(args.filenames)

if __name__ == '__main__':
    main()
