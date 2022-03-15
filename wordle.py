#!/usr/bin/env python3
from collections import defaultdict

class Wordle():

    def __init__(self, *args, **kwargs):
        with open('wordle_words.txt') as f:
            self.__word_list = f.read().split(',')
            self._reset_variables()

    # Public

    def start(self):
        '''Start a Wordle game.'''
        self._reset_variables()
        while self.__turn < 7:
            guess = self._take_guess()
            if guess == 'q':
                return
            pattern = self._take_pattern(guess)
            if pattern == 'Q':
                return
            if pattern == 'GGGGG':
                if self.__turn == 1:
                    print('Congratulations! You got it in 1 guess.')
                else:
                    print('Congratulations! You got it in {0} guesses.'.format(self.__turn))
                return
            self._compute_guess(guess, pattern)
            if self.__turn < 6:
                filtered_words = self._filtered_words()
                print('{0} remaining words'.format(len(filtered_words)))
                suggested_word = self._suggested_word()
                if suggested_word:
                    print('Suggested word: {0}'.format(suggested_word.upper()))
            self.__turn += 1
        print("Uh oh, we didn't get it.")
        filtered_words = self._filtered_words()
        if len(filtered_words) > 0:
            print('The remaining words were:')
            for word in filtered_words:
                print(word)
                
    def autoplay(self, solution, first_guess = None, print_guesses = False):
        '''Determine how many guesses it would take to solve the Wordle
        using the script's suggested word for every guess.'''
        self._reset_variables()
        guess = first_guess
        if guess == None:
            guess = self._suggested_word()
        while self.__turn < 7:
            if print_guesses:
                print(guess)
            pattern = self._pattern(solution, guess)
            if pattern == 'GGGGG':
                return self.__turn
            self._compute_guess(guess, pattern)
            guess = self._suggested_word()
            self.__turn += 1
        if print_guesses:
            print('X')
        return None

    def test(self, first_guess = None):
        '''Test how well the script would do at solving the Wordle
        for all of the available words in the word list.'''
        score_dict = defaultdict(int)
        for (index, word) in enumerate(self.__word_list):
            score = self.autoplay(word, first_guess)
            score_dict[score] += 1
            score_string = 'X' if score == None else score
            print('{0:<4} {1}: {2}'.format(index, word, score_string))
        total_guesses = 0
        for score in range(1, 7):
            total_guesses += (score * score_dict[score])
            print('{0}: {1}'.format(score, score_dict[score]))
        print('X: {0}'.format(score_dict[None]))
        average_score = total_guesses / len(self.__word_list)
        print('Average: {0}'.format(average_score))

    # Private
    
    def _reset_variables(self):
        self.__turn = 1
        self.__must_contain = set()
        self.__must_contain_two = set()
        self.__must_contain_three = set()
        self.__excluded_letters = [set(), set(), set(), set(), set()]
        self.__known_letters = [None, None, None, None, None]
    
    def _take_guess(self):
        '''Ask the user to enter a five-letter Wordle guess.'''
        if self.__turn == 1:
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
        if self.__turn == 1:
            print('B for blank, Y for yellow, G for green.')
            print('ex. BBYBG')
        pattern = input('>>> ').upper()
        while pattern != 'Q' and (len(pattern) != 5 or not set(pattern).issubset(set('BGY'))):
            print('Please enter 5 letters, using only the letters B, G, and Y.')
            pattern = input('>>> ').upper()
        return pattern

    def _pattern(self, solution, guess):
        '''Returns the pattern of colors that would appear in a Wordle game
        for the given guess and the given solution.'''
        pattern = ['', '', '', '', '']
        # Handle greens first
        filtered_solution = list(solution)
        filtered_guess = list(guess)
        for (index, character) in enumerate(guess):
            if guess[index] == solution[index]:
                pattern[index] = 'G'
                filtered_solution[index] = ''
                filtered_guess[index] = ''
        # Handle yellows and blanks
        for (index, character) in enumerate(filtered_guess):
            if character == '':
                continue
            if character in filtered_solution:
                pattern[index] = 'Y'
                index_in_solution = filtered_solution.index(character)
                filtered_solution[index_in_solution] = ''
            else:
                pattern[index] = 'B'
        return ''.join(pattern)

    def _compute_guess(self, guess, pattern):
        '''Updates instance variables based on the given guess and pattern.'''
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
            return None
        frequency_dict = defaultdict(float)
        for word in filtered_words:
            for character in word:
                frequency_dict[character] += 1
        def word_weight(word):
            weight = sum([frequency_dict[character] for character in word])
            # give more weight to words with more unique characters
            weight *= (1 + len(set(word)))
            return weight
        word_weights = [(word, word_weight(word)) for word in filtered_words]
        word_weights.sort(key = lambda t: t[1], reverse = True)
        return word_weights[0][0]

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