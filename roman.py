#!/usr/bin/env python
import argparse

def to_roman(number: int) -> str:
    '''Converts the given integer into Roman numerals.'''
    if number < 0:
        print('The Romans did not have a concept of negative numbers.')
        number = abs(number)
    if number == 0:
        print('There is no Roman numeral for zero.')
        return ''
    if number > 3999:
        print('This script only handles numbers up to 3999.')
        return ''
    thousands = number // 1000
    thousands_string = 'M' * thousands
    remainder = number % 1000
    if remainder >= 900:
        hundreds_string = 'CM'
    else:
        hundreds_string = 'D' if remainder >= 500 else ''
        hundreds = (remainder // 100) % 5
        hundreds_string += 'CD' if hundreds == 4 else 'C' * hundreds
    remainder = remainder % 100
    if remainder >= 90:
        tens_string = 'XC'
    else:
        tens_string = 'L' if remainder >= 50 else ''
        tens = (remainder // 10) % 5
        tens_string += 'XL' if tens == 4 else 'X' * tens
    remainder = remainder % 10
    if remainder == 9:
        ones_string = 'IX'
    else:
        ones_string = 'V' if remainder >= 5 else ''
        ones = remainder % 5
        ones_string += 'IV' if ones == 4 else 'I' * ones
    return thousands_string + hundreds_string + tens_string + ones_string

def from_roman(roman: str) -> int:
    '''Converts the given Roman numeral string into an integer.'''
    value_dict = {'M': 1000, 'CM': 900, 'D': 500, 'CD': 400, 'C': 100, 'XC': 90, 'L': 50, 'XL': 40, 'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1}
    check_two_letters = set(['C', 'X', 'I'])
    next_max_value_dict = {'M': 1000, 'CM': 90, 'D': 100, 'CD': 90, 'C': 100, 'XC': 9, 'L': 10, 'XL': 9, 'X': 10, 'IX': 0, 'V': 1, 'IV': 0, 'I': 1} 
    total = 0
    last_value = None
    max_value = 1000
    repeated_same_value = 0
    i = 0
    while i < len(roman):
        letter = roman[i]
        if letter in check_two_letters and i < len(roman) - 1:
            two_letters = roman[i:(i + 2)]
            two_letters_value = value_dict.get(two_letters)
            if two_letters_value:
                if two_letters_value <= max_value:
                    repeated_same_value = 1
                    last_value = two_letters_value
                    max_value = next_max_value_dict[two_letters]
                    total += two_letters_value
                    i += 2
                    continue
                else:
                    raise ValueError('Invalid Roman numerals.')
        letter_value = value_dict.get(letter)
        if letter_value:
            if letter_value <= max_value:
                if last_value == letter_value:
                    if repeated_same_value < 3:
                        repeated_same_value += 1
                    else:
                        raise ValueError('Invalid Roman numerals.')
                else:
                    repeated_same_value = 1
                last_value = letter_value
                max_value = next_max_value_dict[letter]
                total += letter_value
                i += 1
            else:
                raise ValueError('Invalid Roman numerals.')
        else:
            raise ValueError('Invalid Roman numerals.')
    return total

def to_or_from_roman(string):
    '''If the given string can be represented as an integer, this function will convert it to Roman numerals,
    otherwise it will attempt to convert it from Roman numerals to an integer.'''
    try:
        number = int(string)
        print(to_roman(number))
    except ValueError:
        try:
            print(from_roman(string))
        except ValueError:
            print('Please input either an integer or a string of valid Roman numerals.')

def create_parser():
    '''Creates and returns the argument parser for this script.'''
    parser = argparse.ArgumentParser(description='Converts Arabic numerals into Roman numerals and vice versa.')
    parser.add_argument('number', type=str, help='Number to convert to or from Roman numerals')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    to_or_from_roman(args.number)

if __name__ == '__main__':
    main()
