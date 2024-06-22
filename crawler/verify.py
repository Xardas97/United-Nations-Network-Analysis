import os.path

from constants import *

def verify_all():
   verified = True
   expected_counts = get_expected_record_count()

   start_year = 1946 #1946
   end_year = 2024 #2024

   for year in range(start_year, end_year + 1):
      verified &= verify_year(year, expected_counts[year])

   if verified:
      print("Verification completed successfully")
   else:
      print("Verification failed!")

def get_expected_record_count():
   with open(EXPECTED_RECORD_COUNTS_FILE_PATH) as expected_record_counts_file:
      expected_record_counts = expected_record_counts_file.read().splitlines()

   expected_counts_dict = {}
   for expected_record_count in expected_record_counts:
      split = expected_record_count.split(' ')
      year = int(split[0])
      count = int(split[1])
      expected_counts_dict[year] = count

   return expected_counts_dict

def verify_year(year, expected_count):
   records_file_path = RECORDS_PER_YEAR_TABLE_PATH.format(year)
   if not os.path.isfile(records_file_path):
      print("[Error][{}] Record file does not exist".format(year))
      return False

   verified = verify_record_count(records_file_path, year, expected_count)
   verified &= verify_mandatory_fields(records_file_path, year)
   return verified

def verify_record_count(records_file_path, year, expected):
   with open(records_file_path) as records_file:
      for count, _ in enumerate(records_file):
         pass

   if count != expected:
      print("[Error][{}] Wrong record count: [Expected {}, Actual {}]".format(year, expected, count))
      return False

   return True

def verify_mandatory_fields(records_file_path, year):
   with open(records_file_path) as records_file:
      records = records_file.read().splitlines()

   verified = True
   for record in records[1:]:
      verified &= verify_mandatory_fields_for_record(record, year)

   return verified

def verify_mandatory_fields_for_record(record, year):
   values = record.split(',')
   record_id = values[0]

   for value in values:
      if value == '""' or value == '"None"':
         print("[Error][{}] Missing value for record {}".format(year, record_id))
         return False

   return True

verify_all()