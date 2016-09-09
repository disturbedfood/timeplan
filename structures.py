class Course:
    def __init__(self, name, hashcode, code):
        self.subjects = set()
        self.name = name
        self.hashcode = hashcode
        self.code = code


class DataRow:
    def __init__(self, week, day, date, start, end, code, type, info, campus, rooms):
        self.week = week
        self.day = day
        self.date = date
        self.start = start
        self.end = end
        self.code = code
        self.type = type
        self.info = info
        self.campus = campus
        self.rooms = rooms
        
    def get_data_tuple(self):
       return (self.week, self.day, self.date, self.start, self.end, self.code, self.type, self.info, self.campus, "/".join(self.rooms))
    
    def get_csv_data(self):
        return ";".join(self.get_data_tuple) + ";\n"
