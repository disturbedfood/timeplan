# -*- coding: utf-8 -*-
import dbtools
import timeplan
from structures import Course


# "t": this week
# TODO: be clever about multiple weeks

# "h": fetching for autumn, for spring use "v"

# "1-6": fetching for mon-sat, can be "1-3", "4-6"

#print timeplan.parse_type("g/forel/01")


courses = timeplan.retrieve_course_codes("h")
# for v in courses: print v.subjects
dbtools.save_course_codes(courses)
print "Added courses to database."

justafew = []
count = 0
for c in courses:
    if count > 2: break
    justafew.append(c)
    count += 1

justafew.append(Course("Ingeni\u00f8rfag - Data bachelor 3. \u00e5r (datateknikk)", "6b41ed012c", "#SPLUS25990A"))
    
tt = timeplan.get_all(justafew, "1-6", "33;34;35;36;37;38;39;40;41;42;43;44;45;46;47;48;49;50", "h")
# for c in tt[1]: print "Course", c.name, "has subjects", c.subjects

dbtools.save_subject_codes(tt[1])

for k, v in tt[0].iteritems():
    dbtools.add_to_db(v, k)

print "Added all timetables to database."

# print timeplan.parse_type("DAT220-G/Forel øv/01".decode('utf-8'))
