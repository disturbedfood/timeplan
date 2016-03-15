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

	/<subjectcode>/<week>  

If week is anything other than a number it'll default to the current week. Getting data only works for the current time period (autumn or spring), due to when the timetables update on UiA's site. 
Subject codes can be retrieved with the get\_subject\_codes function in timeplan.py (will add an api for this as well)

The return JSON has two dictionaries: meta and timeplan. The meta contains the week number, course code, human readable course name, when it was last updated and the human readable names for each index in the timeplan objects.  
If an error occured, the return JSON will only have one dictionary: error, which will only contain an error string. Remember to check this when fetching.


## TODO

- Better info gathering
- API for subject codes
- Make a Subjects table
- Make a sample webpage for displaying timetables
