# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import sqlite3 as sql
import datetime as dt
import os

ver = "1.0"

app = Flask(__name__)

# Filter out any disallowed special characters from table name (to avoid injection), wrap in quotation marks
def clean_table_name(tab):
	ret = ''.join(_ for _ in tab if _.isalnum() or _ in ".,æøå# ".decode("utf-8"))
	return unicode("\"" + ret + "\"")

# Build a query to fetch the actual timetable
def timetable_query(subject_code, week):
	return "SELECT Weekday, Date, StartTime, EndTime, Course, Type, Info, Campus, Rooms FROM %s \
		WHERE Week = %s" % (clean_table_name(subject_code), str(week))

# Return all saved subjects, or just the info for one if a subject code is specified
def subjects_query(subject=None):
	query = "SELECT * FROM Subjects"
	if subject: query += " WHERE Code = %s" % (clean_table_name(subject))
	return query

def json_error(err):
	return {"error": err}

# Runs a database query. (be careful)
def fetch_from_db(query):
	try:
		db_con = sql.connect("timetable.db")
		db_con.text_factory = str
		with db_con:
			cur = db_con.cursor()
			cur.execute(query)
			data = cur.fetchall()

		return data

	except sql.Error, e:
		return json_error("SQL error: " + str(e))

@app.route('/<subject>/<week>')
def index(subject="", week=1):
	# Hash sign can be included (needs to be escaped) or omitted
	if subject[0] != "#" and "SPLUS" in subject: subject = "#" + subject
	
	# Set valid week 
	if not week.isdigit(): week = dt.date.today().isocalendar()[1]
	else: week = int(week)
	meta = {"week": week,
		"subject_code": subject,
		"subject_name": "Not implemented",
		"last_updated": "Not implemented",
		"indices": ["Week day", "Date", "Start time", "End time", "Course", "Type", "Info", "Campus", "Rooms"] }

	data = fetch_from_db(timetable_query(unicode(subject), week))

	if "error" in data: return jsonify(data)

	return jsonify({"timeplan": data, "meta": meta }) 


if __name__== '__main__':
	app.run(debug=True)
