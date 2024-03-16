from parser import *
from printer import *
from downloader import *

records = {}

def crawl_all():
   subjects_file = open(SUBJECTS_FILE_PATH)
   subjects = subjects_file.read().splitlines()

   record_count = 0
   record_count += crawl(ParamBody.GENERAL_ASSEMBLY, None, subjects[9], 2005)

   print("Total crawled: " + str(record_count))
   RecordPrinter.print_to_file(records)

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
      if subject:
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
