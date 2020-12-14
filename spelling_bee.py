#!/usr/bin/env python
import argparse

MINIMUM_WORD_LENGTH = 4

def solve(available_letters, required_letter):
    '''Prints a list of solutions to the New York Times Spelling Bee game
    with the given available letters and required letter.'''
    with open('spelling_bee_words.txt') as words_file:
        words = words_file.read().split()
    solutions = []
    for word in words:
        if check_word(word, available_letters, required_letter):
            solutions.append(word)
    # Sort the solutions by length first, then alphabetically
    solutions.sort()
    solutions.sort(key = len, reverse = True)
    
    print('\nSpelling Bee solutions for letters \'{0}\' and required letter \'{1}\':\n'.format(available_letters, required_letter))
    for solution in solutions:
        print(solution)
    
def check_word(word, available_letters, required_letter):
    '''Checks a single word to see if it is a valid solution to the Spelling Bee game
    with the given available letters and required letter.'''
    if len(word) < MINIMUM_WORD_LENGTH:
        return False
    if required_letter not in word:
        return False
    for character in word:
        if character not in available_letters:
            return False
    return True

def create_parser():
    '''Creates and returns the argument parser for this script.'''
    parser = argparse.ArgumentParser(description='Provides solutions to the New York Times Spelling Bee game.')
    parser.add_argument('available_letters', type=str, help='The seven available letters used to form words.')
    parser.add_argument('required_letter', type=str, help='The required letter that each word must contain.')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    available_letters = args.available_letters
    required_letter = args.required_letter
    solve(available_letters, required_letter)

if __name__ == '__main__':
    main()