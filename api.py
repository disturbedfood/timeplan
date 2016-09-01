# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, jsonify
import sqlite3 as sql
import datetime as dt
import os

base = "/timeplan/1.0"

data_index = ["week_day", "date", "start_time", "end_time", "course", "type", "info", "campus", "rooms"]
app = Flask(__name__)

# Filter out any disallowed special characters from table name (to avoid injection), wrap in quotation marks
def clean_table_name(tab, wrap=True):
	ret = ''.join(_ for _ in tab if _.isalnum() or _ in ".,æøå# ")
	if wrap: return "\"" + ret + "\""
	else: return ret

# Build a query to fetch the actual timetable
def timetable_query(subject_code, week):
	return "SELECT Weekday, Date, StartTime, EndTime, Course, Type, Info, Campus, Rooms FROM %s \
		WHERE Week = %s;" % (clean_table_name(subject_code), str(week))

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

@app.route(base + '/subjects/')
@app.route(base + '/subjects/<search>')
def subjects(search=None):
	data = None
	if search:
		search = clean_table_name(search, wrap=False)
		data = fetch_from_db("SELECT Name, Code FROM Subjects WHERE Name LIKE '%%%s%%';" % search) 
	else:
		data = fetch_from_db("SELECT Name, Code FROM Subjects;")
	if "error" in data: return jsonify(data)

	else: 
		rows = []
		for row in data:
			rows.append({"name": row[0], "code": row[1]})
		return jsonify({'subjects': rows})

@app.route(base + '/timeplan/<subject>/<week>')
@app.route(base + '/<subject>/')
def index(subject, week=None):
	# Hash sign can be included (needs to be escaped) or omitted
	# if subject[0] != "#" and "SPLUS" in subject: subject = "#" + subject
	
	# Set valid week 
	if not week or not week.isdigit(): week = dt.date.today().isocalendar()[1]
	else: week = int(week)

	data = fetch_from_db(timetable_query(subject, week))
	subject_data = fetch_from_db("SELECT Name, LastUpdated FROM Subjects WHERE HashCode = '%s';" % subject)	

	if len(subject_data) == 0: return jsonify(json_error("Could not find subject"))

	meta = {"week": week,
		"subject_code": subject,
		"subject_name": subject_data[0][0],
		"last_updated": subject_data[0][1] }


	if "error" in data: return jsonify(data)

	data_formatted = []
	for d in data:
		data_formatted.append({data_index[i]: d[i] for i in range(9)})
	

	return jsonify({"timeplan": data_formatted, "meta": meta }) 


if __name__== '__main__':
	app.run(debug=True)
