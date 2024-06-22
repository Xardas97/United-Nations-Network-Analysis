import os.path

from constants import *

class RecordPrinter:
   @classmethod
   def print_to_file(cls, records, year = None):
      records_file = RECORDS_PER_YEAR_TABLE_PATH.format(year) if year else RECORDS_TABLE_PATH
      print("Saving {} records to {}...".format(len(records), records_file))

      os.makedirs(DATA_FOLDER_PATH, exist_ok = True)
      with open(records_file, 'w', encoding="utf8") as file:
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
      title = cls.escape_double_quptes(record.title)
      subjects = cls.set_to_string(record.subjects)
      return RECORD_TABLE_FORMAT.format(record.id, record.body, title, record.date, record.resolution, subjects, record.voting_data)

   @classmethod
   def set_to_string(cls, set):
      return '{' + ', '.join(f"'{cls.escape_single_quotes(s)}'" for s in set) + '}'

   @classmethod
   def escape_single_quotes(cls, string):
      return string.replace("'", "\\'") if string else ""

   @classmethod
   def escape_double_quptes(cls, string):
      return string.replace("\"", "\"\"") if string else ""