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

Not finished yet, but queries the database for timetable information.  
Syntax:

	/timeplan/1.0/<subjectcode>/<week>  

If week is anything other than a number or omitted it will default to the current week. Getting data only works for the current time period (autumn or spring), due to when the timetables update on UiA's site.  

To retrieve subject codes for use in the URL, use this syntax:

	/timeplan/1.0/subjects/<search>

If you don't enter a search, it will list all saved subjects and their codes.

Data to expect: If you retrieved a time table, expect two dicts: "meta" and "timeplan".  
If you searched for a subject, expect one dict called "subjects".  
If an error occured, the return JSON will only have one dictionary: error, which will only contain an error string. Remember to check this when fetching.


## TODO

- Make a sample webpage for displaying timetables  
- Unified function for updating all needed data (to run once a week)
