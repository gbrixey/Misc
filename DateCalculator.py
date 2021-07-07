import tkinter
import datetime
import re

class DateCalculator():
	'''Calendar and date calculator.'''
	
	def __init__(self, *args, **kwargs):
		today = datetime.date.today()
		self.__year = today.year
		self.__month = today.month
		self.__day = today.day
		self.__month_strings = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		self.__weekday_strings = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		self.__weekday_short_strings = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
		self._create_ui()

	def run(self):
		self.__root.mainloop()
		
	def _create_ui(self):
		'''Creates all of the Tkinter UI elements.'''
		self.__root = tkinter.Tk()
		self.__columns = 16
		self.__rows = 16
		self.__year_button_row = 0
		self.__month_button_row = 2
		self.__weekday_labels_row = 4
		self.__calendar_initial_row = 6
		self.__calendar_initial_column = 4
		self.__calendar_final_row = 11
		self._create_date_fields()
		self._create_calculator_buttons()
		self._create_result_field()
		self._create_vertical_separator()
		self._create_year_buttons()
		self._create_month_buttons()
		self._create_weekday_labels()
		self._refresh_calendar()
	
	@staticmethod
	def _create_single_cell_button(text = '', fg = 'black', command = None):
		'''Helper method to create a square button with the given text.'''
		return tkinter.Button(text = text, width = 4, height = 2, fg = fg, command = command)
	
	@staticmethod
	def _create_single_cell_label(text = '', fg = 'black'):
		'''Helper method to create a square label with the given text.'''
		return tkinter.Label(text = text, width = 4, height = 2, fg = fg)
		
	def _create_horizontal_separator(self, separator_row, separator_column, column_span):
		'''Creates a horizontal line separator.'''
		separator = tkinter.Canvas(self.__root, width = 1, height = 1, bd = 0, bg = 'black')
		separator.grid(row = separator_row, column = separator_column, columnspan = column_span, sticky = 'EW')
		
	def _create_date_fields(self):
		'''Creates the date input fields.'''
		date_1_label = tkinter.Label(text = '  Date 1:  ')
		date_2_label = tkinter.Label(text = '  Date 2:  ')
		days_label = tkinter.Label(text = 'Days:  ')
		date_1_label.grid(row = self.__year_button_row, column = 0, sticky = 'E')
		date_2_label.grid(row = self.__month_button_row, column = 0, sticky = 'E')
		days_label.grid(row = self.__weekday_labels_row, column = 0, sticky = 'E')
		self.__date_1_field = tkinter.Entry()
		self.__date_2_field = tkinter.Entry()
		self.__days_field = tkinter.Entry()
		self.__date_1_field.grid(row = self.__year_button_row, column = 1, sticky = 'EW')
		self.__date_2_field.grid(row = self.__month_button_row, column = 1, sticky = 'EW')
		self.__days_field.grid(row = self.__weekday_labels_row, column = 1, sticky = 'EW')
		
	def _create_calculator_buttons(self):
		'''Creates the buttons for performing calculations.'''
		weekday_button = tkinter.Button(text = 'Weekday of Date 1', width = 30, command = self._calculate_weekday)
		duration_button = tkinter.Button(text = 'Days between Date 1 and Date 2', width = 30, command = self._calculate_duration)
		add_days_button = tkinter.Button(text = 'Add days to Date 1', width = 30, command = self._calculate_date_by_adding_days)		
		weekday_button.grid(row = self.__calendar_initial_row, column = 1, sticky = 'W')
		duration_button.grid(row = self.__calendar_initial_row + 1, column = 1, sticky = 'W')
		add_days_button.grid(row = self.__calendar_initial_row + 2, column = 1, sticky = 'W')
		
	def _create_result_field(self):
		'''Creates the output text field.'''
		# Add a horizontal separator between the calendar and result field
		self._create_horizontal_separator(self.__calendar_final_row + 1, 0, self.__columns)
		# Empty labels for padding above and below the result field.
		empty_label_1 = tkinter.Label(text = ' ', height = 1)
		empty_label_2 = tkinter.Label(text = ' ', height = 1)
		empty_label_1.grid(row = self.__calendar_final_row + 2, column = 0)
		empty_label_2.grid(row = self.__calendar_final_row + 4, column = 0)
		# Now actually create the result field.
		result_label = tkinter.Label(text = 'Result:')
		self.__result_field = tkinter.Text(height = 4, font = 'TkDefaultFont')
		result_label.grid(row = self.__calendar_final_row + 3, column = 0, sticky = 'E')
		self.__result_field.grid(row = self.__calendar_final_row + 3, column = 1, columnspan = self.__columns - 3)
	
	def _create_vertical_separator(self):
		'''Creates the vertical separator between the input/output part
		of the calculator and the calendar part of the calculator.
		'''
		# Use an empty label to pad out the column before the separator
		empty_label = tkinter.Label(text = ' ', width = 2)
		empty_label.grid(row = self.__year_button_row, column = self.__calendar_initial_column - 2)
		# Then create the vertical separator.
		separator = tkinter.Canvas(self.__root, width = 1, height = 1, bd = 0, bg = 'black')
		separator.grid(row = self.__year_button_row, column = self.__calendar_initial_column - 1, rowspan = self.__rows - 4, sticky = 'NS')
		
	def _create_year_buttons(self):
		'''Creates the year label and buttons
		to increment or decrement the year.
		'''
		previous_year_button = DateCalculator._create_single_cell_button(text = '<', command = self._decrement_year)
		previous_year_button.grid(row = self.__year_button_row, column = self.__calendar_initial_column)
		self.__current_year_label = tkinter.Label(text = str(self.__year), relief = tkinter.SUNKEN, width = 12, pady = 4)
		self.__current_year_label.grid(row = self.__year_button_row, column = self.__calendar_initial_column + 1, columnspan = 5)
		next_year_button = DateCalculator._create_single_cell_button(text = '>', command = self._increment_year)
		next_year_button.grid(row = self.__year_button_row, column = self.__calendar_initial_column + 6)
		self._create_horizontal_separator(self.__year_button_row + 1, self.__calendar_initial_column, 7)
		
	def _create_month_buttons(self):
		'''Creates the month label and buttons
		to increment or decrement the month.
		'''
		previous_month_button = DateCalculator._create_single_cell_button(text = '<', command = self._decrement_month)
		previous_month_button.grid(row = self.__month_button_row, column = self.__calendar_initial_column)
		self.__current_month_label = tkinter.Label(text = self.__month_strings[self.__month], relief = tkinter.SUNKEN, width = 12, pady = 4)
		self.__current_month_label.grid(row = self.__month_button_row, column = self.__calendar_initial_column + 1, columnspan = 5)
		next_month_button = DateCalculator._create_single_cell_button(text = '>', command = self._increment_month)
		next_month_button.grid(row = self.__month_button_row, column = self.__calendar_initial_column + 6)
		self._create_horizontal_separator(self.__month_button_row + 1, self.__calendar_initial_column, 7)

	def _create_weekday_labels(self):
		'''Creates the weekday labels just above the calendar.'''
		for i in range(0, 7):
			label = DateCalculator._create_single_cell_label(text = self.__weekday_short_strings[i])
			label.grid(row = self.__weekday_labels_row, column = self.__calendar_initial_column + i)
		self._create_horizontal_separator(self.__weekday_labels_row + 1, self.__calendar_initial_column, 7)
		
	def _refresh_calendar(self):
		'''Recreates the calendar grid.'''
		# Remove old calendar elements.
		for element in self.__root.grid_slaves():
			element_row = int(element.grid_info()['row'])
			element_column = int(element.grid_info()['column'])
			calendar_row = (element_row >= self.__calendar_initial_row and element_row < self.__calendar_initial_row + 6)
			calendar_column = (element_column >= self.__calendar_initial_column and element_column < self.__calendar_initial_column + 7)
			if calendar_row and calendar_column:
				element.grid_forget()

		first_of_this_month = datetime.date(self.__year, self.__month, 1)
		weekday_of_first_day = (first_of_this_month.weekday() + 1) % 7
		calendar_square_list = [None] * 42
		
		# Create labels for days of previous month.
		if weekday_of_first_day > 0:
			if self.__month == 1:
				previous_month = 12
				year_of_previous_month = self.__year - 1
			else:
				previous_month = self.__month - 1
				year_of_previous_month = self.__year
			last_day_of_previous_month = DateCalculator._days_in_month(previous_month, year_of_previous_month)
			for i in range(weekday_of_first_day - 1, -1, -1):
				label = DateCalculator._create_single_cell_label(text = str(last_day_of_previous_month))
				calendar_square_list[i] = label
				last_day_of_previous_month -= 1
		
		# Create buttons for days of this month.
		days_in_this_month = DateCalculator._days_in_month(self.__month, self.__year)
		for i in range(0, days_in_this_month):
			button = DateCalculator._create_single_cell_button(text = str(i + 1), fg = 'blue', command = lambda i=i: self._set_day(i + 1))
			today = datetime.date.today()
			if self.__year == today.year and self.__month == today.month and i + 1 == today.day:
				button.config(fg = 'red')
			calendar_square_list[weekday_of_first_day + i] = button
		
		# Create labels for days of next month.
		day_of_next_month = 1
		for i in range(weekday_of_first_day + days_in_this_month, 42):
			label = DateCalculator._create_single_cell_label(text = str(day_of_next_month))
			calendar_square_list[i] = label
			day_of_next_month += 1
		
		# Grid all the elements.
		for i in range(42):
			row = int(i / 7) + self.__calendar_initial_row
			column = (i % 7) + self.__calendar_initial_column
			sticky = 'NEWS' if type(calendar_square_list[i]) is tkinter.Label else ''
			calendar_square_list[i].grid(row = row, column = column, sticky = sticky)

	def _increment_year(self):
		'''Increments the year and updates the calendar.'''
		self.__year += 1
		self.__current_year_label.config(text = str(self.__year))
		self._refresh_calendar()
		
	def _decrement_year(self):
		'''Decrements the year and updates the calendar.'''
		self.__year -= 1
		self.__current_year_label.config(text = str(self.__year))
		self._refresh_calendar()
		
	def _increment_month(self):
		'''Increments the month and updates the calendar.'''
		if self.__month == 12:
			self.__month = 1
			self.__year += 1
			self.__current_year_label.config(text = str(self.__year))
		else:
			self.__month += 1
		self.__current_month_label.config(text = self.__month_strings[self.__month])
		self._refresh_calendar()
		
	def _decrement_month(self):
		'''Increments the month and updates the calendar.'''
		if self.__month == 1:
			self.__month = 12
			self.__year -= 1
			self.__current_year_label.config(text = str(self.__year))
		else:
			self.__month -= 1
		self.__current_month_label.config(text = self.__month_strings[self.__month])
		self._refresh_calendar()
		
	def _set_day(self, day):
		'''Sets the day to the given day and updates one of the
		date fields with this date.
		'''
		self.__day = day
		field_to_write_date = self.__root.focus_get()
		# If neither date field is in focus, pick one in which to insert the date.
		# If one of the fields is empty, use that one. Otherwise just use the first one.
		if field_to_write_date != self.__date_1_field and field_to_write_date != self.__date_2_field:
			date_1 = self.__date_1_field.get()
			date_2 = self.__date_2_field.get()
			if date_1 == '' or date_1.isspace():
				field_to_write_date = self.__date_1_field
			elif date_2 == '' or date_2.isspace():
				field_to_write_date = self.__date_2_field
			else:
				field_to_write_date = self.__date_1_field
		if field_to_write_date == self.__date_1_field:
			self.__date_1_field.delete(0, tkinter.END)
			self.__date_1_field.insert(0, DateCalculator._format_date(self._get_date()))
		elif field_to_write_date == self.__date_2_field:
			self.__date_2_field.delete(0, tkinter.END)
			self.__date_2_field.insert(0, DateCalculator._format_date(self._get_date()))
		
	def _calculate_weekday(self):
		'''Calculates the weekday of the date in the Date 1 field.'''
		date = DateCalculator._parse_date(self.__date_1_field.get())
		if date == None:
			text = 'Invalid Date 1\nUse mm/dd/yyyy format'
		else:
			text = '{0} is a {1}'.format(DateCalculator._format_date(date), self.__weekday_strings[date.weekday()])
		self.__result_field.delete('1.0', tkinter.END)
		self.__result_field.insert('1.0', text)
	
	def _calculate_duration(self):
		'''Calculates the duration between the dates in the two date fields.'''
		date_1 = DateCalculator._parse_date(self.__date_1_field.get())
		date_2 = DateCalculator._parse_date(self.__date_2_field.get())
		other_format = None
		if date_1 == None:
			text = 'Invalid Date 1\nUse mm/dd/yyyy format'
		elif date_2 == None:
			text = 'Invalid Date 2\nUse mm/dd/yyyy format'
		else:
			tuple = DateCalculator._days_between_two_dates(date_1, date_2)
			days_string = tuple[0]
			text = tuple[1]
			other_format = DateCalculator._days_months_and_years_between_two_dates(date_1, date_2)
			if other_format == days_string:
				other_format = None
		self.__result_field.delete('1.0', tkinter.END)
		self.__result_field.insert('1.0', text)
		if other_format:
			self.__result_field.insert(tkinter.INSERT, '\nOr ' + other_format)
		if not text.startswith('Invalid'):
			self.__result_field.insert(tkinter.INSERT, '\n(Not including starting date)')
	
	def _calculate_date_by_adding_days(self):
		'''Adds the number in the number field to the date
		in the Date 1 field and outputs the resulting date.
		'''
		date = DateCalculator._parse_date(self.__date_1_field.get())
		days = DateCalculator._parse_integer(self.__days_field.get())
		if date == None:
			text = 'Invalid Date 1\nUse mm/dd/yyyy format'
		elif days == None:
			text = 'Invalid number of days.'
		else:
			text = DateCalculator._date_by_adding_days(date, days)
		self.__result_field.delete('1.0', tkinter.END)
		self.__result_field.insert('1.0', text)
		if not text.startswith('Invalid'):
			self.__result_field.insert(tkinter.INSERT, '\n(Not including starting date)')
				
	@staticmethod
	def _days_in_month(month, year):
		'''Returns the number of days in the given month,
		in the given year.
		'''
		if month not in range(1, 13):
			return 0
		elif month in [1, 3, 5, 7, 8, 10, 12]:
			return 31
		elif month in [4, 6, 9, 11]:
			return 30
		elif year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
			return 29
		else:
			return 28
	
	@staticmethod
	def _format_date(date):
		'''Formats a given date as a string, using the format mm/dd/yyyy.'''
		return '{0}/{1}/{2:0>4}'.format(date.month, date.day, date.year)
		
	@staticmethod
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
				parsed_date = datetime.date(year, month, day)
				return parsed_date
			except:
				return None
		else:
			return None
			
	@staticmethod
	def _parse_integer(number_string):
		'''Parses an integer from the given string.'''
		pattern = r'^\-?[0-9]+$'
		if re.search(pattern, number_string) == None:
			return None
		else:
			return int(number_string)
		
	def _get_date(self):
		'''Creates a date object from the year, month, and day variables.'''
		return datetime.date(self.__year, self.__month, self.__day)
	
	@staticmethod
	def _days_between_two_dates(start_date, end_date):
		'''Calculates the number of days between two dates.
		Returns a tuple of two strings with different formats
		of the result.
		
		e.g. for 1/1/2016 and 4/9/2016 this method would return
		('99 days', 'There are 99 days between 1/1/2016 and 4/9/2016')
		'''
		days = abs((end_date - start_date).days)
		verb = 'are' if days != 1 else 'is'
		plural = 's' if days != 1 else ''
		days_string = '{0} day{1}'.format(days, plural)
		text = 'There {0} {1} between {2} and {3}'.format(verb, days_string, DateCalculator._format_date(start_date), DateCalculator._format_date(end_date))
		return (days_string, text)
	
	@staticmethod
	def _days_months_and_years_between_two_dates(start_date, end_date):
		'''Calculates the number of days, months, and years between two dates.
		Returns the result as a string.
		'''
		# Allow the two dates to be in either order by just swapping the arguments.
		if (start_date > end_date):
			return DateCalculator._days_months_and_years_between_two_dates(end_date, start_date)
		years = end_date.year - start_date.year
		months = end_date.month - start_date.month
		if months < 0:
			years -= 1
			months += 12
		days = end_date.day - start_date.day
		if days < 0:
			months -= 1
			if months < 0:
				years -=1
				months += 12
			days += DateCalculator._days_in_month(start_date.month, start_date.year)
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
	
	@staticmethod
	def _date_by_adding_days(start_date, days):
		'''Print the date that occurs a given number of days after a given date.'''
		days_delta = datetime.timedelta(days)
		end_date = start_date + days_delta
		plural_day = 'days' if days > 1 or days < -1 else 'day'
		if days < 0:
			first_string = '{0} {1} before'.format(-days, plural_day)
		else:
			first_string = '{0} {1} after'.format(days, plural_day)
		return '{0} {1} is {2}'.format(first_string, DateCalculator._format_date(start_date), DateCalculator._format_date(end_date))
		
def main():
	calculator = DateCalculator()
	calculator.run()

if __name__ == '__main__':
	main()
