#!/usr/bin/env python
import os
import glob
import argparse
from PIL import Image
from pillow_heif import register_heif_opener

def to_jpeg(filenames):
    '''Converts the given image files to JPEG format.'''
    register_heif_opener()
    # Expand wildcards
    expanded_filenames = []
    for filename in filenames:
        expanded_filenames += glob.glob(filename)
    for filename in expanded_filenames:
        name, extension = os.path.splitext(filename)
        image = Image.open(filename)
        image.save(name + '.jpeg', "JPEG")

def create_parser():
    '''Creates and returns the argument parser for this script.'''
    parser = argparse.ArgumentParser(description='Converts image files to JPEG format.')
    parser.add_argument('filenames', type=str, nargs='*', help='The image files to convert to JPEG.')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    to_jpeg(args.filenames)

if __name__ == '__main__':
    main()
