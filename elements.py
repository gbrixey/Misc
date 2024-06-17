#!/usr/bin/env python3
import argparse
import re

ELEMENTS = {
    'ac': 'actinium',
    'ag': 'silver',
    'al': 'aluminum',
    'am': 'americium',
    'ar': 'argon',
    'as': 'arsenic',
    'at': 'astatine',
    'au': 'gold',
    'b': 'boron',
    'ba': 'barium',
    'be': 'beryllium',
    'bh': 'bohrium',
    'bi': 'bismuth',
    'bk': 'berkelium',
    'br': 'bromine',
    'c': 'carbon',
    'ca': 'calcium',
    'cd': 'cadmium',
    'ce': 'cerium',
    'cf': 'californium',
    'cl': 'chlorine',
    'cm': 'curium',
    'cn': 'copernicum',
    'co': 'cobalt',
    'cr': 'chromium',
    'cs': 'caesium',
    'cu': 'copper',
    'ds': 'darmstadtium',
    'db': 'dubnium',
    'dy': 'dysprosium',
    'er': 'erbium',
    'es': 'einsteinium',
    'eu': 'europium',
    'f': 'fluorine',
    'fe': 'iron',
    'fl': 'flerovium',
    'fm': 'fermium',
    'fr': 'francium',
    'ga': 'gallium',
    'gd': 'gadolinium',
    'ge': 'germanium',
    'h': 'hydrogen',
    'he': 'helium',
    'hf': 'hafnium',
    'hg': 'mercury',
    'ho': 'holmium',
    'hs': 'hassium',
    'i': 'iodine',
    'in': 'indium',
    'ir': 'iridium',
    'k': 'potassium',
    'kr': 'krypton',
    'la': 'lanthanum',
    'li': 'lithium',
    'lr': 'lawrencium',
    'lu': 'lutetium',
    'lv': 'livermorium',
    'mc': 'moscovium',
    'md': 'mendelevium',
    'mg': 'magnesium',
    'mn': 'manganese',
    'mo': 'molybdenum',
    'mt': 'meitnerium',
    'n': 'nitrogen',
    'na': 'sodium',
    'nb': 'niobium',
    'nd': 'neodymium',
    'ne': 'neon',
    'nh': 'nihonium',
    'ni': 'nickel',
    'no': 'nobelium',
    'np': 'neptunium',
    'o': 'oxygen',
    'og': 'oganesson',
    'os': 'osmium',
    'p': 'phosphorus',
    'pa': 'protactinium',
    'pb': 'lead',
    'pd': 'palladium',
    'pm': 'promethium',
    'po': 'polonium',
    'pr': 'praseodymium',
    'pt': 'platinum',
    'pu': 'plutonium',
    'ra': 'radium',
    'rb': 'rubidium',
    're': 'rhenium',
    'rf': 'rutherfordium',
    'rg': 'roentgenium',
    'rh': 'rhodium',
    'rn': 'radon',
    'ru': 'ruthenium',
    's': 'sulfur',
    'sb': 'antimony',
    'sc': 'scandium',
    'se': 'selenium',
    'sg': 'seaborgium',
    'si': 'silicon',
    'sm': 'samarium',
    'sn': 'tin',
    'sr': 'strontium',
    'ta': 'tantalum',
    'tb': 'terbium',
    'tc': 'technetium',
    'te': 'tellurium',
    'th': 'thorium',
    'ti': 'titanium',
    'tl': 'thallium',
    'tm': 'thulium',
    'ts': 'tennessine',
    'u': 'uranium',
    'v': 'vanadium',
    'w': 'tungsten',
    'xe': 'xenon',
    'y': 'yttrium',
    'yb': 'ytterbium',
    'zn': 'zinc',
    'zr': 'zirconium'
}

def elements(word):
    '''Tries to break down the given word into a list of chemical element symbols.
    Non-alphabetic characters are ignored. There may be multiple solutions.'''
    letters = ''.join(re.findall('[a-z]+', word.lower()))
    if len(letters) == 0:
        print('Please enter a word with at least one letter.')
        return
    solutions = elements_helper([], letters)
    count = len(solutions)
    print('Found {0} solution{1} for "{2}".'.format(count, '' if count == 1 else 's', word))
    for solution in solutions:
        symbols = ', '.join([symbol.capitalize() for symbol in solution])
        element_names = ', '.join([ELEMENTS[symbol].capitalize() for symbol in solution])
        print('{0} ({1})'.format(symbols, element_names))

def elements_helper(partial_list, partial_word):
    '''Recursive helper function for the elements function.'''
    result = []
    if len(partial_word) > 0 and partial_word[0] in ELEMENTS.keys():
        new_list = partial_list + [partial_word[0]]
        if len(partial_word) == 1:
            result.append(new_list)
        else:
            result.extend(elements_helper(new_list, partial_word[1:]))
    if len(partial_word) > 1 and partial_word[:2] in ELEMENTS.keys():
        new_list = partial_list + [partial_word[:2]]
        if len(partial_word) == 2:
            result.append(new_list)
        else:
            result.extend(elements_helper(new_list, partial_word[2:]))
    return result

def create_parser():
    '''Creates and returns the argument parser for this script.'''
    parser = argparse.ArgumentParser(description = 'Determines if a given word can be broken down into chemical element symbols.')
    parser.add_argument('word', type=str, help='The word to try to break down into chemical element symbols.')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    word = args.word
    elements(word)

if __name__ == "__main__":
    main()
