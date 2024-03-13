import re
import os.path
import requests
from bs4 import BeautifulSoup

from constants import *

def crawl_all():
   subjects_file = open(SUBJECTS_FILE_PATH)
   subjects = subjects_file.read().splitlines()

   subject = subjects[6]
   crawl(ParamBody.SECURITY_COUNCIL, ParamVote.YES, subject, 1999)

def crawl(body, vote, subject, date):
   url = build_url(body, vote, subject, date)
   print("Accessing: [Body: {}, Vote: {}, Subject: {}, Date: {}]\n\n".format(body.value, vote.value, subject, date))

   source_code = requests.get(url, verify=get_certificate())

   soup_object = BeautifulSoup(source_code.text, 'html.parser')
   for link in soup_object.find_all('a', {'class': 'moreinfo'}, string="Detailed record"):
      record = link.get('href')
      print(record)
      crawl_record(record)
      print("\n")

def crawl_record(link):
   url = BASE_URL + link
   source_code = requests.get(url, verify=get_certificate())

   soup_object = BeautifulSoup(source_code.text, 'html.parser')

   title = soup_object.find('span', {'class': 'title'}, string=re.compile('^Title\\s*$')).nextSibling.string
   date = soup_object.find('span', {'class': 'title'}, string=re.compile('^Vote date\\s*$')).nextSibling.contents[0].string
   resolution = soup_object.find('span', {'class': 'title'}, string=re.compile('^Resolution\\s*$')).nextSibling.contents[0].string

   voting_data_tag = soup_object.find('span', {'class': 'title'}, string=re.compile('^Vote\\s*$')).nextSibling
   voting_data = to_text_with_br_tags_replaced(voting_data_tag)

   print("Title: " + title)
   print("Resolution: " + resolution)
   print("Date: " + date)
   print("Voting data:\n" + voting_data)

def get_certificate():
   if os.path.isfile(CERTIFICATE_PATH):
      return CERTIFICATE_PATH

   return None

def build_url(body, vote, subject, date):
    url = BASE_SEARCH_URL

    if body:
       url = add_param(url, ParamTag.BODY, body)

    if vote:
       url = add_param(url, ParamTag.VOTE, vote)

    if subject:
       url = add_param(url, ParamTag.SUBJECT, subject)

    if date:
       url = add_param(url, ParamTag.DATE, str(date))

    return url

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

crawl_all()
