import os.path

from constants import *

class RecordPrinter:
   @classmethod
   def print_to_file(cls, records):
      print("Saving records to file...")

      os.makedirs(DATA_FOLDER_PATH, exist_ok = True)
      with open(RECORDS_TABLE_PATH, 'w') as file:
         cls.__print_to_file(file, records)

      print("Finished saving records!")

   @classmethod
   def __print_to_file(cls, file, records):
      file.write(RECORD_TABLE_HEADER)
      for _, record in records.items():
         table_row = cls.to_table_row(record)
         file.write("\n" + table_row)

   @classmethod
   def to_table_row(cls, record):
      return RECORD_TABLE_FORMAT.format(record.id, record.body, record.title, record.date, record.resolution, record.subjects, record.voting_data)
