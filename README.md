## Timeplan

A fetcher script and API for timetables at the University of Agder.

### Requirements
	requests  
	BeautifulSoup4
	dateutil
	lxmli

## API

**Additional dependencies:**

	flask

Not finished yet, but queries the database for timetable information.  
Syntax:

	/<subjectcode>/<week>  

If week is anything other than a number it'll default to the current week.  
Subject codes can be retrieved with the get\_subject\_codes function in timeplan.py (will add an api for this as well)


## TODO

- Better info gathering
- API for subject codes
- Make a Subjects table
- Make a sample webpage for displaying timetables
