import sys

from constants import *
from utility.record import *
from utility.parser import *
from utility.reader import *
from utility.printer import *
from utility.downloader import *

sys.stdout.reconfigure(encoding='utf-8')

records = {}

def crawl_all():
   start_date = 1946 #1946
   end_date = 2024 #2024
   ignore_subjects = False

   if len(sys.argv) == 2:
      start_date = int(sys.argv[1])
      end_date = start_date

   if len(sys.argv) > 2:
      start_date = int(sys.argv[1])
      end_date = int(sys.argv[2])

   if len(sys.argv) == 4 and sys.argv[3] == IGNORE_SUBJECTS_ARG:
      ignore_subjects = True

   for date in range(start_date, end_date + 1):
      crawl_date(date, ignore_subjects)

def crawl_date(date, ignore_subjects = False):
   Reader.read_records(date, records)
   print("Reusing {} record(s) for year {}".format(len(records), date))

   try:
      un_bodies = [ParamBody.SECURITY_COUNCIL, ParamBody.GENERAL_ASSEMBLY]
      for body in un_bodies:
         subjects = get_subjects(body, date) if not ignore_subjects else []
         if len(subjects) == 0:
            crawl(body, None, None, date)
            continue

         for subject in subjects:
            crawl(body, None, subject, date)

      print("Total crawled for date {}: {}".format(date, (len(records))))
   finally:
      RecordPrinter.print_to_file(records, date)

def get_subjects(body, date):
   print("Accessing all subjects for [Body: {}, Date: {}]\n".format(fpvp(body), fpp(date)))
   soup = Downloader.download_search_page(body, None, None, date)
   return SearchResultParser.parse_subjects(soup)

def crawl(body, vote, subject, date, page = 0):
   if page == 0:
      print("Accessing: [Body: {}, Vote: {}, Subject: {}, Date: {}]".format(fpvp(body), fpvp(vote), fpp(subject), fpp(date)))

   soup = Downloader.download_search_page(body, vote, subject, date, page)
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
      if subject and not subject in existing_record.subjects:
         print("Adding subject \"{}\" to record {}".format(subject, record_id))
         existing_record.subjects.add(subject)
      return False

def crawl_record(record_id):
   soup = Downloader.download_record(record_id)
   return RecordParser.parse(soup)

# friendly param print
def fpp(val):
   return val if val else "All"

# friendly param value print
def fpvp(val):
   return val.value if val and val.value else "All"

crawl_all()
