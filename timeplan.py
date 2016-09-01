# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
from time import sleep
import datetime as dt
from urllib2 import urlopen
from collections import OrderedDict
import re
from dateutil import parser
import hashlib
import codecs
ROOMS_RE = re.compile('(.\d \d{3})')
SUB_CODE_RE = re.compile('([A-Z]{2,3}[^\s]\d{3})')


# These are parameters that will be fetched from the page.
auto_params = ["__EVENTTARGET", "__EVENTARGUMENT", "__LASTFOCUS", "__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION", "tLinkType",
			  "tWildcard", 'bGetTimetable']

day_convert = {"Man": "Mon", "Tir": "Tue", "Ons": "Wed", "Tor": "Thu", "Fre": "Fri", "Lør": "Sat"}

# Parses type of lesson. NOTE: THIS IS NOT WORKING AT THE MOMENT
def parse_type(type_check):
	type_check = type_check.lower().split("/")
	type = ""
	
	for i in range(0, len(type_check) - 1):
		if (len(type_check) - 1) < i: break
		if "for" in type_check[i]:
			type += "Lecture"
			del type_check[i]
		if (len(type_check) - 1) < i: break
		if "sem" in type_check[i]:
			if len(type) > 0: type += "/"
			type += "Seminar"
			del type_check[i]
		if (len(type_check) - 1) < i: break
		if "øv" in type_check[i] or "lab" in type_check[i]:
			if len(type) > 0: type += "/"
			type += "Practice"
			del type_check[i]
		
	if len(type) == 0: return ["See info", " ".join(type_check)]
	else: return [type, " ".join(type_check)]

# Get correct url
def get_query_url(season):
	return "http://timeplan.uia.no/swsuia" + season + "/public/no/default.aspx"

# Gets the parameters that should be used for requesting timetable data from server.
def get_parameters(session, days, weeks, subject_code, season):
	params = {
		'RadioType': "XMLSpreadsheet;studentsetxmlurl;SWSCUST+StudentSet+XMLSpreadsheet",
		'lbDays': days,
		'lbWeeks': weeks,
		'dlObject': subject_code
	}
	
	r = False
	soup = False
	params['__EVENTVALIDATION'] = False
	
	# Get our event validation token
	while not params['__EVENTVALIDATION']:
		# Give some grace period (don't spam the server - at least too much)
		sleep(0.5)
		
		# Load up the page to get parameters from
		r = session.get(get_query_url(season))
		
		# Save the event validation token
		soup = BeautifulSoup(r.text, 'lxml')
		params['__EVENTVALIDATION'] = soup.find(id='__EVENTVALIDATION')
	
	# Now we need to save all the needed parameters
	for p in auto_params:
		thing = soup.find(id=p)
		if thing != None:
			val = thing.get('value')
			if val:
				params[p] = val
			else:
				params[p] = ""
		else:
			params[p] = p
	
	return params
		
# Gets the timetable for all subjects in dict, in whatever weeks specified.
def get_all(courses, days, weeks, season):
	url = get_query_url(season)
	data = {}
	
	s = requests.Session()
	
	print "Setting parameters.."
	# Subject code gets set in the loop so empty string is fine here
	params = get_parameters(s, days, weeks, "", season)
	counter = 0
	print "Getting course data.."
	for k, v in courses.iteritems():
		counter += 1
		# Set the subject code for the request
		params['dlObject'] = v[1]
		
		# Fetch the data (raw)
		r = s.post(url, data=params)
		
		# Convert the raw data into a list of tuples
		data[k] = convert_to_table_format(r.text, csv=False)
		if data[k] == None:
			print "Could not get data for", k + ". Skipping"
			continue
			
		print "Got data for", k + ",", str(len(data[k])), "rows of data,", counter,"/",len(courses)
		
	return data

# Gets a dict with course hashes as keys and human readable names for courses as values.
def retrieve_course_codes(season):
	data = {}
	html = None
	raw_data = None
	# Check if the HTML contains the pWeeks tag (not used, but sometimes we won't get all course data and that happens when not all the HTML is in)
	contains_weeks = None
	
	with requests.Session() as s:
		while not raw_data and contains_weeks == None:
			req = s.get(get_query_url(season))
			html = BeautifulSoup(req.text, 'lxml')
			# Give server a little grace time (sorry, server)
			sleep(1)
			raw_data = html.find(id='dlObject')
			contains_weeks = html.find(id='pWeeks')

	# We got our data, now structure it in our data dict (use hash for id)
	for c in raw_data.find_all('option'):
		id = hashlib.md5(c.get('value').encode('utf-8')).hexdigest()[0:10]
		data.update({id: (c.getText(), c.get('value'))})
	
	print "Fetched", len(data), "courses."
	if len(data) < 435:
		deb = codecs.open("html.txt", "w", "utf-8")
		deb.write(html.prettify())
		print "wrote debug file"
		print contains_weeks
		print html.find(id='pWeeks')
		deb.close()
	
	return data

# Sorts out the raw HTML for the site, passing what's needed into get_row_info
# If csv is set to false it will create a list with all the information, with csv it makes a long string
def convert_to_table_format(html, csv=False):
	soup = BeautifulSoup(html, 'lxml')
	tab = soup.find_all('table')
	table = []
	if csv: table = ""
	week_no = 0
	for week_table in tab:
		# For each week table
		for week_row in week_table:
			# Each row per table.
			try: 
				row_type = week_row.get('class')
			except:
				print "------------------ Error getting data for this. Refetching/retrying."
				return None

			# tr1 means this is a table header
			if "tr1" in row_type:
				week_info = week_row.find('td', {"class": "td1"})
				week_no = week_info.getText().split(",")[0][4:]
				if csv: table += "\n"

			# tr2 - this is actual content
			if "tr2" in row_type:
				row = week_row.find_all('td')
				if csv:
					table += get_row_info(row, week_no, csv)
				else:
					table.append(get_row_info(row, week_no, csv))

	return table

	
# Handles raw HTML from each individual row, converting into a tuple for database insertion/return
def get_row_info(row, week_no, csv=False):
	week_day = ""
	date = ""
	start_time = ""
	end_time = ""
	course_code = ""
	course_type = ""
	info = ""
	campus = ""
	rooms = ""

	for i in range(len(row)):
		if len(row[i].getText()) > 0:
			# Get rid of any surrounding whitespace
			val = row[i].getText().strip()

			# Convert weekdays
			if i == 0:
				week_day = day_convert[val]

			# Properly format dates (these are English)
			if i == 1:
				date = parser.parse(val).isoformat()[:10]

			# Split the to-from times, have different columns
			if i == 2:
				time_list = val.split("-")
				start_time = time_list[0]
				end_time = time_list[1]

			# Extract info like subject code, type of class
			elif i == 3:
				# Find course codes. If it can't be found, all the info will be in the info column.
				# Use this to map actual courses.
				course_codes = re.findall(SUB_CODE_RE, val)
				if len(course_codes) > 0:
					course_code = "/".join(course_codes)
					for c in course_codes:
						val = val.replace(c, "")
				else: 
					course_code = "See info"
					info = val
				
				# Check for types of lectures.
				
				type_check = parse_type(val)
				
				course_type = type_check[0]		
				info =  type_check[1]
	
				# Remove pointless numbers and symbols in front of info	
				while len(info) > 0 and (not info[0].isalpha() and not info[0] in "æøå"):
					info = info[1:]

			# Find and extract rooms
			elif i == 4:
				# Check for campus
				campus_check = val.lower()
				if "grm" in campus_check:
					campus = "Grimstad"
				elif "krs" in campus_check:
					campus = "Kristiansand"
				else:
					campus = "Unknown"
				
				# If we can't find the rooms, just set whatever is in the column
				listed_rooms = re.findall(ROOMS_RE, val)
				if len(listed_rooms) > 0:
					rooms = "/".join(listed_rooms)
				else:
					rooms = val

	vals = (week_no, week_day, date, start_time, end_time, course_code, course_type, info, campus, rooms)
	if csv: vals = ";".join(vals) + ";\n"
	return vals
