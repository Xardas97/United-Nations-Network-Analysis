import os.path

from constants import *

class RecordPrinter:
   @classmethod
   def print_to_file(cls, records, year = None):
      records_file = RECORDS_PER_YEAR_TABLE_PATH.format(year) if year else RECORDS_TABLE_PATH
      print("Saving {} records to {}...".format(len(records), records_file))

      os.makedirs(DATA_FOLDER_PATH, exist_ok = True)
      with open(records_file, 'w') as file:
         cls.__print_to_file(file, records)

      print("Finished saving records!")

   @classmethod
   def __print_to_file(cls, file, records):
      file.write(RECORD_TABLE_HEADER)
      for _, record in records.items():
         try:
            table_row = cls.to_table_row(record)
            file.write("\n" + table_row)
         except Exception as e:
            print("Exception while saving record {}: {}".format(record.id, e))

   @classmethod
   def to_table_row(cls, record):
      title = record.title.replace("\"", "\"\"") if record.title else ""
      return RECORD_TABLE_FORMAT.format(record.id, record.body, title, record.date, record.resolution, record.subjects, record.voting_data)
