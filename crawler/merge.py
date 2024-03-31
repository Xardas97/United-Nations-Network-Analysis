import os.path
import pandas as pd

from constants import *

def merge():
   start_year = 1946 #1946
   end_year = 2024 #2024

   if not os.path.isdir(DATA_FOLDER_PATH):
      print("The data folder does not exist!")
      return

   merged_records = pd.DataFrame()
   for year in range(start_year, end_year + 1):
      print("Loading records for year {}...".format(year))
      record_file_path = RECORDS_PER_YEAR_TABLE_PATH.format(year)
      if not os.path.isfile(record_file_path):
         print("Records file for year {} is missing".format(year))
         continue

      records_file = pd.read_csv(record_file_path, encoding='latin-1')
      merged_records = pd.concat([merged_records, records_file], axis=0)

   print("Saving merged records...")
   merged_records.to_csv(RECORDS_TABLE_PATH, index=False)

merge()
