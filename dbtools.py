from time import mktime
import datetime as dt
import sqlite3 as sql

ROWS_SQL_TABLE = "(Week INT, Weekday VARCHAR(3), Date VARCHAR(10), StartTime VARCHAR(5), \
		  EndTime VARCHAR(5), Course VARCHAR(16), Type VARCHAR(10), Info VARCHAR(64), \
		  Campus VARCHAR(20), Rooms VARCHAR(128));"

COURSE_CODES_SQL_TABLE = "(HashCode VARCHAR(10), ServerCode VARCHAR(64), Name VARCHAR(256), LastUpdated BIGINT);"


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
			print "Timetable inserted into database"

	except sql.Error, e:
		print "SQL error:", str(e)
		
def save_course_codes(codes):
		db_data = []
		current_time = int(mktime(dt.datetime.utcnow().timetuple()))
		for k, v in codes.iteritems():
			db_data.append((k, v[1], v[0], current_time))
		try:
			db_con = sql.connect("timetable.db")
			with db_con:
				cur = db_con.cursor()
				cur.execute("DROP TABLE IF EXISTS Courses;")
				cur.execute("CREATE TABLE Courses " + COURSE_CODES_SQL_TABLE)
				cur.executemany("INSERT INTO Courses VALUES (?, ?, ?, ?);", db_data)	
		except sql.Error, e:
			print "SQL error: " + str(e)