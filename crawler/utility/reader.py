import os.path

from constants import *
from utility.record import *

class Reader:
   @staticmethod
   def read_records(year, records):
      records.clear()
      records_file_path = RECORDS_PER_YEAR_TABLE_PATH.format(year)

      if not os.path.isfile(records_file_path):
         return {}

      with open(records_file_path, encoding="utf8") as records_file:
         raw_records = records_file.read().splitlines()

      for raw_record in raw_records[1:]:
         record = Record.from_cached_record(raw_record)
         records[record.id] = record
