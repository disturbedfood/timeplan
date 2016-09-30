class Course:
    def __init__(self, name, hashcode, code):
        self.subjects = set()
        self.name = name
        self.hashcode = hashcode
        self.code = code

    def add_subject(self, subject_code):
        self.subjects.add(subject_code)
        
class DataRow:
    def __init__(self):
        self.week = ""
        self.day = ""
        self.date = ""
        self.start = ""
        self.end = ""
        self.code = ""
        self.type = ""
        self.info = ""
        self.campus = ""
        self.rooms = ""
        
    def get_data_tuple(self):
       return (self.week, self.day, self.date, self.start, self.end, self.code, self.type, self.info, self.campus, self.rooms)
    
    def get_csv_data(self):
        return ";".join(self.get_data_tuple) + ";\n"
