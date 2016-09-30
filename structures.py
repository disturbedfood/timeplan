class Course:
    def __init__(self, name, hashcode, code):
        self.subjects = set()
        self.name = name
        self.hashcode = hashcode
        self.code = code
       
    @classmethod
    def from_db(cls, row):
        name = row[0]
        hashcode = row[1]
        return cls(name, hashcode, "")

    def add_subject(self, subject_code):
        self.subjects.add(subject_code)
        
    def response_json(self):
        return {"name": self.name, "code": self.hashcode, "subjects": list(self.subjects)}
        
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
