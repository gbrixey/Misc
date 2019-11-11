#!/usr/bin/env python
import argparse
import re
import datetime
import pickle
from collections import defaultdict

pickle_path = 'drink.pickle'

def record_ml(ml, date):
    '''Record the given amount of alcohol consumed on the given date, in milliliters.
    If a date is not provided, the current date is used instead.'''
    if ml <= 0:
        raise ValueError('mL should be greater than 0.')
    if date == None:
        date = datetime.date.today()
    elif (date - datetime.date.today()).days > 0:
        raise ValueError('Date should be in the past or present.')
    record = load_records()
    if ml > possible_ml_on_date(date):
        print('Whoops! You broke the rules.')
    prior_ml = record[date]
    record[date] += ml
    save_records(record)
    if prior_ml == 0:
        print('Added {0} mL on {1}.'.format(ml, format_date(date)))
    else:
        print('Added {0} mL on {1}, for a total of {2}.'.format(ml, format_date(date), record[date]))
    if date == datetime.date.today():
        print_possible_ml_on_date(date)
    
def check_date(date):
    '''If the given date is in the past, this function checks how many mL of alcohol were consumed on that date.
    If the date is in the future, it checks how many mL can be consumed on that date, assuming none are
    consumed in the intervening period. If the date is the present day, both checks are performed.'''
    record = load_records()
    days_delta = (date - datetime.date.today()).days
    if days_delta < 0:
        if days_delta == -1:
            print('You had {0} mL yesterday.'.format(record[date]))
        else:
            print('You had {0} mL on {1}.'.format(record[date], format_date(date)))
        return
    if days_delta == 0:
        print('You have had {0} mL today.'.format(record[date]))
    print_possible_ml_on_date(date)

def possible_ml_on_date(date):
    '''Checks the amount of alcohol that could be consumed on the given date,
    assuming none is consumed in the intervening period.'''
    record = load_records()
    week = [record[date + datetime.timedelta(delta)] for delta in range(-6, 0)]
    week.append(record[date])
    # No drinking on consecutive days
    if week[-2] > 0:
        return 0
    # Maximum 140 mL per week
    week_remaining = max(0, 140 - sum(week))
    # Maximum 60 mL per day
    day_remaining = max(0, 60 - week[-1])
    return min(week_remaining, day_remaining)

def print_possible_ml_on_date(date):
    '''Prints the amount of alcohol that can be consumed on the given date.'''
    possible_ml = possible_ml_on_date(date)
    days_delta = (date - datetime.date.today()).days
    if days_delta == 0:
        print('You can have {0} more mL today.'.format(possible_ml))
    elif days_delta == 1:
        print('You can have {0} mL tomorrow.'.format(possible_ml))
    else:
        print('You can have {0} mL on {1}.'.format(possible_ml, format_date(date)))

def check_next_drink():
    '''Checks the next date on which alcohol can be consumed.'''
    date = datetime.date.today()
    possible_ml = possible_ml_on_date(date)
    while possible_ml == 0:
        date += datetime.timedelta(1)
        possible_ml = possible_ml_on_date(date)
    print_possible_ml_on_date(date)

def load_records():
    '''Attempts to read the record of alcohol consumption from the pickle file.
    Returns an empty dictionary if unsuccessful.'''
    try:
        with open(pickle_path, 'rb') as pickle_file:
            return pickle.load(pickle_file)
    except Exception as e:
        return defaultdict(int)
        
def save_records(records):
    '''Save the given records dictionary to the pickle file.'''
    try:
        with open(pickle_path, 'wb') as pickle_file:
            pickle.dump(records, pickle_file)
    except Exception as e:
        print('An error occured while trying to update the pickle file.')

def format_date(date):
    '''Formats the given date as a string in yyyy/mm/dd format.'''
    return date.strftime('%Y/%m/%d')

def parse_date(date_string):
    '''Tries to parse a date in yyyy/mm/dd or mm/dd format from the given string.
    If mm/dd format is used, the date returned will be in the current year.'''
    components = date_string.split('/')
    pattern = '^[0-9]{1,2}/[0-9]{1,2}$'
    if re.match(pattern, date_string):
        today = datetime.date.today()
        return datetime.date(today.year, int(components[0]), int(components[1]))
    pattern = '^[0-9]{1,4}/[0-9]{1,2}/[0-9]{1,2}$'
    if re.match(pattern, date_string):
        return datetime.date(int(components[0]), int(components[1]), int(components[2]))
    raise ValueError('Date should be in yyyy/mm/dd format.')

def print_info():
    '''Prints a description of the rules behind this program.'''
    print('\nHere are the rules:\n')
    print('1. No more than 60 mL of pure alcohol per day.')
    print('2. No more than 140 mL per week.')
    print('3. No drinking on consecutive days.\n')

def create_parser():
    '''Creates and returns the argument parser for this script.'''
    parser = argparse.ArgumentParser(description='Keep track of your drinking habits.', usage='%(prog)s [-hr] [-d DATE] [-m ML]')
    parser.add_argument('-d', dest='date', default=None, type=str, help='Date in mm/dd or yyyy/mm/dd format')
    parser.add_argument('-m', dest='ml', default=None, type=int, help='Record mL of pure alcohol')
    parser.add_argument('-r', dest='print_info', action='store_const', default=False, const=True, help='What are the rules?')
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.print_info:
        print_info()
        return
    ml = args.ml
    date = None
    date_string = args.date
    if date_string != None:
        date = parse_date(date_string)
    if ml != None:
        record_ml(ml, date)
    elif date != None:
        check_date(date)
    else:
        check_next_drink()

if __name__ == '__main__':
    main()