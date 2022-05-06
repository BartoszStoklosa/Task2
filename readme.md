**Tax 2**

Script will find soonest date when at least desired number of people are available for given amount of time. With possibility of searching further if user finds date inappropriate.

**Setup**

To run the scrip we have to place all folders containing .txt file with events in people’s calendars.Every .txt file's name has have one of two types:

Type 1:

	name.txt

Type 2:

	name_surname.txt

In every .txt file has contain only lines that match the patterns:

Pattern 1:

	year-month-date

Which means that whole given day is busy.
	
Pattern 2:

	year-month-date hour-minute-second - year-month-date hour-minute-second

Where the first segment means beginning and the 2nd means end of unavailable period of time.

Lines don’t affect on each other so can be contained in random order.

**Warning**

File has to have no empty lines.

**How to use it**

Script accepts a named parameter --duration_in_minutes which defines for how many minutes people should be available.  Minimum number of people that must be available
should be defined by --minimum_people argument.  Script should read people's calendars from .txt files in the directory provided as an --calendars string and --appointment_date given as year-month-date hour-minute-second which  defines the soonest date which user wants.

We can run code using console in same folder as our script by calling line matching pattern:

	python3 find-available-slot.py --calendars __ --duration_in_minutes __ --minumum_people _ --appointment_date __

Example:

	python3 main.py --calendars /in --duration_in_minutes 30 --minimum_people 2 --appointment_date 2022-07-01_02:30:00
	
When we run script program will show attending people and earliest hour with dialog window asking if user wants to set an  appointment. If user agrees date will be append in attending people’s calendars. Otherwise user will be asked if he/she wants to search for a next date. If user decides to disagree program will end but if user agrees program will mark last found date as busy and start searching again. **Warning** the soonest date will be starting at least after end of last found date. Procedure will continue until user will not agree for date or decides to stop searching then all dates marked before as busy will return to being available.


