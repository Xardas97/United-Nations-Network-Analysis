import os.path
import requests
from bs4 import BeautifulSoup

from constants import *

class Downloader:
   @classmethod
   def download_search_page(cls, body, vote, subject, date, page = 0):
      url = cls.build_search_url(body, vote, subject, date, page)
      source_code = requests.get(url, verify=cls.get_certificate())
      return BeautifulSoup(source_code.text, 'html.parser')

   @classmethod
   def download_record(cls, record_id):
      url = cls.build_record_url(record_id)
      source_code = requests.get(url, verify=cls.get_certificate())
      return BeautifulSoup(source_code.text, 'html.parser')

   @staticmethod
   def get_certificate():
      if os.path.isfile(CERTIFICATE_PATH):
         return CERTIFICATE_PATH

      return None

   @classmethod
   def build_search_url(cls, body, vote, subject, date, page):
      url = BASE_SEARCH_URL

      if body:
         url = cls.add_param(url, ParamTag.BODY, body)

      if vote:
         url = cls.add_param(url, ParamTag.VOTE, vote)

      if subject:
         url = cls.add_param(url, ParamTag.SUBJECT, subject)

      if date:
         url = cls.add_param(url, ParamTag.DATE, str(date))

      url = cls.add_param(url, ParamTag.PER_PAGE, str(RECORDS_PER_PAGE))

      first_record = page * RECORDS_PER_PAGE + 1
      url = cls.add_param(url, ParamTag.FIRST_RECORD, str(first_record))

      return url

   @staticmethod
   def add_param(url, param_tag, param_value):
      return url + "&" + param_tag + "=" + param_value

   @staticmethod
   def build_record_url(record_id):
      return RECORD_URL.format(record_id)
