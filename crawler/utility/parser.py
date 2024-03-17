import re

from constants import *
from utility.record import *

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

   @staticmethod
   def parse_subjects(soup):
      subjects = []
      for checkbox in soup.find_all('input', {'id': re.compile(SearchResultRegex.SUBJECT_CHECKBOX)}):
         subject = checkbox.get('aria-label')
         subjects.append(subject)

      return subjects

class RecordParser:
   @classmethod
   def parse(cls, soup):
      title = cls.__get_record_value_tag(soup, RecordRegex.TITLE).string.replace("\u0301", "").replace("\u0302", "")
      date = cls.__get_record_value_tag(soup, RecordRegex.DATE).contents[0].string
      resolution = cls.__get_resolution(soup)
      voting_data = cls.__get_voting_data(soup)

      return Record(title, date, resolution, voting_data)

   @classmethod
   def __get_record_value_tag(cls, soup, value):
      title_tag = soup.find('span', {'class': 'title'}, string=re.compile(value))
      return title_tag.nextSibling if title_tag else None

   @classmethod
   def __get_resolution(cls, soup):
      resolution_tag = cls.__get_record_value_tag(soup, RecordRegex.RESOLUTION)
      if not resolution_tag:
         return ""

      return resolution_tag.contents[0].string

   @classmethod
   def __get_voting_data(cls, soup):
      voting_data_tag = cls.__get_record_value_tag(soup, RecordRegex.VOTING_DATA)
      if not voting_data_tag:
         return "Concensus"

      voting_data = []

      raw_voting_data = cls.__to_text_with_br_tags_replaced(voting_data_tag).split("\n")
      for vote in raw_voting_data:
         vote = vote.replace("İ", "I")
         if not cls.__has_voting_prefix(vote):
            vote = "X " + vote

         voting_data.append(vote)

      return ";".join(voting_data)

   @staticmethod
   def __has_voting_prefix(vote):
      return vote.startswith("A ") or vote.startswith("Y ") or vote.startswith("N ")

   @classmethod
   def __to_text_with_br_tags_replaced(cls, tag):
      text = ''

      for child in tag.recursiveChildGenerator():
         if child.name == 'br':
               text += '\n'
         elif isinstance(child, str):
               text += child.strip()

      return text
