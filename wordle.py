#!/usr/bin/env python3
from collections import defaultdict

class Wordle():

    def __init__(self, *args, **kwargs):
        with open('wordle_words.txt') as f:
            self.__word_list = f.read().split(',')

    # Public

    def start(self):
        '''Start a Wordle game.'''
        self.__guess = 1
        self.__must_contain = set()
        self.__must_contain_two = set()
        self.__must_contain_three = set()
        self.__excluded_letters = [set(), set(), set(), set(), set()]
        self.__known_letters = [None, None, None, None, None]
        while self.__guess < 7:
            guess = self._take_guess()
            if guess == 'q':
                return
            pattern = self._take_pattern(guess)
            if pattern == 'Q':
                return
            if pattern == 'GGGGG':
                if self.__guess == 1:
                    print('Congratulations! You got it in 1 guess.')
                else:
                    print('Congratulations! You got it in {0} guesses.'.format(self.__guess))
                return
            self._compute_guess(guess, pattern)
            if self.__guess < 6:
                self._suggested_word()
            self.__guess += 1
        print("Uh oh, we didn't get it.")
        filtered_words = self._filtered_words()
        if len(filtered_words) > 0:
            print('The remaining words were:')
            for word in filtered_words:
                print(word)

    # Private
    
    def _take_guess(self):
        '''Ask the user to enter a five-letter Wordle guess.'''
        if self.__guess == 1:
            print('Starting a Wordle game!')
            print('You can enter Q at any time to quit.')
            print('Type your first guess:')
        else:
            print('Type your guess:')
        guess = input('>>> ').lower()
        while guess != 'q' and (len(guess) != 5 or not guess.isalpha()):
            print('Please enter a 5 letter word.')
            guess = input('>>> ').lower()
        return guess
        
    def _take_pattern(self, guess):
        '''Ask the user to enter the result of a Wordle guess.'''
        print('Type the colors of the letters in this guess.')
        if self.__guess == 1:
            print('B for blank, Y for yellow, G for green.')
            print('ex. BBYBG')
        pattern = input('>>> ').upper()
        while pattern != 'Q' and (len(pattern) != 5 or not set(pattern).issubset(set('BGY'))):
            print('Please enter 5 letters, using only the letters B, G, and Y.')
            pattern = input('>>> ').upper()
        return pattern

    def _compute_guess(self, guess, pattern):
        '''Updates instance variables based on the given guess.'''
        # Handle greens and yellows first
        yellows_per_character = defaultdict(int)
        greens_per_character = defaultdict(int)
        for (index, character) in enumerate(guess):
            if pattern[index] == 'G':
                self.__must_contain.add(character)
                self.__known_letters[index] = character
                greens_per_character[character] += 1
            elif pattern[index] == 'Y':
                self.__must_contain.add(character)
                self.__excluded_letters[index].add(character)
                yellows_per_character[character] += 1
        # Handle blanks
        for (index, character) in enumerate(guess):
            if pattern[index] == 'B':
                # If the letter already appeared as a yellow elsewhere in the word,
                # then it only gets excluded from this index specifically.
                if yellows_per_character[character] > 0:
                    self.__excluded_letters[index].add(character)
                # If the letter already appeared as a green elsewhere in the word,
                # then it gets excluded from every index apart from the green one(s).
                elif greens_per_character[character] > 0:
                    for index2 in range(5):
                        if self.__known_letters[index2] != character:
                            self.__excluded_letters[index2].add(character)
                else:
                    # Otherwise the letter gets excluded from all indices.
                    for letter_set in self.__excluded_letters:
                        letter_set.add(character)
        # Keep track of whether the word should contain multiples of a letter.
        for character in guess:
            yellows_and_greens = yellows_per_character[character] + greens_per_character[character]
            if yellows_and_greens > 1:
                self.__must_contain_two.add(character)
            if yellows_and_greens > 2:
                self.__must_contain_three.add(character)

    def _suggested_word(self):
        '''Suggest the next word the user should play, based on the results so far.'''
        filtered_words = self._filtered_words()
        if len(filtered_words) == 0:
            return
        print('{0} remaining words'.format(len(filtered_words)))
        character_count_dict = defaultdict(int)
        frequency_dict = defaultdict(float)
        for word in filtered_words:
            for character in word:
                character_count_dict[character] += 1
        total_characters = len(filtered_words) * 5
        for character in character_count_dict.keys():
            frequency_dict[character] = character_count_dict[character] / total_characters
        def word_weight(word):
            weight = sum([frequency_dict[character] for character in word])
            # give more weight to words with more unique characters
            weight *= len(set(word))
            return weight
        word_weights = [(word, word_weight(word)) for word in filtered_words]
        word_weights.sort(key = lambda t: t[1], reverse = True)
        print('Suggested word: {0}'.format(word_weights[0][0].upper()))

    def _filtered_words(self):
        '''Returns words that match the results of previous guesses.'''
        return [word for word in self.__word_list if self._filter_word(word)]
    
    def _filter_word(self, word):
        '''Determines if the given word matches the results of previous guesses.'''
        for letter in self.__must_contain:
            if letter not in word:
                return False
        for letter in self.__must_contain_two:
            if word.count(letter) < 2:
                return False
        for letter in self.__must_contain_three:
            if word.count(letter) < 3:
                return False
        for (index, character) in enumerate(word):
            known_letter = self.__known_letters[index]
            if known_letter != None and character != known_letter:
                return False
            if character in self.__excluded_letters[index]:
                return False
        return True

if __name__ == "__main__":
    wordle = Wordle()
    wordle.start()