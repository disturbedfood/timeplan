# -*- coding: utf-8 -*-
import dbtools
import timeplan


# "t": this week
# TODO: be clever about multiple weeks

# "h": fetching for autumn, for spring use "v"

# "1-6": fetching for mon-sat, can be "1-3", "4-6"


courses = timeplan.retrieve_course_codes("h")
justafew = {}
count = 0
for k, v in courses.iteritems():
	if count > 5: break
	justafew[k] = v
	count += 1

tt = timeplan.get_all(justafew, "1-6", "t", "h")

for k, v in tt.iteritems():
	dbtools.add_to_db(v, k)
	
dbtools.save_course_codes(courses)
