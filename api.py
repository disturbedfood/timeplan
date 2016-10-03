# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, jsonify
import sqlite3 as sql
import datetime as dt
import os
import re
from structures import Course
from flask_cors import CORS, cross_origin

base = "/timeplan/2.0"

data_index = ["week_day", "date", "start_time", "end_time", "subject", "type", "info", "campus", "rooms"]
app = Flask(__name__)
CORS(app)

# Build a query to fetch the actual timetable
def timetable_query(course_code, week):
    return "SELECT Weekday, Date, StartTime, EndTime, Subject, Type, Info, Campus, Rooms FROM '%s' \
        WHERE Week = %s;" % (course_code, str(week))

def timetable_query_with_sub(course_code, week, subject_code):
    return "SELECT Weekday, Date, StartTime, EndTime, Subject, Type, Info, Campus, Rooms FROM '%s' \
        WHERE Week = %s AND Subject LIKE '%%%s%%';" % (course_code, str(week), subject_code)

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

@app.route(base + '/courses')
@app.route(base + '/courses/<search>')
def courses(search=None):
    data = None
    if search:
        data = fetch_from_db("SELECT Name, HashCode FROM Courses WHERE Name LIKE '%%%s%%';" % search) 
    else:
        data = fetch_from_db("SELECT Name, HashCode FROM Courses;")
    if "error" in data: return jsonify(data)

    else: 
        rows = []
        for row in data:
            course = Course.from_db(row)
            subjects = fetch_from_db("SELECT SubjectCode FROM Subjects WHERE HashCode LIKE '%%%s%%'" % course.hashcode)
            if not "error" in subjects and len(subjects) != 0:
                print subjects
                for s in subjects: course.add_subject(s[0])
            rows.append(course.response_json())
        return jsonify({'courses': rows})

@app.route(base + '/subjects')
def subjects():
    subject_data = fetch_from_db("SELECT SubjectCode, HashCode FROM Subjects;")

    if "error" in subject_data: return jsonify(subject_data)
    else:
        rows = []
        for row in subject_data:
            rows.append({"subject_code": row[0], "code": row[1]})

    return jsonify({'subjects': rows})


@app.route(base + "/subject/<subject>/<week>")
@app.route(base + "/subject/<subject>")
def subject(subject, week=None):
    if not len(subject) == 6 and re.match("^[A-Za-z0-9_-]*$", subject):
        return jsonify({"error": "subject code must be 6 characters long and alphanumeric."})

    # Set valid week 
    if not week or not week.isdigit(): week = dt.date.today().isocalendar()[1]
    else: week = int(week)

    course_code = fetch_from_db("SELECT HashCode FROM Subjects WHERE SubjectCode = '%s';" % subject)
    if len(course_code) == 0: return jsonify(json_error("Could not find subject"))
    else: course_code = course_code[0][0]

    data = fetch_from_db(timetable_query_with_sub(course_code, week, subject))
    course_data = fetch_from_db("SELECT Name, LastUpdated FROM Courses WHERE HashCode = '%s';" % course_code)
    if len(course_data) == 0: return jsonify(json_error("Could not find course"))
    print course_data
    meta = {"week": week,
        "subject_code": subject,
        "course_code": course_code,
        "course_name": course_data[0][0],
        "last_updated": course_data[0][1] }

    if "error" in data: return jsonify(data)

    data_formatted = []
    for d in data:
        data_formatted.append({data_index[i]: d[i] for i in range(9)})

    return jsonify({"timeplan": data_formatted, "meta": meta })

@app.route(base + '/course/<course>/<week>')
@app.route(base + '/course/<course>')
def course(course, week=None):
    if not len(course) == 10 and re.match("^[A-Za-z0-9_-]*$", course):
        return jsonify({"error": "course code must be 10 characters long and alphanumeric."})
    
    # Set valid week 
    if not week or not week.isdigit(): week = dt.date.today().isocalendar()[1]
    else: week = int(week)

    data = fetch_from_db(timetable_query(course, week))
    course_data = fetch_from_db("SELECT Name, LastUpdated FROM Courses WHERE HashCode = '%s';" % course)    
    if len(course_data) == 0: return jsonify(json_error("Could not find course"))

    meta = {"week": week,
        "course_code": course,
        "course_name": course_data[0][0],
        "last_updated": course_data[0][1] }


    if "error" in data: return jsonify(data)

    data_formatted = []
    for d in data:
        data_formatted.append({data_index[i]: d[i] for i in range(9)})
    

    return jsonify({"timeplan": data_formatted, "meta": meta }) 


if __name__== '__main__':
    app.run()
