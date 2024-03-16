import os.path
import requests
from bs4 import BeautifulSoup

from parser import *
from constants import *

records = {}

def crawl_all():
   subjects_file = open(SUBJECTS_FILE_PATH)
   subjects = subjects_file.read().splitlines()

   record_count = 0
   record_count += crawl(ParamBody.GENERAL_ASSEMBLY, None, subjects[9], 2005)

   print("Total crawled: " + str(record_count))
   save_records()

def save_records():
   print("Saving records to file...")

   os.makedirs(DATA_FOLDER_PATH, exist_ok = True)
   with open(RECORDS_TABLE_PATH, 'w') as file:
      file.write(RECORD_TABLE_HEADER)
      for _, record in records.items():
         table_row = to_table_row(record)
         file.write("\n" + table_row)

   print("Finished saving records!")

def to_table_row(record):
   return RECORD_TABLE_FORMAT.format(record.id, record.body, record.title, record.date, record.resolution, record.subjects, record.voting_data)

def crawl(body, vote, subject, date, page = 0):
   if page == 0:
      print("Accessing: [Body: {}, Vote: {}, Subject: {}, Date: {}]".format(fpvp(body), fpvp(vote), fpp(subject), fpp(date)))

   url = build_search_url(body, vote, subject, date, page)

   source_code = requests.get(url, verify=get_certificate())
   soup = BeautifulSoup(source_code.text, 'html.parser')

   search_results = SearchResultParser.parse(soup)

   record_count = 0
   for record_id in search_results.records:
      newRecord = process_record(record_id, body, subject)
      if newRecord:
         record_count += 1

   if search_results.has_next_page:
      print("Moving to page {}...".format(page + 1))
      record_count += crawl(body, vote, subject, date, page + 1)

   if page == 0:
      print("Crawled in this search: {}\n".format(record_count))

   return record_count

def process_record(record_id, body, subject):
   existing_record = records.get(record_id)
   if not existing_record:
      print("Creating new record {}".format(record_id))
      record = crawl_record(record_id)
      record.set_external_data(record_id, body, subject)
      records[record_id] = record
      return True
   else:
      if subject:
         print("Adding subject \"{}\" to record {}".format(subject, record_id))
         existing_record.subjects.add(subject)
      return False

def crawl_record(record_id):
   url = build_record_url(record_id)

   source_code = requests.get(url, verify=get_certificate())
   soup = BeautifulSoup(source_code.text, 'html.parser')

   return RecordParser.parse(soup)

def get_certificate():
   if os.path.isfile(CERTIFICATE_PATH):
      return CERTIFICATE_PATH

   return None

def build_search_url(body, vote, subject, date, page):
   url = BASE_SEARCH_URL

   if body:
      url = add_param(url, ParamTag.BODY, body)

   if vote:
      url = add_param(url, ParamTag.VOTE, vote)

   if subject:
      url = add_param(url, ParamTag.SUBJECT, subject)

   if date:
      url = add_param(url, ParamTag.DATE, str(date))

   url = add_param(url, ParamTag.PER_PAGE, str(RECORDS_PER_PAGE))

   first_record = page * RECORDS_PER_PAGE + 1
   url = add_param(url, ParamTag.FIRST_RECORD, str(first_record))

   return url

def build_record_url(record_id):
   return RECORD_URL.format(record_id)

def add_param(url, param_tag, param_value):
   return url + "&" + param_tag + "=" + param_value

# friendly param print
def fpp(val):
   return val if val else "All"

# friendly param value print
def fpvp(val):
   return val.value if val and val.value else "All"

crawl_all()
