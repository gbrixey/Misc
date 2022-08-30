import calendar
import datetime
import re

def _parse_date(date_string):
	'''Parse a date from the given string.
	The expected date format is mm/dd/yyyy
	'''
	components = date_string.split('/')
	if len(components) == 3:
		try:
			month = int(components[0])
			day = int(components[1])
			year = int(components[2])
			parsedDate = datetime.date(year, month, day)
			return parsedDate
		except:
			return None
	else:
		return None

def _get_date(adjective = ''):
	'''Asks the user to input a date.'''
	if len(adjective) > 0:
		adjective += ' '
	print("\nEnter {0}date (mm/dd/yyyy) or enter 'today' for today's date".format(adjective))
	date_string = input('\n>>> ')
	if date_string.lower() == 'today':
		return datetime.date.today()
	else:
		date = _parse_date(date_string)
		while date == None:
			print('Invalid date.')
			date_string = input('\n>>> ')
			date = _parse_date(date_string)
		return date

def _get_number_of_days():
	'''Asks the user to input a number (of days).'''
	print('\nEnter number of days (positive or negative).')
	days_string = input('\n>>> ')
	pattern = r'^\-?[0-9]+$'
	while re.search(pattern, days_string) == None:
		print('Invalid number.')
		days_string = input('\n>>> ')
	return int(days_string)

def _format_date(date):
	'''Formats a given date as a string, using the format mm/dd/yyyy.'''
	return '{0}/{1}/{2}'.format(date.month, date.day, date.year)
	
def _find_weekday():
	'''Prints the weekday of a date entered by the user.'''
	date = _get_date()
	weekday_strings = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	print('{0} is a {1}'.format(_format_date(date), weekday_strings[date.weekday()]))

def _days_between_two_dates():
	'''Calculates the number of days between two dates
	entered by the user.'''
	start_date = _get_date('starting')
	end_date = _get_date('ending')
	days = abs((end_date - start_date).days)
	verb = 'are' if days != 1 else 'is'
	plural = 's' if days != 1 else ''
	days_string = '{0} day{1}'.format(days, plural)
	print ('\nThere {0} {1} between {2} and {3}'.format(verb, days_string, _format_date(start_date), _format_date(end_date)))
	other_format = _days_months_and_years_between_two_dates(start_date, end_date)
	if other_format != days_string:
		print('Or ' + other_format)
	print('(Not including starting date)')

def _days_months_and_years_between_two_dates(start_date, end_date):
	'''Calculates the number of days, months, and years between two dates.
	Returns the result as a string.
	'''
	# Allow the two dates to be in either order by just swapping the arguments.
	if (start_date > end_date):
		return _days_months_and_years_between_two_dates(end_date, start_date)
	working_date = datetime.date(start_date.year, start_date.month, start_date.day)
	# Save start day for later reference
	start_day = start_date.day
	# Start with months = -1 so that on the first iteration it will become 0 (the lowest possible value).
	months = -1
	while working_date <= end_date:
		days = (end_date - working_date).days
		months += 1
		new_year = working_date.year
		new_month = working_date.month + 1
		if new_month > 12:
			new_month = 1
			new_year += 1
		days_in_new_month = calendar.monthrange(new_year, new_month)[1]
		new_day = min(start_day, days_in_new_month)
		working_date = datetime.date(new_year, new_month, new_day)
	years = int(months / 12)
	months = months % 12
	plural_year = 'years' if years != 1 else 'year'
	plural_month = 'months' if months != 1 else 'month'
	plural_day = 'days' if days != 1 else 'day'
	if years > 0:
		return '{0} {1}, {2} {3}, and {4} {5}'.format(years, plural_year, months, plural_month, days, plural_day)
	elif months > 0:
		return '{0} {1} and {2} {3}'.format(months, plural_month, days, plural_day)
	elif days > 0:
		return '{0} {1}'.format(days, plural_day)
	else:
		return '0 days'
		
def _date_by_adding_days():
	'''Print the date that occurs a given number of days
	after a given date.
	'''
	start_date = _get_date('starting')
	int_days = _get_number_of_days()
	days_delta = datetime.timedelta(int_days)
	end_date = start_date + days_delta
	plural_day = 'days' if int_days > 1 or int_days < -1 else 'day'
	if int_days < 0:
		first_string = '\n{0} {1} before'.format(-int_days, plural_day)
	else:
		first_string = '\n{0} {1} after'.format(int_days, plural_day)
	print('{0} {1} is {2}'.format(first_string, _format_date(start_date), _format_date(end_date)))
	print('(Not including starting date)')

def _start_text_interface():
	'''Initiates the text-based date calculator UI.'''
	while(True):
		print('\nWhat do you want to calculate?\n')
		print('    1. Weekday of a given date')
		print('    2. Number of days between two dates')
		print('    3. Date by adding or subtracting days from another date')
		print('    4. Quit')
		option = input('\n>>> ')
		while option not in ['1', '2', '3', '4']:
			print('Please enter a number between 1 and 4.')
			option = input('\n>>> ')
		if option == '1':
			_find_weekday()
		elif option == '2':
			_days_between_two_dates()
		elif option == '3':
			_date_by_adding_days()
		else:
			return None

def main():
	_start_text_interface()

if __name__ == '__main__':
	main()