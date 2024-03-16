import re

from constants import *

class SearchResults:
   def __init__(self, records, has_next_page):
      self.records = records
      self.has_next_page = has_next_page

class SearchResultParser:
   @staticmethod
   def parse(soup):
      records = []
      for link in soup.find_all('abbr', {'class': 'unapi-id'}):
         record_id = link.get('title')
         records.append(record_id)

      next_page_tag = soup.find('img', {'alt': 'next'})
      has_next_page = True if next_page_tag else False

      return SearchResults(records, has_next_page)

class Record:
   RECORD_PRINT_FORMAT = "ID: {}\nBody: {}\nTitle: {}\nDate: {}\nResolution: {}\nSubjects: {}\nVoting data: {}"

   def __init__(self, title, date, resolution, voting_data):
      self.title = title
      self.date = date
      self.resolution = resolution
      self.voting_data = voting_data

   def set_external_data(self, id, body, subject):
      self.id = id
      self.body = body.value if body else ""
      self.subjects = { subject }

   def __str__(self):
      return Record.RECORD_PRINT_FORMAT.format(self.id, self.body, self.title, self.date, self.resolution, self.subjects, self.voting_data)

class RecordParser:
   @classmethod
   def parse(cls, soup):
      title = cls.__get_record_value_tag(soup, RecordRegex.TITLE).string
      date = cls.__get_record_value_tag(soup, RecordRegex.DATE).contents[0].string
      resolution = cls.__get_record_value_tag(soup, RecordRegex.RESOLUTION).contents[0].string

      voting_data_tag = cls.__get_record_value_tag(soup, RecordRegex.VOTING_DATA)
      voting_data = cls.__get_voting_data(voting_data_tag)

      return Record(title, date, resolution, voting_data)

   @classmethod
   def __get_record_value_tag(cls, soup, value):
      title_tag = soup.find('span', {'class': 'title'}, string=re.compile(value))
      return title_tag.nextSibling if title_tag else None

   @classmethod
   def __get_voting_data(cls, voting_data_tag):
      if not voting_data_tag:
         return "Concensus"

      return cls.__to_text_with_br_tags_replaced(voting_data_tag).replace("\n", ";")

   @classmethod
   def __to_text_with_br_tags_replaced(cls, tag):
      text = ''

      for child in tag.recursiveChildGenerator():
         if child.name == 'br':
               text += '\n'
         elif isinstance(child, str):
               text += child.strip()

      return text
