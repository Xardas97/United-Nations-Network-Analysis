import ast

from constants import *

class Record:
   RECORD_PRINT_FORMAT = "ID: {}\nBody: {}\nTitle: {}\nDate: {}\nResolution: {}\nSubjects: {}\nVoting data: {}"

   def __init__(self, title, date, resolution, voting_data):
      self.title = title
      self.date = date
      self.resolution = resolution
      self.voting_data = voting_data

   def set_external_data(self, id, body, subject):
      self.id = id
      self.body = body.value if body else ""
      self.subjects = { subject } if subject else {}

   @classmethod
   def from_cached_record(cls, raw_record):
      values = raw_record[1:-1].split("\",\"")

      record = Record(values[2], values[3], values[4], values[6])
      record.id = values[0]
      record.body = values[1]
      record.subjects = ast.literal_eval(values[5])

      return record

   def __str__(self):
      return Record.RECORD_PRINT_FORMAT.format(self.id, self.body, self.title, self.date, self.resolution, self.subjects, self.voting_data)
