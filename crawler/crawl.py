import re
import os.path
import requests
from bs4 import BeautifulSoup

from constants import *

class Record:
   RECORD_TABLE_HEADER = "ID,Title,Date,Resolution,Subejcts,Voting Data"
   RECORD_TABLE_FORMAT = "\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\""
   RECORD_PRINT_FORMAT = "ID: {}\nTitle: {}\nDate: {}\nResolution: {}\nSubjects: {}\nVoting data: {}"

   def __init__(self, id, title, date, resolution, voting_data, subject):
      self.id = id
      self.title = title
      self.date = date
      self.resolution = resolution
      self.voting_data = voting_data
      self.subjects = { subject }

   def __str__(self):
      return Record.RECORD_PRINT_FORMAT.format(self.id, self.title, self.date, self.resolution, self.subjects, self.voting_data)

   def to_table_row(self):
      return Record.RECORD_TABLE_FORMAT.format(self.id, self.title, self.date, self.resolution, self.subjects, self.voting_data)

records = {}

def crawl_all():
   subjects_file = open(SUBJECTS_FILE_PATH)
   subjects = subjects_file.read().splitlines()

   record_count = 0
   record_count += crawl(ParamBody.SECURITY_COUNCIL, ParamVote.YES, subjects[6], 1999)
   record_count += crawl(ParamBody.SECURITY_COUNCIL, ParamVote.YES, subjects[27], 1999)

   print("Total crawled: " + str(record_count))
   save_records()

def save_records():
   print("Saving records to file...")

   os.makedirs(DATA_FOLDER_PATH, exist_ok = True)
   with open(RECORDS_TABLE_PATH, 'w') as file:
      file.write(Record.RECORD_TABLE_HEADER)
      for _, record in records.items():
         table_row = record.to_table_row()
         file.write("\n" + table_row)

   print("Finished saving records!")

def crawl(body, vote, subject, date, page = 0):
   if page == 0:
      print("Accessing: [Body: {}, Vote: {}, Subject: {}, Date: {}]".format(fpvp(body), fpvp(vote), fpp(subject), fpp(date)))

   url = build_search_url(body, vote, subject, date, page)

   source_code = requests.get(url, verify=get_certificate())
   soup_object = BeautifulSoup(source_code.text, 'html.parser')

   record_count = 0
   for link in soup_object.find_all('abbr', {'class': 'unapi-id'}):
      record_id = link.get('title')
      newRecord = process_record(record_id, subject)
      if newRecord:
         record_count += 1

   nextPageTag = soup_object.find('img', {'alt': 'next'})
   if nextPageTag:
      print("Moving to page {}...".format(page + 1))
      record_count += crawl(body, vote, subject, date, page + 1)

   if page == 0:
      print("Crawled in this search: {}\n".format(record_count))

   return record_count

def process_record(record_id, subject):
   existing_record = records.get(record_id)
   if not existing_record:
      print("Creating new record {}".format(record_id))
      records[record_id] = crawl_record(record_id, subject)
      return True
   else:
      if subject:
         print("Adding subject \"{}\" to record {}".format(subject, record_id))
         existing_record.subjects.add(subject)
      return False

def crawl_record(record_id, subject):
   url = build_record_url(record_id)

   source_code = requests.get(url, verify=get_certificate())
   soup_object = BeautifulSoup(source_code.text, 'html.parser')

   title = soup_object.find('span', {'class': 'title'}, string=re.compile('^Title\\s*$')).nextSibling.string
   date = soup_object.find('span', {'class': 'title'}, string=re.compile('^Vote date\\s*$')).nextSibling.contents[0].string
   resolution = soup_object.find('span', {'class': 'title'}, string=re.compile('^Resolution\\s*$')).nextSibling.contents[0].string

   voting_data_tag = soup_object.find('span', {'class': 'title'}, string=re.compile('^Vote\\s*$')).nextSibling
   voting_data = to_text_with_br_tags_replaced(voting_data_tag).replace("\n", ";")

   return Record(record_id, title, date, resolution, voting_data, subject)

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

def to_text_with_br_tags_replaced(tag):
   text = ''

   for child in tag.recursiveChildGenerator():
      if child.name == 'br':
         text += '\n'
      elif isinstance(child, str):
         text += child.strip()

   return text

# friendly param print
def fpp(val):
   return val if val else "All"

# friendly param value print
def fpvp(val):
   return val.value if val and val.value else "All"

crawl_all()
