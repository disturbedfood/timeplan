from time import mktime
import datetime as dt
import sqlite3 as sql

ROWS_SQL_TABLE = "(Week INT, Weekday VARCHAR(3), Date VARCHAR(10), StartTime VARCHAR(5), \
          EndTime VARCHAR(5), Subject VARCHAR(16), Type VARCHAR(10), Info VARCHAR(64), \
          Campus VARCHAR(20), Rooms VARCHAR(128));"

COURSE_CODES_SQL_TABLE = "(HashCode VARCHAR(10), ServerCode VARCHAR(64), Name VARCHAR(256), LastUpdated BIGINT);"

SUBJECT_CODES_SQL_TABLE = "(SubjectCode VARCHAR(6), HashCode VARCHAR(10));"

# Adds a subjects timetable to the database, with the code as the table name.
# Adding to the database will overwrite any existing subject information.
def add_to_db(timetable, code):
    try: 
        db_con = sql.connect("timetable.db")
        db_con.text_factory = str
        with db_con:
            table = "\"" + code + "\""
            cur = db_con.cursor()
            cur.execute("DROP TABLE IF EXISTS " + table)
            cur.execute("CREATE TABLE " + table + ROWS_SQL_TABLE)
            cur.executemany("INSERT INTO " + table + " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", timetable)

    except sql.Error, e:
        print "SQL error:", str(e)
        
def save_course_codes(courses):
    db_data = []
    current_time = int(mktime(dt.datetime.utcnow().timetuple()))
    for course in courses:
        db_data.append((course.hashcode, course.code, course.name, current_time))
    try:
        db_con = sql.connect("timetable.db")
        with db_con:
            cur = db_con.cursor()
            cur.execute("DROP TABLE IF EXISTS Courses;")
            cur.execute("CREATE TABLE Courses " + COURSE_CODES_SQL_TABLE)
            cur.executemany("INSERT INTO Courses VALUES (?, ?, ?, ?);", db_data)    
    except sql.Error, e:
        print "SQL error: " + str(e)

def save_subject_codes(courses):
    db_format = []
    for course in courses:
        for s in course.subjects:
            db_format.append((s, course.hashcode))

    try: 
        db_con = sql.connect("timetable.db")
        db_con.text_factory = str
        with db_con:
            cur = db_con.cursor()
            cur.execute("DROP TABLE IF EXISTS Subjects;")
            cur.execute("CREATE TABLE Subjects" + SUBJECT_CODES_SQL_TABLE)
            cur.executemany("INSERT INTO Subjects VALUES (?, ?);", db_format)

    except sql.Error, e:
        print "SQL error:", str(e)
