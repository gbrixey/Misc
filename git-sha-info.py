#!/usr/bin/env python
import argparse
import subprocess
from collections import defaultdict

def analyze_digit_frequency(sha_list):
    '''Calculates how many times each hex digit appears in the given
    list of commit hashes.'''
    frequency_dict = defaultdict(int)
    for sha in sha_list:
        for digit in sha:
            frequency_dict[digit] += 1
    sum_digits = float(sum(frequency_dict.values()))
    print('Digit   Occurrences   Frequency')
    print('-----   -----------   ---------')
    for digit, occurrences in sorted(frequency_dict.items(), key=lambda t: (t[1], t[0])):
        percent = (occurrences / sum_digits) * 100
        print('{0}       {1}   {2:.3f} %'.format(digit, str(occurrences).ljust(11), percent))
    print('\nTotal digits: {0}'.format(int(sum_digits)))

def find_longest_letter_string_in_list(string_list):
    '''Finds the longest substring of consecutive alphabetical
    characters in the given list of strings.'''
    longest_letter_string_list = []
    for string in string_list:
        longest_letter_string_list.append(find_longest_letter_string(string))
    longest_letter_string_length = 0
    for longest_letter_string in longest_letter_string_list:
        if len(longest_letter_string) > longest_letter_string_length:
            longest_letter_string_length = len(longest_letter_string)
    print('The longest string of only letters is {0} letters long:'.format(longest_letter_string_length))
    for (index, longest_letter_string) in enumerate(longest_letter_string_list):
        if len(longest_letter_string) == longest_letter_string_length:
            print('{0}, in {1}'.format(longest_letter_string, string_list[index]))

def find_longest_letter_string(string):
    '''Finds the longest substring of consecutive alphabetical
    characters in the given string.'''
    start_pos = 0
    max_length = 0
    current_length = 0
    for i in range(0, len(string) + 1):
        if i < len(string) and string[i].isalpha():
            current_length += 1
        else:
            if current_length > max_length:
                max_length = current_length
                start_pos = i - current_length
            current_length = 0
    if max_length > 0:
        return string[start_pos:start_pos + max_length]
    else:
        return ''

def find_longest_repeating_char_in_list(string_list):
    '''Finds the longest substring of consecutive repeated characters
    in the given list of strings.'''
    longest_repeating_char_list = []
    for string in string_list:
        longest_repeating_char_list.append(find_longest_repeating_char(string))
    longest_repeating_char_length = 0
    for longest_repeating_char in longest_repeating_char_list:
        if len(longest_repeating_char) > longest_repeating_char_length:
            longest_repeating_char_length = len(longest_repeating_char)
    print('The longest sequence of repeated digits is {0} digits long:'.format(longest_repeating_char_length))
    for (index, longest_repeating_char) in enumerate(longest_repeating_char_list):
        if len(longest_repeating_char) == longest_repeating_char_length:
            print('{0}, in {1}'.format(longest_repeating_char, string_list[index]))

def find_longest_repeating_char(string):
    '''Finds the longest substring of consecutive repeated characters
    in the given string.'''
    i = 0
    sub_string = string[1]
    longest_repeating_char = ''
    while i < len(string) - 1:
        if string[i] == string[i + 1]:
            sub_string += string[i + 1]
        else:
            if len(sub_string) > len(longest_repeating_char):
                longest_repeating_char = sub_string
            sub_string = string[i + 1]
        i += 1
    return longest_repeating_char

def find_word(sha_list, word):
    '''Finds all commit hashes in the given list that contain the given word.'''
    valid_word = validate_word(word)
    word_sha_list = []
    if valid_word:
        for sha in sha_list:
            if word.lower() in sha:
                word_sha_list.append(sha)
    s = 's' if len(word_sha_list) == 1 else ''
    print('{0} of your commit hashes contain{1} {2}'.format(len(word_sha_list), s, word.lower()))
    for word_sha in word_sha_list[:10]:
        print(word_sha)
    if len(word_sha_list) > 10:
        print('...Just to name a few.')
        
def validate_word(word):
    '''Checks if the given word is a valid hex word that could appear
    in a commit hash.'''
    # Empty string or whitespace-only string is handled in main()
    if len(word) > 40:
        return False
    for character in word:
        if character not in '0123456789abcdef':
            return False
    return True

def get_sha_list(path):
    '''Returns a list of the git commit hashes in the given directory
    in the form of string representations of base-16 numbers.'''
    pop = subprocess.Popen(['git', '-C', path, 'log', '--pretty=format:"%H"', '--encoding=UTF-8'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = pop.communicate()
    if error:
        error = decode_bytes_if_necessary(error)
        print(error)
        return []
    output = decode_bytes_if_necessary(output)
    sha_list = []
    for line in output.split('\n'):
        sha_list.append(line.strip('"'))
    return sha_list
    
def decode_bytes_if_necessary(string_or_bytes):
    '''If the given parameter is of type bytes, this method will decode it
    using utf-8 encoding and return a string.'''
    # In Python 3, Popen returns output as bytes. In Python 2 it returns a str.
    # In Python 2 it seems like str and bytes are the same type.
    if type(string_or_bytes) is bytes and not type(string_or_bytes) is str:
        return string_or_bytes.decode('utf-8')
    else:
        return string_or_bytes
    
def create_parser():
    '''Creates and returns the argument parser for this script.'''
    parser = argparse.ArgumentParser(description='Prints interesting facts about the SHA-1 commit hashes in a git repository.\nWill print some default facts if no options are specified.', usage='%(prog)s [-dhlr] [-p PATH] [-w WORD]')
    parser.add_argument('-p', '--path', dest='path', default='.', type=str, help='Path to the git repository to use. Defaults to the current directory.')
    parser.add_argument('-w', '--word', dest='word', default=None, type=str, help='Word to search for in the commit hashes.')
    parser.add_argument('-r', dest='find_repeating', action='store_const', default=False, const=True, help='Find the longest string of repeating characters.')
    parser.add_argument('-l', dest='letters', action='store_const', default=False, const=True, help='Find the longest string of only letters.')
    parser.add_argument('-d', '--digits', dest='digits', action='store_const', default=False, const=True, help='Analyze digit frequency.')
    return parser
    
def main():
    parser = create_parser()
    args = parser.parse_args()
    path = args.path
    sha_list = get_sha_list(path)
    if len(sha_list) > 0:
        print(' ')
        default = True
        word = args.word
        if word and len(word) > 0 and not word.isspace():
            find_word(sha_list, word)
            default = False
        if args.find_repeating:
            find_longest_repeating_char_in_list(sha_list)
            default = False
        if args.letters:
            find_longest_letter_string_in_list(sha_list)
            default = False
        if args.digits:
            analyze_digit_frequency(sha_list)
            default = False
        if default:
            find_word(sha_list, 'beef')
            print(' ')
            find_longest_repeating_char_in_list(sha_list)

if __name__ == '__main__':
    main()
