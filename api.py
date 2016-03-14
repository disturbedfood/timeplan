# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import sqlite3 as sql
import os

ver = "1.0"

app = Flask(__name__)

def clean_table_name(tab):
	ret = ''.join(_ for _ in tab if _.isalnum() or _ in ".,æøå# ".decode("utf-8"))
	return unicode("\"" + ret + "\"")

def fetch_from_db(subject_code, week):
	try:
		db_con = sql.connect("timetable.db")
		db_con.text_factory = str
		with db_con:
			cur = db_con.cursor()
			cur.execute("SELECT * FROM " + clean_table_name(subject_code) + " WHERE Week = ?", (str(week),))
			data = cur.fetchall()
		return data
	except sql.Error, e:
		print "SQL error:", str(e)

@app.route('/<subject>/<week>')
def index(subject="", week=1):
	if subject[0] != "#" and "SPLUS" in subject: subject = "#" + subject
	# d = fetch_from_db("#SPLUSE0C745", int(week))
	d = fetch_from_db(unicode(subject), week)
	final = ""
	for row in d:
		r = ""
		for _ in row:
			_ = str(_)
			r += " | " + _.decode("utf-8")
		final += r + "<br />"
	return final


if __name__== '__main__':
	app.run(debug=True)
