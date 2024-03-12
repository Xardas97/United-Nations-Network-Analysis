import requests
from bs4 import BeautifulSoup

from constants import *

PAR_SUBJECT_MIDDLE_EAST = "MIDDLE EAST SITUATION"

def crawl(body, vote, subject, date):
    url = build_url(body, vote, subject, date)

    source_code = requests.get(url)
    source_code_text = source_code.text

    soup_object = BeautifulSoup(source_code_text, 'html.parser')
    for line in soup_object.find_all('a', {'class': 'moreinfo'}, True, "Detailed record"):
        print(line)

def build_url(body, vote, subject, date):
    url = BASE_URL

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

crawl(ParamBody.GENERAL_ASSEMBLY, ParamVote.YES, PAR_SUBJECT_MIDDLE_EAST, 2015)
