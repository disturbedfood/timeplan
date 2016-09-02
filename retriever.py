# -*- coding: utf-8 -*-
import dbtools
import timeplan


# "t": this week
# TODO: be clever about multiple weeks

# "h": fetching for autumn, for spring use "v"

# "1-6": fetching for mon-sat, can be "1-3", "4-6"

#print timeplan.parse_type("g/forel/01")



courses = timeplan.retrieve_course_codes("h")
dbtools.save_course_codes(courses)
print "Added courses to database."

justafew = {}
count = 0
for k, v in courses.iteritems():
	if count > 4: break
	justafew[k] = v
	count += 1

tt = timeplan.get_all(justafew, "1-6", "33;34;35;36;37;38;39;40;41;42;43;44;45;46;47;48;49;50", "h")

for k, v in tt.iteritems():
	dbtools.add_to_db(v, k)

print "Added all timetables to database."
