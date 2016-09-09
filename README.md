## Timeplan

A fetcher script and API for timetables at the University of Agder.

### Requirements
	requests  
	BeautifulSoup4
	dateutil
	lxml

## API

**Additional dependencies:**

	flask
    flask_cors

Queries the database for timetable information.  

### Getting courses  
Syntax:

	/timeplan/2.0/<coursecode>/<week>  

If week is anything other than a number or omitted it will default to the current week. Getting data only works for the current time period (autumn or spring), due to when the timetables update on UiA's site.  

To retrieve course codes for use in the URL, use this syntax:

	/timeplan/2.0/courses/<search>

If you don't enter a search, it will list all saved courses and their codes (codes are updated, they are now hashed and are all 10 characters).


### Getting subjects  
Syntax:  

	/timeplan/2.0/<subjectcode>/<week>

Same thing with the week here.

To get an overview of all the saved subject codes and their related course codes, use this:

	/timeplan/2.0/subjects

Data to expect: If you retrieved a time table, expect two dicts: "meta" and "timeplan".  
If you searched for a course, expect one dict called "courses".  
If an error occured, the return JSON will only have one dictionary: error, which will only contain an error string. Remember to check this when fetching.


## TODO

- Make a sample webpage for displaying timetables  
- Unified function for updating all needed data (to run once a week) (semi-done, there's now reciever.py)
